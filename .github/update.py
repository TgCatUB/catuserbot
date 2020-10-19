import asyncio

from userbot import runcmd


async def update_requirements():
    try:
        await runcmd("pip install --upgrade pip")
        print("Pip is upto-date")
    except BaseException:
        print("Error while updating pip")
    try:
        await runcmd("pip install -r requirements.txt")
        print("Succesfully Updated requirements")
    except Exception as e:
        print(f"Error while installing requirments {str(e)}")


loop = asyncio.get_event_loop()
loop.run_until_complete(update_requirements())
loop.close()
