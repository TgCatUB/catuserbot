#!/usr/bin/env python

import argparse
import collections
import errno
import json
import math
import os
import re
import sys
import time

try:
    from urllib.request import HTTPError, Request, urlopen
except ImportError:
    from urllib2 import HTTPError, Request, urlopen

try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser

try:
    from urllib.parse import quote as urllib_quote
except ImportError:
    from urllib2 import quote as urllib_quote

__prog__ = "cmrudl.py"
__version__ = "1.0.6"
__copyright__ = "Copyright (c) 2019 JrMasterModelBuilder"
__license__ = "MPL-2.0"


class Main(object):
    DL_PROGRESS_START = 1
    DL_PROGRESS_READ = 2
    DL_PROGRESS_WROTE = 3
    DL_PROGRESS_DONE = 4

    def __init__(self, options):
        self.options = options
        self._output_progress_max = 0

    def log(self, message, verbose=False, err=False, nl=True):
        if verbose and not self.options.verbose:
            return
        self.output(message, err, nl)

    def output(self, message, err=False, nl=True):
        out = sys.stderr if err else sys.stdout
        out.write(message)
        if nl:
            out.write(os.linesep)
        out.flush()

    def output_progress_start(self):
        self.output_progress_max = 0

    def output_progress(self, message, err=False, nl=True):
        l = max(self._output_progress_max, len(message))
        self._output_progress_max = l
        message_pad = message.ljust(l)
        self.output("\r%s\r" % message_pad, err, False)

    def stat(self, path):
        try:
            return os.stat(path)
        except OSError as ex:
            if ex.errno != errno.ENOENT:
                raise ex
        return None

    def dict_has_props(self, dic, props):
        return all(p in dic for p in props)

    def assert_status_code(self, code, expected):
        if code != expected:
            raise Exception("Invalid status code: %s expected: %s" % (code, expected))

    def seconds_human(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)

    def bytes_human(self, size):
        based = float(size)
        base = 1024
        names = ["B", "K", "M", "G", "T"]
        il = len(names) - 1
        i = 0
        while based > base and i < il:
            based /= base
            i += 1
        return "%.2f%s" % (based, names[i])

    def percent_human(self, part, total):
        f = (part / float(total)) if total else 0
        return "%.2f%%" % (f * 100)

    def json_decode(self, s):
        return json.loads(s)

    def js_object_decode(self, s):
        # Add non-standard hex escape sequence support.
        def repl(m):
            p = m.group(0).split("\\x")
            p[1] = json.dumps(chr(int(p[1], 16)))[1:-1]
            return "".join(p)

        json_clean = re.sub(r"(^|[^\\])(\\\\)*\\x[0-9A-Fa-f]{2}", repl, s)
        return self.json_decode(json_clean)

    def request(self, url, headers):
        r = None
        try:
            req = Request(url, None, headers)
            r = urlopen(req, timeout=self.options.timeout)
        except HTTPError as ex:
            r = ex
        return r

    def request_data(self, url):
        res = self.request(url, {"User-Agent": ""})
        code = res.getcode()
        headers = res.info()
        body = res.read()
        return (code, headers, body)

    def request_data_decode(self, body, headers):
        # Should use headers to determine the correct encoding.
        return body.decode("utf-8")

    def request_header_get(self, headers, header, cast=None):
        r = headers[header] if header in headers else None
        if cast:
            try:
                r = cast(r)
            except:
                r = None
        return r

    def request_download(self, url, dest, progress, cont=False):
        buffer_size = self.options.buffer

        # Open the output file, append mode if continue.
        with open(dest, "ab" if cont else "wb") as fp:
            status = 200
            headers = {"User-Agent": ""}

            # Get the file size if continue.
            offset = fp.tell() if cont else 0
            continued = cont and offset
            if continued:
                # Switch to range request if continue from existing.
                status = 206
                headers["Range"] = "bytes=%s-" % (offset)

            start = time.time()
            progress(self.DL_PROGRESS_START, start, start, offset, 0, offset, None)

            res = self.request(url, headers)
            code = res.getcode()

            # If continued and range is invalid, then no more bytes.
            if continued and code == 416:
                progress(
                    self.DL_PROGRESS_DONE, start, time.time(), offset, 0, offset, offset
                )
                return

            self.assert_status_code(res.getcode(), status)

            headers = res.info()
            content_length = self.request_header_get(headers, "content-length", int)

            total = None if content_length is None else (offset + content_length)
            size = offset

            while True:
                data = res.read(buffer_size)
                added = len(data)
                if not added:
                    break
                size += added
                progress(
                    self.DL_PROGRESS_READ,
                    start,
                    time.time(),
                    offset,
                    added,
                    size,
                    total,
                )
                fp.write(data)
                progress(
                    self.DL_PROGRESS_WROTE,
                    start,
                    time.time(),
                    offset,
                    added,
                    size,
                    total,
                )

            progress(self.DL_PROGRESS_DONE, start, time.time(), offset, 0, size, total)

    def parse_storage(self, html):
        class TheHTMLParser(HTMLParser):
            def __init__(self):
                HTMLParser.__init__(self)
                self.script = False
                self.jsobjreg = re.compile(
                    r"^window\.cloudSettings[\s\r\n]*=[\s\r\n]*(\{[\s\S]*\});?$"
                )
                self.jsobj = None

            def handle_starttag(self, tag, attrs):
                self.script = tag.lower() == "script"

            def handle_data(self, data):
                if not self.script:
                    return
                src = data.strip()
                m = self.jsobjreg.match(src)
                if not m:
                    return
                self.jsobj = m.group(1)

            def result(self):
                if not self.jsobj:
                    return None
                return self.jsobj

        parser = TheHTMLParser()
        parser.feed(html)

        # The object is JSON, except any < is hex encoded, so use decode wrapper.
        jsobj = parser.result()
        cloud_settings = self.js_object_decode(jsobj)

        return {"cloudSettings": cloud_settings}

    def fetch_storage(self, url):
        self.log("Fetching storage: %s" % (url), True)
        (code, headers, body) = self.request_data(self.options.url[0])
        self.assert_status_code(code, 200)

        html = self.request_data_decode(body, headers)
        parsed = self.parse_storage(html)
        cloud_settings = parsed["cloudSettings"]
        if not cloud_settings:
            raise Exception("The cloudSettings object was not found")

        weblink_get = cloud_settings["dispatcher"]["weblink_get"]
        weblink_get_len = len(weblink_get)
        if weblink_get_len != 1:
            raise Exception(
                "Unexpected dispatcher.weblink_get count: %s" % (weblink_get_len)
            )

        weblink_get_url = weblink_get[0]["url"]
        self.log("Found URL: %s" % (weblink_get_url), True)

        state_id = cloud_settings["state"]["id"]
        self.log("Found ID: %s" % (state_id), True)

        folders = cloud_settings["folders"]
        file_info = self.search_folders(folders, state_id)
        if not file_info:
            raise Exception("Could not find file info in folders tree")

        file_name = file_info["name"]
        self.log("Found name: %s" % (file_name), True)

        file_size = file_info["size"]
        self.log("Found size: %s" % (file_size), True)

        file_mtime = file_info["mtime"]
        self.log("Found mtime: %s" % (file_mtime), True)

        # A unique hash, appears to be SHA1, but unknown what is hashed.
        # If how it is generated can be documented, could be used to verify download.
        file_hash = file_info["hash"]
        self.log("Found hash: %s" % (file_hash), True)

        return {
            "url": weblink_get_url,
            "id": state_id,
            "name": file_name,
            "size": file_size,
            "mtime": file_mtime,
            "hash": file_hash,
        }

    def fetch_token(self):
        url = "https://cloud.mail.ru/api/v2/tokens/download"
        self.log("Fetching token: %s" % (url), True)
        (code, headers, body) = self.request_data(url)
        self.assert_status_code(code, 200)

        json_str = self.request_data_decode(body, headers)
        json_obj = self.json_decode(json_str)

        obj_status = json_obj["status"]
        self.assert_status_code(obj_status, 200)

        token = json_obj["body"]["token"]
        self.log("Found token: %s" % (token), True)

        return token

    def search_folders(self, folders, search_id):
        props = ["id", "mtime", "name", "size", "hash"]
        queue = collections.deque([folders])
        while len(queue):
            entry = queue.pop()
            if self.dict_has_props(entry, props) and entry["id"] == search_id:
                return entry
            for k, v in entry.items():
                if isinstance(v, list):
                    for e in v:
                        if isinstance(e, dict):
                            queue.append(e)
                elif isinstance(v, dict):
                    queue.append(v)
        return None

    def create_download_url(self, storage, token):
        return "%s/%s?key=%s" % (storage["url"], storage["id"], urllib_quote(token))

    def create_out_dir(self):
        opt_dir = self.options.dir
        return opt_dir or ""

    def create_file_name_temp(self, storage):
        return ".%s.%s" % (__prog__, urllib_quote(storage["hash"]))

    def create_file_name(self, storage):
        opt_file = self.options.file
        if opt_file:
            return opt_file
        return storage["name"] if storage else None

    def download_verify_size(self, file_path, file_size):
        size = self.stat(file_path).st_size
        if size != file_size:
            raise Exception(
                "Unexected download size: %s expected: %s" % (size, file_size)
            )

    def download_set_mtime(self, file_path, file_mtime):
        os.utime(file_path, (file_mtime, file_mtime))

    def assert_not_exists(self, file_path):
        if self.stat(file_path):
            raise Exception("Already exists: %s" % (file_path))

    def download(self):
        out_dir = self.create_out_dir()
        if out_dir:
            self.log("Output dir: %s" % (out_dir))

        file_name = self.create_file_name(None)
        if file_name is not None:
            self.log("Output file: %s" % (file_name))
            self.assert_not_exists(os.path.join(out_dir, file_name))

        storage = self.fetch_storage(self.options.url[0])

        if file_name is None:
            file_name = self.create_file_name(storage)
            self.log("Output file: %s" % (file_name))

        token = self.fetch_token()

        url = self.create_download_url(storage, token)
        self.log("Download URL: %s" % (url), True)

        file_name_path = os.path.join(out_dir, file_name)
        self.assert_not_exists(file_name_path)

        file_name_temp = self.create_file_name_temp(storage)
        self.log("Temporary file: %s" % (file_name_temp), True)

        file_name_temp_path = os.path.join(out_dir, file_name_temp)

        # only if metadata flag
        if self.options.metadata:
            file_size = storage["size"]
            meta = {"file_name": file_name, "file_size": file_size, "download": url}
            print(json.dumps(meta))
            exit(0)

        # Download with progress info, adding new line to clear after.
        try:
            self.request_download(
                url, file_name_temp_path, self.download_progress, True
            )
        finally:
            self.log("")

        # Verify size.
        storage_size = storage["size"]
        self.log("Verifying size: %s" % (storage_size), True)
        try:
            self.download_verify_size(file_name_temp_path, storage_size)
        except Exception as ex:
            os.remove(file_name_temp_path)
            raise ex

        # Set the modified time if requested.
        if self.options.mtime:
            storage_mtime = storage["mtime"]
            self.log("Setting mtime: %s" % (storage_mtime), True)
            self.download_set_mtime(file_name_temp_path, storage_mtime)

        os.rename(file_name_temp_path, file_name_path)
        self.log("Done")

    def download_progress(self, status, start, now, offset, added, current, total):
        if status is self.DL_PROGRESS_READ:
            return

        if status is self.DL_PROGRESS_START:
            self.output_progress_start()
            return

        delta = now - start
        sub_total = total - offset
        sub_current = current - offset
        sub_remain = sub_total - sub_current
        bytes_sec = sub_current / float(delta) if delta else 0
        delta_remain = sub_remain / float(bytes_sec) if bytes_sec else 0

        timestr = self.seconds_human(math.floor(delta))
        percent = self.percent_human(current, total)
        amount = "%s (%s) / %s (%s)" % (
            self.bytes_human(current),
            current,
            self.bytes_human(total),
            total,
        )
        persec = "%s/s" % (self.bytes_human(round(bytes_sec)))
        timerem = self.seconds_human(math.ceil(delta_remain))

        self.output_progress("  ".join(["", timestr, percent, amount, persec, timerem]))

    def run(self):
        self.download()

    def main(self):
        def exception(ex):
            if self.options.debug:
                raise ex
            s = str(ex)
            if not s:
                s = ex.__class__.__name__
            self.output("Error: %s" % (s))
            return 1

        try:
            self.run()
        except Exception as ex:
            return exception(ex)
        except KeyboardInterrupt as ex:
            return exception(ex)
        return 0


def main():
    parser = argparse.ArgumentParser(
        prog=__prog__,
        description=os.linesep.join(
            ["%s %s" % (__prog__, __version__), "%s %s" % (__copyright__, __license__)]
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-v", "--version", action="version", version=__version__, help="Print version"
    )
    parser.add_argument("-V", "--verbose", action="store_true", help="Verbose mode")
    parser.add_argument("-D", "--debug", action="store_true", help="Debug output")
    parser.add_argument("-B", "--buffer", type=int, default=1024, help="Buffer size")
    parser.add_argument(
        "-t", "--timeout", type=int, default=60, help="Request timeout in seconds"
    )
    parser.add_argument(
        "-M", "--mtime", action="store_true", help="Use server modified time"
    )
    parser.add_argument("-d", "--dir", default=None, help="Output directory")
    parser.add_argument(
        "-s", "--metadata", action="store_true", help="show metadata only"
    )
    parser.add_argument("url", nargs=1, help="URL")
    parser.add_argument("file", nargs="?", default=None, help="FILE")
    options = parser.parse_args()
    return Main(options).main()


if __name__ == "__main__":
    sys.exit(main())
