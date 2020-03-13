#autobio for @PhycoNinja13b, Edit bio strings Amigo if u use this plugin, Or else u are cursed :)
import asyncio
import time
from telethon import events
import random, re
from telethon.tl import functions
from telethon.errors import FloodWaitError
from uniborg.util import admin_cmd


BIO_STRINGS = [
     "If I fall, don't bring me back.",
     "Loosing It All Now.",
     "If you desire something, just take it.",
     " 🌀Every flight begins with a fall.🌀",
     "People come and go in our lives, treasure the memory and moved on.",
     "Always positive",
     "In the world full of darkness be their reason to belive in goodness",
     "When u make a commitment, u build hope. When u keep it u build trust",
     "Everything suck,,,,,,see ya soon🚶🚶🚶🏇🤺🎅🕵️",
     "I have more money than you, stay broke. ",
     "Wise men listen and laugh, while fools talk.",
     "stop stalking me",
     "Fight your struggles🙄not me ",
     "...travel far enough, and you will meet yourself..",
     "Not in a Mood To write Bio",
     "Some duh ppl are tryna make fake IDs. Well, Bios r overrated lol",
     "Kill yourself Please ;D",
     "Fuck all hater's this is me",
     "Sometimes, you don’t get what you want, because you deserve better",
     "Loading..",
     "ERROR404 BIO NOT FOUND",
     "Once a wise man said 'FUCK OFF' :)",
     "Kindly..mind your own business..AMIGO",
     "Check your EGO, AMIGO :)",
     "No FUCKS Given",
     "Are u A Idiot",
     "Go get a job and stop reading my BIO",
     "Congratulations, I hate u",
     "Come closer, Let's die together :)",
     "Pain behind my Smile ",
     "Are u a magnet?, coz my steel body is getting attracted to u 🙃",
     "World is already full of MÀDAFÁKAŚ, so be unique ",
     "Once a dumb ass said 'Love is in the Air'",
     "I do whatever it takes",
     "I love how it feels when I break the chains",
     "Just Let me love you, when your heart is tired :)",
     "When u whisper, I'm Alright. But i see through ur white lies",
     "Nice to meet you, hope you are having a good day",
     "💮💮 Every lesson give a chance 💮💮",
     "I don't mind anything, as long as you are not serious about it",
     "Don't waste my time...",
     "Everything happens for a reason",
     "I will live as long as I live...!!!",
     "Another drop in the ocean that is humanity",
     "No matter what we go thru, i'll always be with you",
     "ᴛʜᴇʀᴇ  are ғᴇᴇʟɪɴɢs  I ɴᴇᴠᴇʀ  ᴡᴀɴɴᴀ ғᴇᴇʟ ᴀɢᴀɪɴ.",
     "I'm not alone, it's just me and your soul💖",
     "Stay with me, Don't leave please♡💔",
     "Drugs? no , thanks . I'm already addicted to someone!!",
     "we hide our true intentions",
     "we hide our pasts",
     "we hide our feelings",
     "We fake our smiles",
     "I have been sad for years.  Do not tell me it gets better",
     "You will never understand the hell I feel inside my head 😔💔",
     "I'm happy now because of you...stay here! Please don't leave me!",
     "I don't want Someone like you, I WANT YOU",
     "Stars can't shine without darkness. 🌃",
     "Some people pretend they’re strong, but they’re broken inside💔",
     "real heartbreak is when you forget what it's like to be loved.",
     "Everyone has things they can't say.",
     "find someone who makes you laugh while you're crying.💛",
     "I PREFER TO LOSE, BUT DO NOT BEG",
     "CHOOSE PEOPLE WHO TAKE A STAND FOR YOU",
     "Life is a song 🎼 Love is the lyrics"
]


DEL_TIME_OUT = 70


@borg.on(admin_cmd(pattern="autobio"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    while True:
        bro = random.randint(0, len(BIO_STRINGS) - 1)    
        #input_str = event.pattern_match.group(1)
        Bio = BIO_STRINGS[bro]
        DMY = time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M:%S")
        #bio = f"📅 {DMY} | ᗯᗩᏆᎢᏆᑎᏀ ᏞᏆᏦᗴ ᎢᏆᗰᗴ | ⌚️ {HM}"
        logger.info(Bio)
        try:
            await borg(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                about=Bio
            ))
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
        # else:
            # logger.info(r.stringify())
            # await borg.send_message(  # pylint:disable=E0602
            #     Config.PRIVATE_GROUP_BOT_API_ID,  # pylint:disable=E0602
            #     "Successfully Changed Profile Bio"
            # )
        await asyncio.sleep(DEL_TIME_OUT)
