"""
Life Pro Tips
  Syntax: .tip
by
  @Deonnn

"""
from telethon import events

import asyncio

import os

import sys

import random



from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern=f"tip", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Well, let me give you a life-pro tip... 😉")
    await asyncio.sleep(2)
    x=(random.randrange(1,87))
    if x==1:
        await event.edit("`\"Before telling your landlord you're moving, ask them to fix anything broken that you're worried you might get charged for. They often will, and then when you move out they won't be able to take it out of your security deposit.\"`")
    if x==2:
        await event.edit("`\"Walking before solving a problem improves your creativity by an average of 60%.\"`")
    if x==3:

        await event.edit("`\"Wake up a little earlier than your alarm? Don’t go back to bed and wait for your alarm. Waking up naturally instead of to some sort of stimuli will help you get off to a better and healthier start to your day.\"`")

    if x==4:

        await event.edit("`\"Act like your future self is a real person. So when you see a chore that needs to be done, you can say \"I'll do this now to be nice to my future self\". Helps motivate to get things done because you're doing work for someone you want to help.\"`")

    if x==5:

        await event.edit("`\"Think of purchases as a percentage of your budget/account balance rather than their actual cost.\"`")

    if x==6:

        await event.edit("`\"Counting on fingers is a vital part of learning math, and children that do it from an early age develop much better math skills than those who have been told not to.\"`")

    if x==7:

        await event.edit("`\"There are just some things in life you can’t control or you’ll never know the real reason why. The only thing you can do is accept it and move on. Part of happiness is accepting the past happened or being proud of it.\"`")

    if x==8:

        await event.edit("`\"Make a recording of your voice with a sweet message or telling a story. If anything happens to you, your loved ones will greatly appreciate being able to listen to your voice again.\"`")

    if x==9:

        await event.edit("`\"If someone is treating you to a meal and you're wondering how much you should spend, ask them what they're ordering to get a better idea of the range.\"`")

    if x==10:

        await event.edit("`\"Never leave water bottles, reading glasses, or anything else that can focus light in a spot that could get direct sunlight. A significant number of house/vehicle fires happen every year because of this.\"`")

    if x==11:

        await event.edit("`\"If you reach out to someone for help on a technical issue and they spend their valuable time helping you but are unable to resolve it, always try and let them know how it got resolved so they can help the next person with the same issue.\"`")

    if x==12:

        await event.edit("`\"If you find information on the internet that you may need again in the future, print the page to a PDF digital file. There is no guarantee that the page will be available again in the future, and now you will have a digital copy for future reference.\"`")

    if x==13:

        await event.edit("`\"If you want to learn another language, watch children’s shows in that language to pick up on it quicker.\"`")

    if x==14:

        await event.edit("`\"If you want to separate some pdf pages without using any new software. you can open the pdf file in chrome then click on print then select custom pages option, and finally choose to save as pdf.\"`")

    if x==15:

        await event.edit("`\"If you’re ever in the heat of an argument, always act like you’re being recorded. This helps you from saying things you don’t mean and could regret later.\"`")

    if x==16:

        await event.edit("`\"Make music playlists during times in your life when good things are happening and you are experiencing good feelings. Then when you're down later in life listen to those playlists to instantly feel better, and feel those good emotions again.\"`")

    if x==17:

        await event.edit("`\"When going on a first date, think in terms of \"will I like them?\" instead of \"will they like me?\"\"`")

    if x==18:

        await event.edit("`\"When researching things to do for your next leisure travel. Include \<location\> tourism scam into your search. All tourist heavy areas will have their own scams. This should not dampen your excitement but heighten your knowledge so your vacation will be more enjoyable.\"`")

    if x==19:

        await event.edit("`\"Just because you’ve know that person for years doesn’t mean you should stay friends with them. A toxic friend need to be cut out of your life.\"`")

    if x==20:

        await event.edit("`\"Tired of all the ads in one of the free (offline) game apps you’re playing? Go to your settings and turn off the apps access to cellular data. Enjoy the ad free game play!\"`")

    if x==21:

        await event.edit("`\"Treat your monthly savings goal like a bill. At the end of the month, hold yourself accountable to \“pay it off\” like you would your rent or your utilities. This will keep you on track for your savings goals.\"`")
    
    if x==22:

        await event.edit("`\"If you need to wait until your boss is in a good mood to ask for something as simple as time off, you're in a toxic work environment and you need to take steps to exit sooner than later.\"`")
    
    if x==23:

        await event.edit("`\"When debating someone on a heated issue, start by looking for something to agree with them on. The rest of the conversation will be a lot less hostile if you establish common ground.\"`")
    
    if x==24:

        await event.edit("`\"Record random conversations with your parents and grandparents. Someday hearing their voice may be priceless to you.\"`")
    
    if x==25:

        await event.edit("`\"If you're a student planning on your career, look up postings of your dream job, find the skills and qualifications you'll need, then work backwards from there.\"`")
    
    if x==26:

        await event.edit("`\"If someone asks how your weekend was, assume they're really wanting to tell you about theirs. Keep your answer short and enthusiastically ask about theirs. It'll make their day.\"`")
    
    if x==27:

        await event.edit("`\"When traveling with a friend or family member, don’t be afraid to suggest breaking off to each do your own things for a day. Going solo can be enjoyable (eat/go wherever want at your own pace), plus it reduces you being sick of each other by the end of the trip.\"`")
    
    if x==28:

        await event.edit("`\"If you’ve got some free time and you’re planning on spending it watching tv/playing video games, etc. make yourself go on a short walk or do some brief exercise beforehand. You’ll probably end up going longer than you planned and you’ll feel better about relaxing after.\"`")
    
    if x==29:

        await event.edit("`\"When you get a new notebook, leave the first page blank. When you finish using the notebook, you can number the pages and use the first page as a table of contents.\"`")
    
    if x==30:

        await event.edit("`\"Don’t delete old playlists if you can prevent it; years later you can listen and not only rediscover music you were into but also experience whatever emotion you had associated with your tunes at the time.\"`")
    
    if x==31:

        await event.edit("`\"No matter how small the job is, wear correct masks/respirators/eye or ear protection. Your future self will thank you.\"`")
    
    if x==32:

        await event.edit("`\"Getting angry with people for making mistakes doesn't teach them not to make mistakes, it just teaches them to hide them.\"`")
    
    if x==33:

        await event.edit("`\"When making conversation with someone you've just met, ask them what they've been listening to lately, rather than what their favorite kind of music is - it's fresh in their mind and they won't have to pick favorites on the spot.\"`")
    
    if x==34:

        await event.edit("`\"Learn to do -- and enjoy -- things by yourself. You're going to miss out on a lot of fun if you keep waiting for someone else to accompany you.\"`")
    
    if x==35:

        await event.edit("`\"If you want someone to really listen to you, then start the conversation with \"I shouldn't be telling you this, but...\"\"`")
    
    if x==36:

        await event.edit("`\"Do you not like having bitter coffee but don't want to add sugar for dietary or other reasons? Add a pinch of salt instead, it removes the bitter taste while not making your coffee taste salty.\"`")
    
    if x==37:

        await event.edit("`\"Don't choose a common sound for your alarm clock to wake up. If you hear your alarm clock sound any other time, you will get anxiety.\"`")
    
    if x==38:

        await event.edit("`\"Keep your water bottle near you and your alarm far from you in the morning for a great start to the day!\"`")
    
    if x==39:

        await event.edit("`\"If you borrow money from someone, don’t let it get to the point that he/she has to ask for it back. It sucks for both. If you can’t repay now, show intent by paying what you can and keeping the other person posted often\"`")
    
    if x==40:

        await event.edit("`\"Don't brag about knowledge you just acquired, simply explain it. You will learn humility, plus people often like to learn new things.\"`")
    
    if x==41:

        await event.edit("`\"If you have a favorite movie you’ve seen several (or hundreds) of times, try watching it with subtitles/closed captioning on. You might be surprised just how many lines you heard wrong or missed entirely.\"`")
    
    if x==42:

        await event.edit("`\"Write down great ideas when you get them; do that right away. You think you will never forget them, but you almost always will.\"`")
    
    if x==43:

        await event.edit("`\"If you’re not sure whether someone is waving at you or someone behind you, just smile at them. \n(It’ll save you the very awkward feeling of receiving a greeting meant for someone else.)\"`")
    
    if x==44:

        await event.edit("`\"If you want to offer a deep and memorable compliment, ask someone how they did something. It gives them the opportunity to tell their story, and shows your genuine interest.\"`")
    
    if x==45:

        await event.edit("`\"Don’t hide the things that make you unique. If you smile a certain way or have any thing about you that is not normal, be confident with it. People will find it cute or attractive because it makes you special.\"`")
    
    if x==46:

        await event.edit("`\"When someone only remove one ear pod to talk to you, they most probably don't want a lengthy conversation.\"`")
    
    if x==47:

        await event.edit("`\"If you haven't used your voice in a while (sleeping, lonely, etc) and suddenly need to take a phone call, hum for a few seconds prior. Your vocal cords won't let you down.\"`")
    
    if x==48:

        await event.edit("`\"Open chip bags upside down. They've been sitting upright most of their lives which makes the seasoning settle to the bottom of the bag.\"`")
    
    if x==49:

        await event.edit("`\"If you tell people there is an invisible man in the sky that created the entire universe, most will believe you; if you tell them the paint is wet, most will touch it to be sure.\"`")
    
    if x==50:

        await event.edit("`\"When asked online to confirm \"I am not a robot\", if you long press on the tick box and release, you will not be asked to complete the \"click all store front\" etc tests.\"`")
    
    if x==51:

        await event.edit("`\"Buy yourself a good pillow. You use it every night and the difference between a good pillow and a stack of cheap ones is almost immediately noticeable.\"`")
    
    if x==52:

        await event.edit("`\"If you want your man to win in this world, treat him as a king at home, the world by itself call you a queen!\"`")
    
    if x==53:

        await event.edit("`\"Be mindful of poorer friends when suggesting splitting the bill equally in a restaurant. Some people will choose cheaper options because they're on a budget.\"`")
    
    if x==54:

        await event.edit("`\"When you are trying to resolve an issue where someone else made an error, put the focus on the error and not the person. Example of this: Instead of saying, \“You didn’t send the attachment,\” I say, \“The attachment didn’t come through, please try sending it again.\”\"`")
    
    if x==55:

        await event.edit("`\"Buy a small bottle of perfume you have never tried on before going for a vacation and use it for while you're there. At any point after your vacation, you get a sniff of it, it brings back those memories instantly. Because scents are among the most powerful memory triggers.\"`")
    
    if x==56:

        await event.edit("`\"If someone wishes you Merry Christmas and you don't celebrate Christmas, just say thank you. There's no need to tell them you don't celebrate. It just makes things awkward.\"`")
    
    if x==57:

        await event.edit("`\"When trying to focus on something (writing, revising, reading) listen to music with no words. This allows you to block out unwanted sound and having no lyrics can stop you from being distracted.\"`")
    
    if x==58:

        await event.edit("`\"If you are quitting a vice (smoking, drinking, etc.) treat yourself with the money you are saving. It makes quitting easier.\"`")
    
    if x==59:

        await event.edit("`\"Someone who likes you will often automatically look at you when they laugh or find something funny.\"`")
    
    if x==60:

        await event.edit("`\"Never shake spices over a hot pan. The steam will enter the bottle causing the spice to go hard.\"`")
    
    if x==61:

        await event.edit("`\"When starting a new change in your life such as going to the gym or quitting smoking, avoid telling friends or family. Their positive feedback can give you a false feeling of accomplishment tricking you into thinking you have already succeeded which can hinder your efforts to change.\"`")
    
    if x==62:

        await event.edit("`\"If you are composing an important message, do not enter the recipient until you have finished composing it so that you do not accidentally send an incomplete message.\"`")
    
    if x==63:

        await event.edit("`\"If you are nervous walking into a new place with a group of people, make sure you are the first to the building. You can hold the door for everyone else making yourself look kind, yet you will be the last one in and can follow everyone elses lead.\"`")
    
    if x==2:

        await event.edit("`\"If you're double checking a number or a sequence, read it backwards to avoid making the same mistake twice.\"`")
    
    if x==64:

        await event.edit("`\"Take photos of your parents doing things they do every day. When you get older, they will bring back memories more than any posed pic ever could.\"`")
    
    if x==65:

        await event.edit("`\"If you're in a job interview and you're offered a glass of water, always accept. If you're asked a tough question, you can take a sip and get yourself some extra seconds to think of a response.\"`")
    
    if x==66:

        await event.edit("`\"If you make a mistake, admit to the mistake, apologize, and explain what steps you'll take to prevent it from happening again in the future. It's very hard for people to yell at you if you've done that.\"`")
    
    if x==67:

        await event.edit("`\"Universities like MIT offer free online courses for subjects like Computer Science, Engineering, Psychology and more that include full lectures and exams.\"`")
    
    if x==68:

        await event.edit("`\"Treat another persons phone or computer like you would their diary. Don't even touch it unless they allow you to. It's always for the best.\"`")
    
    if x==69:

        await event.edit("`\"Don't undervalue yourself when deciding whether or not to apply for a new job. It's up to the person doing the hiring to determine if you are what they're looking for, and the only way to guarantee that you won't get the job is if you don't apply for it.\"`")
    
    if x==70:

        await event.edit("`\"When drying clothes in the sun, turn them inside out so the colours don’t fade in the sunlight.\"`")
    
    if x==71:

        await event.edit("`\"To listen to music on your phone via YouTube in the background, use the Chrome browser, go to the video, and request desktop site. This will allow you to listen anywhere on the phone.\"`")
    
    if x==72:

        await event.edit("`\"Whenever your smoke alarm goes off, give your dog a treat. They'll associate the alarm with the treat; so when the alarm goes off for real, your dog will come right to you.\"`")
    
    if x==73:

        await event.edit("`\"You never know what is taking place in a stranger's life. Try to be patient and passive if some seems to be \"overreacting\".\"`")
    
    if x==74:

        await event.edit("`\"Everybody is genious of its own. But if you judge a fish by its ability to climb a tree rather than swimming, she will felt whole life like dumb. So master your field and recognise it very well rather than going after the blind suspections.\"`")
    
    if x==75:

        await event.edit("`\"Search a beautiful heart, not a beautiful face. Beautiful things are not always good, but good things are always beautiful.\"`")
    
    if x==76:

        await event.edit("`\"It's better to cross the line and suffer the consequences than to just stare at the line for the rest of your life.\"`")
    
    if x==77:

        await event.edit("`\"Rather than shushing someone who’s speaking too loudly, try just talking to them in a much quieter voice. They often pick up on the contrast in volume, and self-correct without feeling attacked.\"`")
    
    if x==78:

        await event.edit("`\"If there are no chances for job growth or improvement - it's time to move on. You are worth more the more you learn. Otherwise you are getting paid less the more you know.\"`")
    
    if x==79:

        await event.edit("`\"If you burn food to the bottom of a pot and can't scrub it out, put the pot back on the stove and boil water in it. It will loosen the burnt food and make it easier to clean.\"`")
    
    if x==80:

        await event.edit("`\"When filling out applications online, make sure you copy responses which typically take a long time to write, and paste them to a text file. You never know when you could get a server timeout.\"`")
    
    if x==81:

        await event.edit("`\"Being positive doesn’t mean we don’t get negative thoughts. It just means that we don’t allow those thoughts to control our life.\"`")
    
    if x==82:

        await event.edit("`\"If you share an 'inside joke' with a friend around other people, just let them know what it is even if they won't get it. People don't appreciate being excluded.\"`")
    
    if x==83:

        await event.edit("`\"Never make fun of someone if they mispronounce a word. It means they learned it by reading.\"`")
    
    if x==84:
        await event.edit("`\"If a service dog without a person approaches you, it means that the person is in need of help.\"`")
    if x==85:
        await event.edit("`\"When taking a taxi ALWAYS get a receipt even if you don't need one. That way if you happen to accidentally leave a personal belonging behind you will have the company name and taxi number.\"`")
    if x==86:
        await event.edit("`\"If you're buying a home printer for occasional use, get a laser printer; they're more expensive up front but way more economical in the long run.\"`")
    if x==87:
        await event.edit("`\"Go for that run, no one is looking at you, don't overthink it, do it!\"`")
