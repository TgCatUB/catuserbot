# Special Credits: @odi for Somnium <image gen>

import asyncio
import html
import re
import time
import urllib.parse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from somnium import Somnium

from ..core.managers import edit_delete, edit_or_reply
from ..helpers import reply_id
from ..sql_helper.globals import addgvar, gvarstatus
from . import catub, logging, mention

plugin_category = "tools"
LOGS = logging.getLogger(__name__)

_ASK_LOCK = asyncio.Lock()

_CHROME_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)


def _clean_ai_text(raw_text: str) -> str:
    """Extract and clean the Google AI Mode reply from page innerText."""
    if not raw_text:
        return ""

    start_match = re.search(r"AI Mode reply for [^\n]*\n", raw_text)
    text = raw_text[start_match.end():] if start_match else raw_text

    for stop_marker in (
        "\nAI can make mistakes",
        "\nAI Mode response is ready",
        "\nSkip to previous prompt",
    ):
        idx = text.find(stop_marker)
        if idx != -1:
            text = text[:idx]
            break

    text = re.sub(r"\s*\[Highlight (?:start|end)\]\s*", " ", text)
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)
    text = re.sub(r"\n(?:[^\n]{1,60}\n){1,2}[ \t\xa0]*\+\d+[ \t\xa0]*(?=\n|$)", "", text)
    text = re.sub(r"\n[ \t\xa0]*\+\d+[ \t\xa0]*(?=\n|$)", "", text)
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _fetch_google_ai(query: str) -> str:
    """Fetch an answer from Google AI Mode (google.com/ai) using headless Chrome."""
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-extensions")
    opts.add_argument("--disable-background-networking")
    opts.add_argument("--blink-settings=imagesEnabled=false")
    opts.add_argument("--window-size=1280,800")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument(f"user-agent={_CHROME_USER_AGENT}")

    url = f"https://www.google.com/search?udm=50&q={urllib.parse.quote_plus(query)}"
    driver = webdriver.Chrome(options=opts)
    try:
        driver.set_page_load_timeout(25)
        driver.get(url)

        deadline = time.time() + 25
        raw_text = ""
        while time.time() < deadline:
            cur_url = driver.current_url or ""
            if "/sorry/" in cur_url:
                raise RuntimeError("Google blocked the request with a CAPTCHA check.")

            raw_text = driver.execute_script(
                "return document.body ? document.body.innerText : \x27\x27;"
            )
            if (
                "AI Mode response is ready" in raw_text
                or "AI can make mistakes" in raw_text
            ) and "AI Mode reply for" in raw_text:
                break
            time.sleep(0.8)

        time.sleep(0.5)
        raw_text = driver.execute_script(
            "return document.body ? document.body.innerText : \x27\x27;"
        )
        return _clean_ai_text(raw_text)
    finally:
        driver.quit()


@catub.cat_cmd(
    pattern=r"genimg(?:\s|$)([\s\S]*)",
    command=("genimg", plugin_category),
    info={
        "header": "Create beautiful artwork using the power of AI.",
        "notes": "Best styles are V2s",
        "usage": [
            "{tr}genimg -l ( get list of artstyles )",
            "{tr}genimg -l <style-id> ( change the style )",
            "{tr}genimg <text> (generate)",
        ],
        "examples": [
            "{tr}genimg -l",
            "{tr}genimg -l 2000",
            "{tr}genimg Cat riding bike",
        ],
    },
)
async def gen_img(odi):
    "Generate an Image using the provided text with Somnium"
    reply_to_id = await reply_id(odi)
    query = odi.pattern_match.group(1)
    if not query:
        return await edit_delete(odi, "`What should I do ??`")

    catevent = await edit_or_reply(odi, "`Processing ...`")
    rstyles = {value: key for key, value in Somnium.Styles().items()}
    styleid = int(gvarstatus("DREAM_STYLE") or "2000")

    if query.startswith("-l"):
        query = query.replace("-l", "").strip()
        if query.isnumeric():
            if int(query) in rstyles:
                addgvar("DREAM_STYLE", int(query))
                return await edit_delete(catevent, f"`Style changed to {rstyles[int(query)]}.`")

            return await edit_delete(
                catevent,
                f"**Wrong style id.\n\n🎠 Here is list of:**  [styles]({Somnium.StylesGraph()}) ",
                link_preview=True,
                time=120,
            )

        return await edit_delete(
            catevent,
            f"**🎠 Here is list of:**  [styles]({Somnium.StylesGraph()}) ",
            link_preview=True,
            time=120,
        )
    await edit_or_reply(catevent, "`Generating ai image ...`")
    getart = await asyncio.to_thread(Somnium.Generate, query, styleid)
    if getart is None:
        return await edit_delete(catevent, "`Process failed or contains NSFW.`")
    await catub.send_file(
        odi.chat_id,
        getart,
        force_document=True,
        reply_to=reply_to_id,
        caption=f"**Query:** `{query}`\n**Style:** `{rstyles[styleid]}`\n\n__Generated by__ {mention}",
    )
    await catevent.delete()


@catub.cat_cmd(
    pattern=r"(?:gentxt|ask)(?:\s|$)([\s\S]*)",
    command=("gentxt", plugin_category),
    info={
        "header": "Generate AI response using Google AI Mode (google.com/ai).",
        "description": "Sends your question or prompt to Google AI Mode and posts the answer in chat.",
        "usage": [
            "{tr}gentxt <text / reply>",
            "{tr}ask <text / reply>",
        ],
        "examples": [
            "{tr}gentxt write a paragraph on cat",
            "{tr}ask why is navaratra celebrated",
        ],
    },
)
async def gen_txt(event):
    "Generate an AI response using Google AI Mode without any API key"
    query = event.pattern_match.group(1).strip()
    if not query:
        reply = await event.get_reply_message()
        if reply and reply.text:
            query = reply.text.strip()

    if not query:
        return await edit_delete(event, "`What should I do ??`")

    catevent = await edit_or_reply(event, f"🔍 **Asking Google AI:** `{query}`...")
    try:
        async with _ASK_LOCK:
            answer = await asyncio.to_thread(_fetch_google_ai, query)
    except Exception as exc:
        LOGS.exception("Error querying Google AI Mode")
        return await edit_delete(catevent, f"❌ **Google AI error:** `{exc}`", 10)

    if not answer:
        return await edit_delete(catevent, "`Sorry, unable to generate response`", 8)

    header = f"<b>Question:</b> {html.escape(query)}\n\n<b>Google AI:</b>\n"
    full_msg = header + html.escape(answer)

    if len(full_msg) < 4096:
        await edit_or_reply(catevent, full_msg, parse_mode="html", link_preview=False)
    else:
        await edit_or_reply(
            catevent,
            f"Question: {query}\n\nGoogle AI:\n{answer}",
            file_name="google_ai_answer.txt",
            noformat=True,
        )
