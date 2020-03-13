"""

conversation starter questions...

Syntax: .qt

  inspired by @Deonnn's being_logical.py

  edited by : @mahshook_bot

"""



from telethon import events



import asyncio



import os



import sys



import random


from userbot.utils import admin_cmd






@borg.on(admin_cmd(pattern=r"qt"))



async def _(event):



    if event.fwd_from:



        return



    await event.edit("selecting question...")



    await asyncio.sleep(2)



    x=(random.randrange(1,60))



    if x==1:



        await event.edit("`\"Arrange them in descending order of importance – MONEY, LOVE, FAMILY, CAREER, FRIENDS.\"`")



    if x==2:



        await event.edit("`\"If you had to change your name, what would your new name be, and why would you choose that name?\"`")



    if x==3:



        await event.edit("`\"What’s the most interesting thing you’ve read or seen this week?\"`")



    if x==4:



        await event.edit("`\"What scene from a TV show will you never forget?\"`")



    if x==5:



        await event.edit("`\"If you could become a master in one skill, what skill would you choose?\"`")



    if x==6:



        await event.edit("`\"What three words can describe you?\"`")



    if x==7:



        await event.edit("`\"If you had to delete one app from your phone, what would it be?\"`")



    if x==8:



        await event.edit("`\"Would you go out with me if I was the last person on earth?\"`")



    if x==9:



        await event.edit("`\"If you switched genders for the day, what would you do?\"`")



    if x==10:



        await event.edit("`\"If you could eat lunch with someone here. Who would you choose?\"`")



    if x==11:



        await event.edit("`\"If you were told you only had one week left to live, what would you do?\"`")



    if x==12:



        await event.edit("`\"What's number one item you would save from your burning house?\"`")



    if x==13:



        await event.edit("`\"If you could only text one person for the rest of your life, but you could never talk to that person face to face, who would that be?\"`")



    if x==14:



        await event.edit("`\"How many kids do you want to have in the future?\"`")



    if x==15:



        await event.edit("`\"Who in this group would be the worst person to date? Why?\"`")



    if x==16:



        await event.edit("`\"What does your dream boy or girl look like?\"`")



    if x==17:



        await event.edit("`\"What would be in your web history that you’d be embarrassed if someone saw?\"`")



    if x==18:



        await event.edit("`\"Do you sing in the shower?\"`")



    if x==19:



        await event.edit("`\"What’s the right age to get married?\"`")



    if x==20:



        await event.edit("`\"What are your top 5 rules for life?\"`")



    if x==21:



        await event.edit("`\"If given an option, would you choose a holiday at the beach or in the mountains?\"`")



    if x==22:



        await event.edit("`\"If you are made the president of your country, what would be the first thing that you will do?\"`")



    if x==23:



        await event.edit("`\"If given a chance to meet 3 most famous people on the earth, who would it be, answer in order of preference.\"`")



    if x==24:



        await event.edit("`\"Have you ever wished to have a superpower, if so, what superpower you would like to have?\"`")



    if x==25:



        await event.edit("`\"Can you spend an entire day without phone and internet? If yes, what would you do?\"`")



    if x==26:



        await event.edit("`\"Live-in relation or marriage, what do you prefer?\"`")



    if x==27:



        await event.edit("`\"What is your favorite cuisine or type of food?\"`")



    if x==28:



        await event.edit("`\"What are some good and bad things about the education system in your country?\"`")



    if x==29:



        await event.edit("`\"What do you think of online education?\"`")



    if x==30:



        await event.edit("`\"What are some goals you have failed to accomplish?\"`")



    if x==31:



        await event.edit("`\"Will technology save the human race or destroy it?\"`")



    if x==32:



        await event.edit("`\"What was the best invention of the last 50 years?\"`")



    if x==33:



        await event.edit("`\"Have you travelled to any different countries? Which ones?\"`")



    if x==34:



        await event.edit("`\"Which sport is the most exciting to watch? Which is the most boring to watch?\"`")



    if x==35:



        await event.edit("`\"What’s the most addictive mobile game you have played?\"`")



    if x==36:



        await event.edit("`\"How many apps do you have on your phone?\"`")



    if x==37:



        await event.edit("`\"What was the last song you listened to?\"`")



    if x==38:



        await event.edit("`\"Do you prefer to watch movies in the theater or in the comfort of your own home?\"`")



    if x==39:



        await event.edit("`\"Do you like horror movies? Why or why not?\"`")



    if x==40:



        await event.edit("`\"How often do you help others? Who do you help? How do you help?\"`")



    if x==41:



        await event.edit("`\"What song do you play most often?\"`")



    if x==42:



        await event.edit("`\"Suggest a new rule that should be added in this group!\"`")



    if x==43:



        await event.edit("`\"What app on your phone do you think I should get?\"`")



    if x==44:



        await event.edit("`\"What website or app has completely changed your life for better or for worse?\"`")



    if x==45:



        await event.edit("`\"What isn’t real but you desperately wish it was?\"`")



    if x==46:



        await event.edit("`\"What thing do you really wish you could buy right now?\"`")



    if x==47:



        await event.edit("`\"If you could ban an admin from this group. Who would you prefer ?\"`")



    if x==48:



        await event.edit("`\"What would you do if someone left a duffle bag filled with $2,000,000 on your back porch?\"`")



    if x==49:



        await event.edit("`\"Who is the luckiest person you know?\"`")



    if x==50:



        await event.edit("`\"If you could visit someone's house in this group, who would it be ?\"`")



    if x==51:



        await event.edit("`\"What are you tired of hearing about?\"`")



    if x==52:



        await event.edit("`\"If you died today, what would your greatest achievement be?\"`")



    if x==53:



        await event.edit("`\"What method will you choose to kill yourself?\"`")



    if x==54:



        await event.edit("`\"What’s the best news you've heard in the last 24 hours?\"`")



    if x==55:



        await event.edit("`\"What is the most important change that should be made to your country’s education system?\"`")



    if x==56:



        await event.edit("`\"Send your favourite sticker pack.\"`")



    if x==57:



        await event.edit("`\"Send your favourite animated sticker pack.\"`")



    if x==58:



        await event.edit("`\"Send your favourite video or gif.\"`")



    if x==59:



        await event.edit("`\"Send your favourite emojies\"`")



    if x==60:



        await event.edit("`\"What’s something you misunderstood as a child and only realized much later was wrong?\"`")
