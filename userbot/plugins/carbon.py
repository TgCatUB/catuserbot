import asyncio
import os
import random
from urllib.parse import quote_plus

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from . import catub, deEmojify

plugin_category = "utils"

CARBONLANG = "auto"


@catub.cat_cmd(
    pattern="carbon(?:\s|$)([\s\S]*)",
    command=("carbon", plugin_category),
    info={
        "header": "Carbon generators for given text (Fixed style)",
        "usage": [
            "{tr}carbon <text>",
            "{tr}carbon <reply to text>",
        ],
    },
)
async def carbon_api(event):
    """A Wrapper for carbon.now.sh"""
    await event.edit("`Processing..`")
    CARBON = "https://carbon.now.sh/?l={lang}&code={code}"
    textx = await event.get_reply_message()
    pcode = event.text
    if pcode[8:]:
        pcode = str(pcode[8:])
    elif textx:
        pcode = str(textx.message)
    else:
        return await edit_delete(
            event,
            "`No text is given. Either pass text along with cmd or reply to text`",
        )
    pcode = deEmojify(pcode)
    code = quote_plus(pcode)
    cat = await edit_or_reply(event, "`Carbonizing...\n25%`")
    url = CARBON.format(code=code, lang=CARBONLANG)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = Config.CHROME_BIN
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    prefs = {"download.default_directory": "./"}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(
        executable_path=Config.CHROME_DRIVER, options=chrome_options
    )
    driver.get(url)
    await edit_or_reply(cat, "`Be Patient...\n50%`")
    download_path = "./"
    driver.command_executor._commands["send_command"] = (
        "POST",
        "/session/$sessionId/chromium/send_command",
    )
    params = {
        "cmd": "Page.setDownloadBehavior",
        "params": {"behavior": "allow", "downloadPath": download_path},
    }
    driver.execute("send_command", params)
    driver.find_element("xpath", "//button[contains(text(),'Export')]").click()

    await edit_or_reply(cat, "`Processing..\n75%`")

    await asyncio.sleep(2)
    await edit_or_reply(cat, "`Done Dana Done...\n100%`")
    file = "./carbon.png"
    await edit_or_reply(cat, "`Uploading..`")
    await event.client.send_file(
        event.chat_id,
        file,
        caption="Here's your carbon",
        force_document=True,
        reply_to=event.message.reply_to_msg_id,
    )
    os.remove("./carbon.png")
    driver.quit()

    await cat.delete()


@catub.cat_cmd(
    pattern="kar1(?:\s|$)([\s\S]*)",
    command=("kar1", plugin_category),
    info={
        "header": "Carbon generators for given text (Fixed style)",
        "usage": [
            "{tr}kar1 <text>",
            "{tr}kar1 <reply to text>",
        ],
    },
)
async def kar1_api(event):
    """A Wrapper for carbon.now.sh"""
    cat = await edit_or_reply(event, "🔲🔲🔲🔲🔲")
    CARBON = "https://carbon.now.sh/?bg=rgba(249%2C237%2C212%2C0)&t=synthwave-84&wt=none&l=application%2Fjson&ds=true&dsyoff=20px&dsblur=0px&wc=true&wa=true&pv=56px&ph=0px&ln=false&fl=1&fm=IBM%20Plex%20Mono&fs=14.5px&lh=153%25&si=false&es=4x&wm=false&code={code}"
    textx = await event.get_reply_message()
    pcode = event.text
    if pcode[6:]:
        pcode = str(pcode[6:])
    elif textx:
        pcode = str(textx.message)
    else:
        return await edit_delete(
            cat, "`No text is given. Either pass text along with cmd or reply to text`"
        )
    code = quote_plus(pcode)
    url = CARBON.format(code=code, lang=CARBONLANG)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = Config.CHROME_BIN
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    prefs = {"download.default_directory": "./"}
    chrome_options.add_experimental_option("prefs", prefs)
    await edit_or_reply(cat, "🔳🔳🔲🔲🔲")

    driver = webdriver.Chrome(
        executable_path=Config.CHROME_DRIVER, options=chrome_options
    )
    driver.get(url)
    download_path = "./"
    driver.command_executor._commands["send_command"] = (
        "POST",
        "/session/$sessionId/chromium/send_command",
    )
    params = {
        "cmd": "Page.setDownloadBehavior",
        "params": {"behavior": "allow", "downloadPath": download_path},
    }
    driver.execute("send_command", params)

    driver.find_element("xpath", "//button[contains(text(),'Export')]").click()
    await asyncio.sleep(1)
    await edit_or_reply(cat, "🔳🔳🔳🔲🔲")
    await asyncio.sleep(1)
    await edit_or_reply(cat, "🔳🔳🔳🔳🔳")
    file = "./carbon.png"
    await edit_or_reply(cat, "☣️Karbon1 Completed, Uploading Karbon☣️")
    await event.client.send_file(
        event.chat_id,
        file,
        force_document=True,
        reply_to=event.message.reply_to_msg_id,
    )
    os.remove("./carbon.png")

    await cat.delete()


