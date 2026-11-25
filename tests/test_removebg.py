"""Offline contract and command tests: python -m unittest discover -s tests -v."""

import base64
import importlib.util
import json
import os
from pathlib import Path
import re
import runpy
import sys
import tempfile
import types
import unittest
from unittest.mock import AsyncMock, Mock, patch

import httpx


ROOT = Path(__file__).resolve().parents[1]
PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=")
API_URL = "https://cloud.leonardo.ai/api/rest/v2/generationssync"
IMAGE_URL = "https://images.example/cutout.png?signature=example"
SOURCE_URL = "https://images.example/source.jpg"


def load_plugin():
    """Import the real plugin without starting a Telegram session or database."""
    config = types.SimpleNamespace(LEONARDO_API_KEY="leonardo-test-key", REM_BG_API_KEY="legacy-test-key")
    modules = {name: types.ModuleType(name) for name in ("userbot", "userbot.plugins", "userbot.Config", "userbot.core", "userbot.core.managers", "userbot.helpers", "userbot.helpers.utils")}
    modules["userbot"].catub = types.SimpleNamespace(cat_cmd=lambda **kwargs: lambda function: function)
    modules["userbot"].Convert = types.SimpleNamespace(to_image=AsyncMock(), to_sticker=AsyncMock())
    modules["userbot.Config"].Config = config
    modules["userbot.core.managers"].edit_delete = AsyncMock()
    modules["userbot.core.managers"].edit_or_reply = AsyncMock()
    modules["userbot.helpers.utils"].reply_id = AsyncMock(return_value=42)
    spec = importlib.util.spec_from_file_location("userbot.plugins.removebg", ROOT / "userbot/plugins/removebg.py")
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, modules):
        spec.loader.exec_module(module)
    return module


class RemoveBgContractTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.plugin = load_plugin()
        self.requests = []
        self.api_response = httpx.Response(200, json={"results": [{"url": IMAGE_URL, "contentType": "image/png"}]})
        self.download_response = httpx.Response(200, content=PNG, headers={"content-type": "image/png"})
        self.client_type = httpx.AsyncClient

    def mock_client(self):
        def handle(request):
            self.requests.append(request)
            if request.method == "POST":
                self.assertEqual(str(request.url), API_URL)
                return self.api_response
            self.assertNotIn("authorization", request.headers)
            return self.download_response

        def factory(**kwargs):
            self.assertGreaterEqual(kwargs["timeout"], 30)
            return self.client_type(transport=httpx.MockTransport(handle), **kwargs)

        return patch.object(self.plugin.httpx, "AsyncClient", side_effect=factory)

    async def test_file_request_and_download(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "photo.png"
            path.write_bytes(PNG)
            with self.mock_client():
                response = await self.plugin.ReTrieveFile(path)
        payload = json.loads(self.requests[0].content)
        self.assertEqual(self.requests[0].headers["authorization"], "Bearer leonardo-test-key")
        self.assertEqual(self.requests[0].headers["content-type"], "application/json")
        self.assertEqual(payload["model"], "remove-bg")
        self.assertIs(payload["ephemeral"], True)
        self.assertNotIn("base64", payload)
        self.assertEqual(payload["parameters"]["format"], "png")
        image = payload["parameters"]["guidances"]["image_reference"]
        self.assertEqual(image, [{"image": {"type": "BASE64", "data": base64.b64encode(PNG).decode()}}])
        self.assertEqual(response.content, PNG)
        self.assertEqual(response.headers["content-type"], "image/png")
        self.assertEqual([r.method for r in self.requests], ["POST", "GET"])

    async def test_url_request(self):
        with self.mock_client():
            response = await self.plugin.ReTrieveURL(SOURCE_URL)
        image = json.loads(self.requests[0].content)["parameters"]["guidances"]["image_reference"]
        self.assertEqual(image, [{"image": {"type": "URL", "url": SOURCE_URL}}])
        self.assertEqual(response.content, PNG)

    async def test_url_whitespace_is_trimmed(self):
        with self.mock_client():
            await self.plugin.ReTrieveURL(f"  {SOURCE_URL}\n")
        image = json.loads(self.requests[0].content)["parameters"]["guidances"]["image_reference"][0]["image"]
        self.assertEqual(image["url"], SOURCE_URL)

    async def test_non_https_input_is_rejected_before_request(self):
        for url in ("http://images.example/source.jpg", "not a url", "https://"):
            with self.subTest(url=url), self.mock_client(), self.assertRaisesRegex(ValueError, "HTTPS"):
                await self.plugin.ReTrieveURL(url)
        self.assertEqual(self.requests, [])

    async def test_api_http_errors_do_not_download_results(self):
        for status in (401, 429, 500):
            with self.subTest(status=status):
                self.requests.clear()
                self.api_response = httpx.Response(status, json={"results": [{"url": IMAGE_URL}]})
                with self.mock_client():
                    response = await self.plugin.ReTrieveURL(SOURCE_URL)
                self.assertEqual(response.status_code, status)
                self.assertEqual(len(self.requests), 1)

    async def test_errors_take_precedence_over_results(self):
        self.api_response = httpx.Response(200, json={"errors": [{"message": "Insufficient credits"}], "results": [{"url": IMAGE_URL}]})
        with self.mock_client(), self.assertRaisesRegex(ValueError, "Insufficient credits"):
            await self.plugin.ReTrieveURL(SOURCE_URL)
        self.assertEqual(len(self.requests), 1)

    async def test_malformed_errors_are_reported(self):
        for errors in ("failed", [None], ["failed"], [{"message": {"unexpected": "object"}}]):
            with self.subTest(errors=errors):
                self.api_response = httpx.Response(200, json={"errors": errors})
                with self.mock_client(), self.assertRaises(ValueError):
                    await self.plugin.ReTrieveURL(SOURCE_URL)

    async def test_non_json_response_is_reported(self):
        self.api_response = httpx.Response(200, text="upstream unavailable", headers={"content-type": "image/png"})
        with self.mock_client(), self.assertRaisesRegex(ValueError, "JSON"):
            await self.plugin.ReTrieveURL(SOURCE_URL)

    async def test_non_object_json_is_reported(self):
        for data in ([], None, "unexpected", 7):
            with self.subTest(data=data):
                self.api_response = httpx.Response(200, json=data)
                with self.mock_client(), self.assertRaises(ValueError):
                    await self.plugin.ReTrieveURL(SOURCE_URL)

    async def test_empty_or_malformed_results_are_reported(self):
        for results in (None, [], {}, {"x": 1}, "unexpected", [None], ["unexpected"], [{}]):
            with self.subTest(results=results):
                self.api_response = httpx.Response(200, json={"results": results})
                with self.mock_client(), self.assertRaises(ValueError):
                    await self.plugin.ReTrieveURL(SOURCE_URL)

    async def test_invalid_download_urls_are_reported(self):
        for url in (None, 12, "", "http://images.example/result", "https://"):
            with self.subTest(url=url):
                self.api_response = httpx.Response(200, json={"results": [{"url": url}]})
                with self.mock_client(), self.assertRaises(ValueError):
                    await self.plugin.ReTrieveURL(SOURCE_URL)

    async def test_download_http_error_is_preserved(self):
        self.download_response = httpx.Response(403, content=b"expired", headers={"content-type": "image/png"})
        with self.mock_client():
            response = await self.plugin.ReTrieveURL(SOURCE_URL)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, b"expired")

    async def test_non_png_downloads_are_not_relabelled(self):
        for content in (b"<html>Storage error</html>", b"", b"not an image"):
            with self.subTest(content=content):
                self.download_response = httpx.Response(200, content=content)
                with self.mock_client(), self.assertRaisesRegex(ValueError, "PNG"):
                    await self.plugin.ReTrieveURL(SOURCE_URL)

    async def test_png_without_download_content_type_is_supported(self):
        self.download_response = httpx.Response(200, content=PNG)
        with self.mock_client():
            response = await self.plugin.ReTrieveURL(SOURCE_URL)
        self.assertEqual(response.content, PNG)
        self.assertEqual(response.headers["content-type"], "image/png")

    async def test_download_redirect_does_not_receive_api_key(self):
        def handle(request):
            self.requests.append(request)
            if request.method == "POST":
                return self.api_response
            self.assertNotIn("authorization", request.headers)
            if request.url.host == "images.example":
                return httpx.Response(302, headers={"location": "https://cdn.example/result.png"})
            return self.download_response

        with patch.object(self.plugin.httpx, "AsyncClient", side_effect=lambda **kwargs: self.client_type(transport=httpx.MockTransport(handle), **kwargs)):
            response = await self.plugin.ReTrieveURL(SOURCE_URL)
        self.assertEqual(response.content, PNG)
        self.assertEqual(len(self.requests), 3)


class RemoveBgCommandTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.plugin = load_plugin()
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        previous = Path.cwd()
        os.chdir(self.directory.name)
        self.addCleanup(os.chdir, previous)
        self.status = types.SimpleNamespace(delete=AsyncMock())
        self.plugin.edit_or_reply.return_value = self.status
        self.event = types.SimpleNamespace(reply_to_msg_id=None, pattern_match=re.match(r"(rmbg|srmbg) (.*)", f"rmbg {SOURCE_URL}"), client=types.SimpleNamespace(send_file=AsyncMock()), chat_id=123, get_reply_message=AsyncMock())
        self.plugin.ReTrieveURL = AsyncMock(return_value=httpx.Response(200, content=PNG, headers={"content-type": "image/png"}))
        self.plugin.ReTrieveFile = AsyncMock(return_value=self.plugin.ReTrieveURL.return_value)

    async def test_missing_or_blank_key_stops_before_request(self):
        for key in (None, "", "   "):
            with self.subTest(key=key):
                self.plugin.Config.LEONARDO_API_KEY = key
                await self.plugin.remove_background(self.event)
        self.plugin.ReTrieveURL.assert_not_awaited()
        self.assertIn("LEONARDO_API_KEY", self.plugin.edit_delete.call_args.args[1])
        self.assertIn("REM_BG_API_KEY", self.plugin.edit_delete.call_args.args[1])

    async def test_png_command_sends_document_and_cleans_output(self):
        sent = []

        async def send_file(chat_id, path, **kwargs):
            sent.append(Path(path))
            self.assertEqual(Path(path).read_bytes(), PNG)
            self.assertTrue(kwargs["force_document"])
            self.assertEqual(kwargs["reply_to"], 42)

        self.event.client.send_file.side_effect = send_file
        await self.plugin.remove_background(self.event)
        self.assertEqual(len(sent), 1)
        self.assertFalse(sent[0].exists())
        self.status.delete.assert_awaited_once()

    async def test_sticker_command_converts_and_sends(self):
        Path("temp").mkdir()
        self.event.pattern_match = re.match(r"(rmbg|srmbg) (.*)", f"srmbg {SOURCE_URL}")

        async def to_sticker(event, path, **kwargs):
            self.assertEqual(Path(path).read_bytes(), PNG)
            Path(path).unlink()
            sticker = Path("temp") / kwargs["file"]
            sticker.write_bytes(b"sticker")
            return event, str(sticker)

        self.plugin.Convert.to_sticker.side_effect = to_sticker
        await self.plugin.remove_background(self.event)
        self.event.client.send_file.assert_awaited_once()
        self.assertNotIn("force_document", self.event.client.send_file.call_args.kwargs)
        self.assertFalse(Path(self.event.client.send_file.call_args.args[1]).exists())

    async def test_download_timeout_is_reported(self):
        self.plugin.ReTrieveURL.side_effect = httpx.ReadTimeout("timeout")
        await self.plugin.remove_background(self.event)
        self.plugin.edit_delete.assert_awaited_once()
        self.event.client.send_file.assert_not_awaited()

    async def test_provider_error_is_escaped(self):
        self.plugin.ReTrieveURL.side_effect = ValueError("<b>Insufficient credits</b>")
        await self.plugin.remove_background(self.event)
        self.assertIn("&lt;b&gt;", self.plugin.edit_delete.call_args.args[1])
        self.assertEqual(self.plugin.edit_delete.call_args.kwargs["parse_mode"], "html")

    async def test_reply_input_is_deleted_on_network_error(self):
        Path("temp").mkdir()
        input_path = Path("temp/input.png")
        input_path.write_bytes(PNG)
        self.event.reply_to_msg_id = 42
        self.event.pattern_match = re.match(r"(rmbg|srmbg)(.*)", "rmbg")
        self.plugin.Convert.to_image.return_value = (self.event, str(input_path))
        self.plugin.ReTrieveFile.side_effect = httpx.ConnectError("offline")
        await self.plugin.remove_background(self.event)
        self.assertFalse(input_path.exists())
        self.plugin.edit_delete.assert_awaited_once()

    async def test_reply_input_is_deleted_on_success(self):
        Path("temp").mkdir()
        input_path = Path("temp/input.png")
        input_path.write_bytes(PNG)
        self.event.reply_to_msg_id = 42
        self.event.pattern_match = re.match(r"(rmbg|srmbg)(.*)", "rmbg")
        self.plugin.Convert.to_image.return_value = (self.event, str(input_path))
        await self.plugin.remove_background(self.event)
        self.assertFalse(input_path.exists())
        self.plugin.ReTrieveFile.assert_awaited_once_with(str(input_path))
        self.event.client.send_file.assert_awaited_once()

    async def test_error_without_content_type_or_utf8_is_reported(self):
        self.plugin.ReTrieveURL.return_value = httpx.Response(502, content=b"bad gateway\xff")
        await self.plugin.remove_background(self.event)
        self.plugin.edit_delete.assert_awaited_once()
        self.event.client.send_file.assert_not_awaited()

    async def test_image_content_type_on_http_error_is_rejected(self):
        self.plugin.ReTrieveURL.return_value = httpx.Response(500, content=PNG, headers={"content-type": "image/png"})
        await self.plugin.remove_background(self.event)
        self.plugin.edit_delete.assert_awaited_once()
        self.event.client.send_file.assert_not_awaited()

    async def test_large_http_error_is_bounded_and_escaped(self):
        self.plugin.ReTrieveURL.return_value = httpx.Response(500, text="<b>" + "x" * 10000)
        await self.plugin.remove_background(self.event)
        text = self.plugin.edit_delete.call_args.args[1]
        self.assertLess(len(text), 4096)
        self.assertIn("&lt;b&gt;", text)
        self.assertEqual(self.plugin.edit_delete.call_args.kwargs["parse_mode"], "html")

    async def test_missing_input_does_not_call_provider(self):
        self.event.pattern_match = re.match(r"(rmbg|srmbg)(.*)", "rmbg")
        await self.plugin.remove_background(self.event)
        self.plugin.edit_delete.assert_awaited_once()
        self.plugin.ReTrieveURL.assert_not_awaited()
        self.plugin.ReTrieveFile.assert_not_awaited()


