import os
import time
import urllib

import magic
import requests

from .. import LOGS



def googleimagesdownload( keywords, limit, extensions={".jpg", ".png", ".jpeg"}):
        LOGS.info("Searching..")
        keyword_to_search = [str(item).strip() for item in keywords.split(",")]
        main_directory = os.path.join("./", "temp")
        len(keyword_to_search) * limit

        for item_ in keyword_to_search:
            _create_directories(main_directory, item_)
            url = (
                (
                    "https://www.google.com/search?q="
                    + urllib.parse.quote(item_.encode("utf-8"))
                )
                + "&biw=1536&bih=674&tbm=isch&sxsrf=ACYBGNSXXpS6YmAKUiLKKBs6xWb4uUY5gA:1581168823770&source=lnms&sa=X&ved=0ahUKEwioj8jwiMLnAhW9AhAIHbXTBMMQ_AUI3QUoAQ"
            )

            raw_html = _download_page(url)

            end_object = -1
            google_image_seen = False
            j = 0
            while j < limit:
                while True:
                    try:
                        new_line = raw_html.find('"https://', end_object + 1)
                        end_object = raw_html.find('"', new_line + 1)

                        buffor = raw_html.find("\\", new_line + 1, end_object)
                        if buffor != -1:
                            object_raw = raw_html[new_line + 1 : buffor]
                        else:
                            object_raw = raw_html[new_line + 1 : end_object]

                        if any(extension in object_raw for extension in extensions):
                            break

                    except Exception:
                        break
                path = main_directory + item_.replace(" ", "_")

                try:
                    r = requests.get(object_raw, allow_redirects=True, timeout=1)
                    if "html" not in str(r.content):
                        mime = magic.Magic(mime=True)
                        file_type = mime.from_buffer(r.content)
                        file_extension = f'.{file_type.split("/")[1]}'
                        if file_extension not in extensions:
                            raise ValueError()
                        if file_extension == ".png" and not google_image_seen:
                            google_image_seen = True
                            raise ValueError()
                        file_name = str(item_) + "_" + str(j + 1) + file_extension
                        with open(os.path.join(path, file_name), "wb") as file:
                            file.write(r.content)
                    else:
                        j -= 1
                except Exception:
                    j -= 1
                j += 1
        LOGS.info("downloaded")

def _create_directories( main_directory, name):
        name = name.replace(" ", "_")
        try:
            if not os.path.exists(main_directory):
                os.makedirs(main_directory)
                time.sleep(0.2)
            path = name
            sub_directory = os.path.join(main_directory, path)
            if not os.path.exists(sub_directory):
                os.makedirs(sub_directory)
        except OSError as e:
            if e.errno != 17:
                raise
        return

def _download_page( url):

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
            }

            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            return str(resp.read())
        except Exception as e:
            print(e)