@catub.cat_cmd(
    pattern="kar2(?:\s|$)([\s\S]*)",
    command=("kar2", plugin_category),
    info={
        "header": "Carbon generators for given text (Fixed style)",
        "usage": [
            "{tr}kar2 <text>",
            "{tr}kar2 <reply to text>",
        ],
    },
)
async def kar2_api(event):
    """A Wrapper for carbon.now.sh"""
    cat = await edit_or_reply(event, "📛📛📛📛📛")
    CARBON = "https://carbon.now.sh/?bg=rgba(239%2C40%2C44%2C1)&t=one-light&wt=none&l=application%2Ftypescript&ds=true&dsyoff=20px&dsblur=68px&wc=true&wa=true&pv=56px&ph=56px&ln=false&fl=1&fm=Hack&fs=14px&lh=143%25&si=false&es=2x&wm=false&code={code}"
    textx = await event.get_reply_message()
    pcode = event.text
    if pcode[6:]:
        pcode = str(pcode[6:])
    elif textx:
        pcode = str(textx.message)
    else:
        return await edit_delete(
            cat, "`No text is given. Either pass text along with cmd or reply to text`"
        )
    code = quote_plus(pcode)
    url = CARBON.format(code=code, lang=CARBONLANG)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = Config.CHROME_BIN
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    prefs = {"download.default_directory": "./"}
    chrome_options.add_experimental_option("prefs", prefs)
    await edit_or_reply(cat, "🔘🔘📛📛📛")
    driver = webdriver.Chrome(
        executable_path=Config.CHROME_DRIVER, options=chrome_options
    )
    driver.get(url)
    download_path = "./"
    driver.command_executor._commands["send_command"] = (
        "POST",
        "/session/$sessionId/chromium/send_command",
    )
    params = {
        "cmd": "Page.setDownloadBehavior",
        "params": {"behavior": "allow", "downloadPath": download_path},
    }
    driver.execute("send_command", params)
    driver.find_element("xpath", "//button[contains(text(),'Export')]").click()
    await asyncio.sleep(1)
    await edit_or_reply(cat, "🔘🔘🔘📛📛")
    await asyncio.sleep(1)
    await edit_or_reply(cat, "🔘🔘🔘🔘🔘")
    file = "./carbon.png"
    await edit_or_reply(cat, "☣️Karbon2 Completed, Uploading Karbon☣️")
    await event.client.send_file(
        event.chat_id,
        file,
        caption="Here's your Karbon2",
        force_document=True,
        reply_to=event.message.reply_to_msg_id,
    )

    os.remove("./carbon.png")

    await cat.delete()