class RemoveBgConfigTests(unittest.IsolatedAsyncioTestCase):
    async def test_new_and_legacy_keys_are_loaded_and_guarded(self):
        with patch.dict(os.environ, {"LEONARDO_API_KEY": "new-test-key", "REM_BG_API_KEY": "old-test-key"}, clear=True), patch("dotenv.load_dotenv"):
            config = runpy.run_path(str(ROOT / "userbot/Config/config.py"))["Config"]
        self.assertEqual(config.LEONARDO_API_KEY, "new-test-key")
        self.assertEqual(config.REM_BG_API_KEY, "old-test-key")
        config.STRING_SESSION = "session-test-value"
        config.API_HASH = "hash-test-value"
        config.TG_BOT_TOKEN = "telegram-test-value"
        modules = {name: types.ModuleType(name) for name in ("userbot", "userbot.Config", "userbot.core", "userbot.core.managers", "userbot.core.session", "userbot.sql_helper", "userbot.sql_helper.globals")}
        modules["userbot.Config"].Config = config
        modules["userbot.core.managers"].edit_or_reply = AsyncMock()
        modules["userbot.sql_helper.globals"].gvarstatus = Mock(return_value=None)
        modules["userbot.core.session"].catub = types.SimpleNamespace(uid=123, get_entity=AsyncMock(return_value=types.SimpleNamespace(phone="441234567890")))
        spec = importlib.util.spec_from_file_location("userbot.core.events", ROOT / "userbot/core/events.py")
        module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, modules):
            spec.loader.exec_module(module)
            self.assertTrue(await module.safe_check_text("key: new-test-key"))
            self.assertTrue(await module.safe_check_text("key: old-test-key"))
            self.assertFalse(await module.safe_check_text("normal message"))

    async def test_old_key_does_not_become_leonardo_credential(self):
        with patch.dict(os.environ, {"REM_BG_API_KEY": "old-test-key"}, clear=True), patch("dotenv.load_dotenv"):
            config = runpy.run_path(str(ROOT / "userbot/Config/config.py"))["Config"]
        self.assertIsNone(config.LEONARDO_API_KEY)


if __name__ == "__main__":
    unittest.main()
