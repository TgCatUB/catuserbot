import requests
import asyncio
from userbot.utils import parse_arguments, admin_cmd

"""Type 
`.docs <module name>`
It will search in the docs for for You.
"""

@borg.on(admin_cmd(pattern="docs (.*)"))
async def doc_search(e):
    params = e.pattern_match.group(1)
    args, lib = parse_arguments(params, ['version'])
    lib = lib.strip()

    version = int(args.get('version', 3))
    python_url = f"https://docs.python.org/{version}/library/{lib}.html"
    pip_url = f"https://pypi.org/project/{lib}/"

    await e.edit(f"Searching Docs For `{lib}`...")
    if requests.get(python_url).status_code == 200:
        response = f"[Python {version} Documentation for {lib}]({python_url})"
        await e.edit(response)
    elif requests.get(pip_url).status_code == 200:
        readthedocs_url = f"https://readthedocs.org/projects/{lib}/"
        if requests.get(readthedocs_url).status_code == 200:
            response = f"[Documentation for {lib} on Read The Docs]({readthedocs_url})"
            await e.edit(response)
    else:
        fak = await e.edit(f"No Docs Found for `{lib}`...")
        await asyncio.sleep(3)
        await fak.delete()

