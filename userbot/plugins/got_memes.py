# BY @Deonnn
"""
Game of Thrones Dialogues That You Can Use In Everyday Situations
 command .gotm
 by @Deonnn

Game of Thrones Thoughts plugin
by @Deonnn
command .gott
"""

import asyncio
import random

from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern=f"gott$", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Typing...")
    await asyncio.sleep(2)
    x = random.randrange(1, 40)
    if x == 1:
        await event.edit('`"The man who passes the sentence should swing the sword."`')
    if x == 2:
        await event.edit(
            '`"When the snows fall and the white winds blow, the lone wolf dies but the pack survives!"`'
        )
    if x == 3:
        await event.edit('`"The things I do for love!"`')
    if x == 4:
        await event.edit(
            '`"I have a tender spot in my heart for cripples, bastards and broken things."`'
        )
    if x == 5:
        await event.edit(
            '`"Death is so terribly final, while life is full of possibilities."`'
        )
    if x == 6:
        await event.edit(
            '`"Once you’ve accepted your flaws, no one can use them against you."`'
        )
    if x == 7:
        await event.edit('`"If I look back I am lost."`')
    if x == 8:
        await event.edit('`"When you play the game of thrones, you win or you die."`')
    if x == 9:
        await event.edit(
            '`"I grew up with soldiers. I learned how to die a long time ago."`'
        )
    if x == 10:
        await event.edit('`"What do we say to the Lord of Death?\nNot Today!"`')
    if x == 11:
        await event.edit('`"Every flight begins with a fall."`')
    if x == 12:
        await event.edit('`"Different roads sometimes lead to the same castle."`')
    if x == 13:
        await event.edit(
            '`"Never forget what you are. The rest of the world will not. Wear it like armour, and it can never be used to hurt you."`'
        )
    if x == 14:
        await event.edit(
            '`"The day will come when you think you are safe and happy, and your joy will turn to ashes in your mouth."`'
        )
    if x == 15:
        await event.edit('`"The night is dark and full of terrors."`')
    if x == 16:
        await event.edit('`"You know nothing, Jon Snow."`')
    if x == 17:
        await event.edit('`"Night gathers, and now my watch begins!"`')
    if x == 18:
        await event.edit('`"A Lannister always pays his debts."`')
    if x == 19:
        await event.edit('`"Burn them all!"`')
    if x == 20:
        await event.edit('`"What do we say to the God of death?"`')
    if x == 21:
        await event.edit('`"There\'s no cure for being a c*nt."`')
    if x == 22:
        await event.edit('`"Winter is coming!"`')
    if x == 23:
        await event.edit('`"That\'s what I do: I drink and I know things."`')
    if x == 24:
        await event.edit(
            '`"I am the dragon\'s daughter, and I swear to you that those who would harm you will die screaming."`'
        )
    if x == 25:
        await event.edit(
            '`"A lion does not concern himself with the opinion of sheep."`'
        )
    if x == 26:
        await event.edit('`"Chaos isn\'t a pit. Chaos is a ladder."`')
    if x == 27:
        await event.edit(
            '`"I understand that if any more words come pouring out your c*nt mouth, I\'m gonna have to eat every f*cking chicken in this room."`'
        )
    if x == 28:
        await event.edit(
            '`"If you think this has a happy ending, you haven\'t been paying attention."`'
        )
    if x == 29:
        await event.edit(
            '`"If you ever call me sister again, I\'ll have you strangled in your sleep."`'
        )
    if x == 30:
        await event.edit('`"A girl is Arya Stark of Winterfell. And I\'m going home."`')
    if x == 31:
        await event.edit("`\"Any man who must say 'I am the King' is no true King.\"`")
    if x == 32:
        await event.edit('`"If I fall, don\'t bring me back."`')
    if x == 33:
        await event.edit(
            "`\"Lannister, Targaryen, Baratheon, Stark, Tyrell... they're all just spokes on a wheel. This one's on top, then that one's on top, and on and on it spins, crushing those on the ground.\"`"
        )
    if x == 34:
        await event.edit('`"Hold the door!`')
    if x == 35:
        await event.edit(
            '`"When people ask you what happened here, tell them the North remembers. Tell them winter came for House Frey."`'
        )
    if x == 36:
        await event.edit('`"Nothing f*cks you harder than time."`')
    if x == 37:
        await event.edit(
            '`"There is only one war that matters. The Great War. And it is here."`'
        )
    if x == 38:
        await event.edit('`"Power is power!"`')
    if x == 39:
        await event.edit('`"I demand a trial by combat!"`')
    if x == 40:
        await event.edit('`"I wish I was the monster you think I am!"`')
    if x == 41:
        await event.edit(
            "Never forget what you are. The rest of the world will not.Wear it like armor,\n and it can never be used to hurt you."
        )
    if x == 42:
        await event.edit("There is only one thing we say to death: **Not today.**")
    if x == 43:
        await event.edit(
            "If you think this has a happy ending, you haven’t been **paying attention**."
        )
    if x == 44:
        await event.edit("Chaos isn’t a pit. Chaos is a ladder.")
    if x == 45:
        await event.edit("You know nothing, **Jon Snow**")
    if x == 46:
        await event.edit("**Winter** is coming.")
    if x == 47:
        await event.edit("When you play the **game of thrones**, you win or you die.")
    if x == 48:
        await event.edit(
            "I'm not going to **stop** the wheel, I'm going to **break** the wheel."
        )
    if x == 49:
        await event.edit(
            "When people ask you what happened here, tell them the **North remembers**. Tell them winter came for **House Frey**."
        )
    if x == 50:
        await event.edit(
            "When the snows fall and the white winds blow,\n the lone wolf dies, but the pack **survives**."
        )