@catub.cat_cmd(
    pattern="kar3(?:\s|$)([\s\S]*)",
    command=("kar3", plugin_category),
    info={
        "header": "Carbon generators for given text (Fixed style)",
        "usage": [
            "{tr}kar3 <text>",
            "{tr}kar3 <reply to text>",
        ],
    },
)
async def kar3_api(event):
    """A Wrapper for carbon.now.sh"""
    cat = await edit_or_reply(event, "🎛🎛🎛🎛🎛")
    CARBON = "https://carbon.now.sh/?bg=rgba(74%2C144%2C226%2C1)&t=material&wt=none&l=auto&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=true&pv=56px&ph=56px&ln=false&fl=1&fm=Fira%20Code&fs=14px&lh=152%25&si=false&es=2x&wm=false&code={code}"
    textx = await event.get_reply_message()
    pcode = event.text
    if pcode[6:]:
        pcode = str(pcode[6:])
    elif textx:
        pcode = str(textx.message)
    else:
        return await edit_delete(
            cat, "`No text is given. Either pass text along with cmd or reply to text`"
        )
    code = quote_plus(pcode)
    url = CARBON.format(code=code, lang=CARBONLANG)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = Config.CHROME_BIN
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    prefs = {"download.default_directory": "./"}
    chrome_options.add_experimental_option("prefs", prefs)
    await edit_or_reply(cat, "🔵🔵🎛🎛🎛")

    driver = webdriver.Chrome(
        executable_path=Config.CHROME_DRIVER, options=chrome_options
    )
    driver.get(url)
    download_path = "./"
    driver.command_executor._commands["send_command"] = (
        "POST",
        "/session/$sessionId/chromium/send_command",
    )
    params = {
        "cmd": "Page.setDownloadBehavior",
        "params": {"behavior": "allow", "downloadPath": download_path},
    }
    driver.execute("send_command", params)

    driver.find_element("xpath", "//button[contains(text(),'Export')]").click()
    await asyncio.sleep(1)
    await edit_or_reply(cat, "🔵🔵🔵🎛🎛")
    await asyncio.sleep(1)
    await edit_or_reply(cat, "🔵🔵🔵🔵🔵")
    file = "./carbon.png"
    await edit_or_reply(cat, "☣️Karbon3 Completed, Uploading Karbon⬆️")
    await event.client.send_file(
        event.chat_id,
        file,
        caption="Here's your Karbon3",
        force_document=True,
        reply_to=event.message.reply_to_msg_id,
    )

    os.remove("./carbon.png")
    await cat.delete()


@catub.cat_cmd(
    pattern="kar4(?:\s|$)([\s\S]*)",
    command=("kar4", plugin_category),
    info={
        "header": "Carbon generators for given text (Fixed style)",
        "usage": [
            "{tr}kar4 <text>",
            "{tr}kar4 <reply to text>",
        ],
    },
)
async def kar4_api(event):
    """A Wrapper for carbon.now.sh"""
    cat = await edit_or_reply(event, "🌚🌚🌚🌚🌚")
    CARBON = "https://carbon.now.sh/?bg=rgba(29%2C40%2C104%2C1)&t=one-light&wt=none&l=application%2Ftypescript&ds=true&dsyoff=20px&dsblur=68px&wc=true&wa=true&pv=56px&ph=56px&ln=false&fl=1&fm=Hack&fs=14px&lh=143%25&si=false&es=2x&wm=false&code={code}"
    textx = await event.get_reply_message()
    pcode = event.text
    if pcode[6:]:
        pcode = str(pcode[6:])
    elif textx:
        pcode = str(textx.message)
    else:
        return await edit_delete(
            cat, "`No text is given. Either pass text along with cmd or reply to text`"
        )
    code = quote_plus(pcode)
    url = CARBON.format(code=code, lang=CARBONLANG)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = Config.CHROME_BIN
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    prefs = {"download.default_directory": "./"}
    chrome_options.add_experimental_option("prefs", prefs)
    await edit_or_reply(cat, "🌝🌝🌚🌚🌚")
    driver = webdriver.Chrome(
        executable_path=Config.CHROME_DRIVER, options=chrome_options
    )
    driver.get(url)
    download_path = "./"
    driver.command_executor._commands["send_command"] = (
        "POST",
        "/session/$sessionId/chromium/send_command",
    )
    params = {
        "cmd": "Page.setDownloadBehavior",
        "params": {"behavior": "allow", "downloadPath": download_path},
    }
    driver.execute("send_command", params)
    driver.find_element("xpath", "//button[contains(text(),'Export')]").click()
    await asyncio.sleep(1)
    await edit_or_reply(cat, "🌝🌝🌝🌚🌚")
    await asyncio.sleep(1)
    await edit_or_reply(cat, "🌝🌝🌝🌝🌝")
    file = "./carbon.png"
    await edit_or_reply(cat, "✅Karbon4 Completed, Uploading Karbon✅")
    await event.client.send_file(
        event.chat_id,
        file,
        caption="Here's your Karbon4 ",
        force_document=True,
        reply_to=event.message.reply_to_msg_id,
    )

    os.remove("./carbon.png")
    await cat.delete()