@borg.on(admin_cmd(pattern=f"gotm$", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Thinking... 🤔")
    await asyncio.sleep(2)
    x = random.randrange(1, 30)
    if x == 1:
        await event.edit(
            "[To your teachers on failing you in all your papers confidently, every time...](https://telegra.ph/file/431d178780f9bff353047.jpg)",
            link_preview=True,
        )
    if x == 2:
        await event.edit(
            "[A shift from the mainstream darling, sweetheart, jaanu, and what not...](https://telegra.ph/file/6bbb86a6c7d2c4a61e102.jpg)",
            link_preview=True,
        )
    if x == 3:
        await event.edit(
            "[To the guy who's friendzone-ing you...](https://telegra.ph/file/8930b05e9535e9b9b8229.jpg)",
            link_preview=True,
        )
    if x == 4:
        await event.edit(
            "[When your friend asks for his money back...](https://telegra.ph/file/2df575ab38df5ce9dbf5e.jpg)",
            link_preview=True,
        )
    if x == 5:
        await event.edit(
            "[A bad-ass reply to who do you think you are?](https://telegra.ph/file/3a35a0c37f4418da9f702.jpg)",
            link_preview=True,
        )
    if x == 6:
        await event.edit(
            "[When the traffic police stops your car and asks for documents...](https://telegra.ph/file/52612d58d6a61315a4c3a.jpg)",
            link_preview=True,
        )
    if x == 7:
        await event.edit(
            "[ When your friend asks about the food he/she just cooked and you don't want to break his/her heart...](https://telegra.ph/file/702df36088f5c26fef931.jpg)",
            link_preview=True,
        )
    if x == 8:
        await event.edit(
            "[When you're out of words...](https://telegra.ph/file/ba748a74bcab4a1135d2a.jpg)",
            link_preview=True,
        )
    if x == 9:
        await event.edit(
            "[When you realize your wallet is empty...](https://telegra.ph/file/a4508324b496d3d4580df.jpg)",
            link_preview=True,
        )
    if x == 10:
        await event.edit(
            "[When shit is about to happen...](https://telegra.ph/file/e15d9d64f9f25e8d05f19.jpg)",
            link_preview=True,
        )
    if x == 11:
        await event.edit(
            "[When that oversmart classmate shouts a wrong answer in class...](https://telegra.ph/file/1a225a2e4b7bfd7f7a809.jpg)",
            link_preview=True,
        )
    if x == 12:
        await event.edit(
            "[When things go wrong in a big fat Indian wedding...](https://telegra.ph/file/db69e17e85bb444caca32.jpg)",
            link_preview=True,
        )
    if x == 13:
        await event.edit(
            "[A perfect justification for breaking a promise...](https://telegra.ph/file/0b8fb8fb729d157844ac9.jpg)",
            link_preview=True,
        )
    if x == 14:
        await event.edit(
            "[When your friend just won't stop LOL-ing on something silly you said...](https://telegra.ph/file/247fa54106c32318797ae.jpg)",
            link_preview=True,
        )
    if x == 15:
        await event.edit(
            "[When someone makes a joke on you...](https://telegra.ph/file/2ee216651443524eaafcf.jpg)",
            link_preview=True,
        )
    if x == 16:
        await event.edit(
            "[When your professor insults you in front of the class...](https://telegra.ph/file/a2dc7317627e514a8e180.jpg)",
            link_preview=True,
        )
    if x == 17:
        await event.edit(
            "[When your job interviewer asks if you're nervous...](https://telegra.ph/file/9cc147d0bf8adbebf164b.jpg)",
            link_preview=True,
        )
    if x == 18:
        await event.edit(
            "[When you're sick of someone complaining about the heat outside...](https://telegra.ph/file/9248635263c52b968f968.jpg)",
            link_preview=True,
        )
    if x == 19:
        await event.edit(
            "[When your adda is occupied by outsiders...](https://telegra.ph/file/ef537007ba6d9d4cbd384.jpg)",
            link_preview=True,
        )
    if x == 20:
        await event.edit(
            "[When you don't have the right words to motivate somebody...](https://telegra.ph/file/2c932d769ae4c5fbed368.jpg)",
            link_preview=True,
        )
    if x == 21:
        await event.edit(
            "[When the bouncer won't let you and your group of friends in because you're all under-aged...](https://telegra.ph/file/6c8ca79f1e20ebd04391c.jpg)",
            link_preview=True,
        )
    if x == 22:
        await event.edit(
            "[To the friend who wants you to take the fall for his actions...](https://telegra.ph/file/d4171b9bc9104b5d972d9.jpg)",
            link_preview=True,
        )
    if x == 23:
        await event.edit(
            "[When that prick of a bully wouldn't take your words seriously...](https://telegra.ph/file/188d73bd24cf866d8d8d0.jpg)",
            link_preview=True,
        )
    if x == 24:
        await event.edit(
            "[ When you're forced to go shopping/watch a football match with your partner...](https://telegra.ph/file/6e129f138c99c1886cb2b.jpg)",
            link_preview=True,
        )
    if x == 25:
        await event.edit(
            "[To the large queue behind you after you get the last concert/movie ticket...](https://telegra.ph/file/2423f213dd4e4282a31ea.jpg)",
            link_preview=True,
        )
    if x == 26:
        await event.edit(
            "[When your parents thought you'd fail but you prove them wrong...](https://telegra.ph/file/39cc5098466f622bf21e3.jpg)",
            link_preview=True,
        )
    if x == 27:
        await event.edit(
            "[A justification for not voting!](https://telegra.ph/file/87d475a8f9a8350d2450e.jpg)",
            link_preview=True,
        )
    if x == 28:
        await event.edit(
            "[When your partner expects you to do too many things...](https://telegra.ph/file/68bc768d36e08862bf94e.jpg)",
            link_preview=True,
        )
    if x == 29:
        await event.edit(
            "[When your friends cancel on the plan you made at the last minute...](https://telegra.ph/file/960b58c8f625b17613307.jpg)",
            link_preview=True,
        )
    if x == 30:
        await event.edit(
            "[For that friend of yours who does not like loud music and head banging...](https://telegra.ph/file/acbce070d3c52b921b2bd.jpg)",
            link_preview=True,
        )