@catub.cat_cmd(
    pattern="kargb(?:\s|$)([\s\S]*)",
    command=("kargb", plugin_category),
    info={
        "header": "Carbon generators for given text (random from some selected themes)",
        "usage": [
            "{tr}kargb <text>",
            "{tr}kargb <reply to text>",
        ],
    },
)
async def kargb_api(event):
    """A Wrapper for carbon.now.sh"""
    RED = random.randint(0, 256)
    GREEN = random.randint(0, 256)
    BLUE = random.randint(0, 256)
    THEME = [
        "3024-night",
        "a11y-dark",
        "blackboard",
        "base16-dark",
        "base16-light",
        "cobalt",
        "dracula",
        "duotone-dark",
        "hopscotch",
        "lucario",
        "material",
        "monokai",
        "night-owl",
        "nord",
        "oceanic-next",
        "one-light",
        "one-dark",
        "panda-syntax",
        "paraiso-dark",
        "seti",
        "shades-of-purple",
        "solarized",
        "solarized%20light",
        "synthwave-84",
        "twilight",
        "verminal",
        "vscode",
        "yeti",
        "zenburn",
    ]
    CUNTHE = random.randint(0, len(THEME) - 1)
    The = THEME[CUNTHE]
    cat = await edit_or_reply(event, "⬜⬜⬜⬜⬜")
    CARBON = "https://carbon.now.sh/?bg=rgba({R}%2C{G}%2C{B}%2C1)&t={T}&wt=none&l=auto&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=true&pv=56px&ph=56px&ln=false&fl=1&fm=Fira%20Code&fs=14px&lh=152%25&si=false&es=2x&wm=false&code={code}"
    textx = await event.get_reply_message()
    pcode = event.text
    if pcode[7:]:
        pcode = str(pcode[7:])
    elif textx:
        pcode = str(textx.message)
    else:
        return await edit_delete(
            cat, "`No text is given. Either pass text along with cmd or reply to text`"
        )
    code = quote_plus(pcode)
    url = CARBON.format(code=code, R=RED, G=GREEN, B=BLUE, T=The, lang=CARBONLANG)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = Config.CHROME_BIN
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    prefs = {"download.default_directory": "./"}
    chrome_options.add_experimental_option("prefs", prefs)
    await edit_or_reply(cat, "⬛⬛⬜⬜⬜")
    driver = webdriver.Chrome(
        executable_path=Config.CHROME_DRIVER, options=chrome_options
    )
    driver.get(url)
    download_path = "./"
    driver.command_executor._commands["send_command"] = (
        "POST",
        "/session/$sessionId/chromium/send_command",
    )
    params = {
        "cmd": "Page.setDownloadBehavior",
        "params": {"behavior": "allow", "downloadPath": download_path},
    }
    driver.execute("send_command", params)
    driver.find_element("xpath", "//button[contains(text(),'Export')]").click()
    await asyncio.sleep(1)
    await edit_or_reply(cat, "⬛⬛⬛⬜⬜")
    await asyncio.sleep(1)
    await edit_or_reply(cat, "⬛⬛⬛⬛⬛")
    file = "./carbon.png"
    await edit_or_reply(cat, "✅RGB Karbon Completed, Uploading Karbon✅")
    await event.client.send_file(
        event.chat_id,
        file,
        caption="Here's your karbonrgb",
        force_document=True,
        reply_to=event.message.reply_to_msg_id,
    )

    os.remove("./carbon.png")
    await cat.delete()
