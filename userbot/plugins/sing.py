from telethon import events
import asyncio
import os
import sys
import random
from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern=r"msing$", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Singing...")
    await asyncio.sleep(2)
    x=(random.randrange(1,44))
    if x==1:
        await event.edit("🎶 ഒരുനാൾ തരളമിവനിൽ... പടരൂ വനലതികയായ്... മുറുകെ... മതിവരുവോളം സഖീ... 🎶")
    if x==2:
        await event.edit("🎶 അഴലിന്റെ ആഴങ്ങളിൽ അവൾ മാഞ്ഞുപോയ്... നോവിന്റെ തീരങ്ങളിൽ ഞാൻ മാത്രമായ്... 🎶")
    if x==3:
        await event.edit("🎶 ആവണിപ്പൊന്നൂഞ്ഞാലാടിക്കാം നിന്നെ ഞാൻ... ആയില്ല്യം കാവിലെ വെണ്ണിലാവേ... 🎶")
    if x==4:
        await event.edit("🎶 ഇന്ദ്രനീലിമയോലും ഈ മിഴി പൊയ്കകളിൽ... ഇന്നലെ നിൻ മുഖം നീ നോക്കി നിന്നൂ... 🎶")
    if x==5:
        await event.edit("🎶 മയിലായ് പറന്നുവാ മഴവില്ലു തോൽക്കുമെന്നഴകേ... 🎶")
    if x==6:
        await event.edit("🎶 നിലാവിന്റെ നീലഭസ്മ കുറിയണിഞ്ഞവളേ... കാതിലോലക്കമ്മലിട്ടു കുണുങ്ങി നിന്നവളേ... 🎶")
    if x==7:
        await event.edit("🎶 നീയൊരു പുഴയായ് തഴുകുമ്പോൾ ഞാൻ പ്രണയം വിടരും കരയാവും... 🎶")    
    if x==8:
        await event.edit("🎶 അരികിൽ നീയുണ്ടായിരുന്നെങ്കിലെന്നു ഞാൻ... ഒരുമാത്ര വെറുതേ നിനച്ചുപോയി... 🎶")
    if x==9:
        await event.edit("🎶 എത്രയോ ജന്മമായ് നിന്നെഞാൻ തേടുന്നു... അത്രമേൽ ഇഷ്ടമായ് നിന്നെയെൻ പുണ്യമേ... 🎶")
    if x==10:
        await event.edit("🎶 മഴത്തുള്ളികൾ പൊഴിഞ്ഞീടുമീ നാടൻ വഴി... നനഞ്ഞോടിയെൻ കുടക്കീഴിൽ നീ വന്ന നാൾ... 🎶")     
    if x==11:
        await event.edit("🎶 കരളേ നിൻ കൈ പിടിച്ചാൽ, കടലോളം വെണ്ണിലാവ്... ഉൾക്കണ്ണിൻ കാഴ്ചയിൽ നീ, കുറുകുന്നൊരു വെൺപിറാവ്... 🎶")
    if x==12:
        await event.edit("🎶 മറന്നിട്ടുമെന്തിനോ മനസ്സിൽ തുളുമ്പുന്നു മൗനാനുരാഗത്തിൻ ലോലഭാവം... 🎶")    
    if x==13:
        await event.edit("🎶 മഴക്കാലം എനിക്കായി മയിൽ ചെലുള്ള പെണ്ണേ നിന്നെത്തന്നേ... 🎶")
    if x==14:
        await event.edit("🎶 മിഴിയറിയാതെ വന്നു നീ മിഴിയൂഞ്ഞാലിൽ... കനവറിയാതെയേതോ കിനാവു പോലെ... 🎶")        
    if x==15:
        await event.edit("🎶 ചന്ദനച്ചോലയിൽ മുങ്ങിനീരാടിയെൻ ഇളമാൻ കിടാവേ ഉറക്കമായോ... 🎶")
    if x==16:
        await event.edit("🎶 കറുത്തപെണ്ണേ നിന്നെ കാണാഞ്ഞിട്ടൊരു നാളുണ്ടേ... 🎶")    
    if x==17:
        await event.edit("🎶 താമരപ്പൂവിൽ വാഴും ദേവിയല്ലോ നീ... പൂനിലാക്കടവിൽ പൂക്കും പുണ്യമല്ലോ നീ... 🎶")
    if x==18:
        await event.edit("🎶 പാടം പൂത്തകാലം പാടാൻ വന്നു നീയും... 🎶")
    if x==19:
        await event.edit("🎶 രാജഹംസമേ മഴവിൽ കുടിലിൽ... സ്നേഹദൂതുമായ് വരുമോ... 🎶")
    if x==20:
        await event.edit("🎶 പത്തുവെളുപ്പിന് മുറ്റത്തു നിക്കണ കസ്തൂരി മുല്ലയ്ക്ക് കാത്തുകുത്ത്... എന്റെ കസ്തൂരി മുല്ലയ്ക്ക് കാത്തുകുത്ത്... 🎶")
    if x==21:     
        await event.edit("🎶 മഞ്ഞൾ പ്രസാദവും നെറ്റിയിൽ ചാർത്തി... മഞ്ഞക്കുറിമുണ്ടു ചുറ്റി... 🎶")        
    if x==22:        
        await event.edit("🎶 അന്തിപ്പൊൻവെട്ടം കടലിൽ മെല്ലെത്താഴുമ്പോൾ... മാനത്തെ മുല്ലത്തറയില് മാണിക്യച്ചെപ്പ്... 🎶")       
    if x==23:
        await event.edit("🎶 അമ്പലപ്പുഴെ ഉണ്ണിക്കണ്ണനോടു നീ... എന്തുപരിഭവം മെല്ലെയോതിവന്നുവോ... 🎶")
    if x==24:
        await event.edit("🎶 കുടജാദ്രിയിൽ കുടചൂടുമാ കോടമഞ്ഞുപോലെയീ പ്രണയം... തഴുകുന്നു, എന്നെ പുണരുന്നു... 🎶")
    if x==25:       
        await event.edit("🎶 ശ്യാമാംബരം പുൽകുന്നൊരാ വെൺചന്ദ്രനായ് നിൻ പൂമുഖം... 🎶")       
    if x==26:       
        await event.edit("🎶 ശ്രീരാഗമോ തേടുന്നിതെൻ വീണതൻ പൊൻ തന്ത്രിയിൽ... 🎶")        
    if x==27:        
        await event.edit("🎶 എന്തിനു വേറൊരു സൂര്യോദയം... നീയെൻ പൊന്നുഷസ്സന്ധ്യയല്ലേ... 🎶")        
    if x==28:        
        await event.edit("🎶 അനുരാഗിണീ ഇതായെൻ കരളിൽ വിരിഞ്ഞ പൂക്കൾ... 🎶")
    if x==29:        
        await event.edit("🎶 പാടാം നമുക്കു പാടാം... വീണ്ടുമൊരു പ്രേമഗാനം... 🎶")        
    if x==30:        
        await event.edit("🎶 അല്ലിമലർ കാവിൽ പൂരം കാണാൻ... അന്നു നമ്മൾ പോയി രാവിൽ നിലാവിൽ... 🎶")    
    if x==31:        
        await event.edit("🎶 കറുകവയൽ കുരുവീ... മുറിവാലൻ കുരുവീ... തളിർ വെറ്റിലയുണ്ടോ... വരദക്ഷിണ വെക്കാൻ... 🎶")        
    if x==32:        
        await event.edit("🎶 കുന്നിമണിച്ചെപ്പു തുറന്നെണ്ണി നോക്കും നേരം, പിന്നിൽവന്നു കണ്ണു പൊത്തും കള്ളനെങ്ങു പോയി... 🎶")        
    if x==33:        
        await event.edit("🎶 നാടോടി പൂന്തിങ്കൾ മുടിയിൽ ചൂടി നവരാത്രി പുള്ളോർക്കുടമുള്ളിൽ മീട്ടി കണിക്കൊന്നപ്പൂ മണിക്കമ്മലണിഞ്ഞും പുളിയിലക്കര കസവുമുണ്ടുടുത്തും പുഴയിന്നൊരു നാടൻ പെണ്ണായോ... 🎶")        
    if x==34:        
        await event.edit("🎶 നീ കണ്ണോട് കണ്ണോട് കണ്ണോരമായ് കാതോട് കാതോട് കാതോരമായ് നെഞ്ചോട് നെഞ്ചോട് നെഞ്ചോരമായ് നിറയേ....🎶")        
    if x==35:      
        await event.edit("🎶 എള്ളോളം തരി പൊന്നെന്തിനാ തനി തഞ്ചാവൂര് പട്ടെന്തിനാ തങ്കം തെളിയണ പട്ടു തിളങ്ങണ ചന്തം നിനക്കാടീ... 🎶")     
    if x==36:        
        await event.edit("🎶 പൂമുത്തോളെ നീയെരിഞ്ഞ വഴിയില്‍ ഞാന്‍മഴയായി പെയ്തെടീ... ആരീരാരം ഇടറല്ലേ മണിമുത്തേ കണ്മണീ... മാറത്തുറക്കാനിന്നോളം തണലെല്ലാം വെയിലായി കൊണ്ടെടീ... മാനത്തോളം മഴവില്ലായ്‌ വളരേണം എന്‍ മണീ ..🎶")        
    if x==37:       
        await event.edit("🎶 നീ ഹിമമഴയായ് വരൂ... ഹൃദയം അണിവിരലാൽ തൊടൂ... ഈ മിഴിയിണയിൽ സദാ പ്രണയം മഷിയെഴുതുന്നിതാ... ശിലയായി നിന്നിടാം നിന്നെ നോക്കീ യുഗമേറെയെന്റെ കൺചിമ്മിടാതെ... എൻജീവനേ......🎶")       
    if x==38:       
        await event.edit("🎶 ലല്ലലം ചൊല്ലുന്ന ചെല്ലകിളികളേ വേടന്‍ കുരുക്കും കടങ്കഥ ഇക്കഥ ഇക്കഥയ്ക്കുത്തരം തേടുവാന്‍ കൂടാമോ.. ഇല്ലെങ്കില്‍ സുല്ലെങ്കില്‍ ഇല്ലില്ല സമ്മാനം...🎶")        
    if x==39:        
        await event.edit("🎶 സുന്ദരീ സുന്ദരീ ഒന്നൊരുങ്ങി വാ നാളെയാണ് താലി മംഗലം.... 🎶")        
    if x==40:        
        await event.edit("🎶 തൂമിന്നൽ തൂവൽ തുമ്പാൽ മെല്ലെ എൻ പൂവൽ കനവിൽ തഴുകാൻ വരൂ... വാർതിങ്കൾ മായും രാവിൻ കൊമ്പിൽ ചിറകേറി നീ പുലർ വെയിൽ മലർ തരൂ...🎶")        
    if x==41:        
        await event.edit("🎶 ജീവാംശമായ് താനേ നീ എന്നിൽ കാലങ്ങൾ മുന്നേ വന്നൂ ...🎶")        
    if x==42:       
        await event.edit("🎶 ചന്ദനക്കുറി നീയണിഞ്ഞതിലെന്റെ പേര് പതിഞ്ഞില്ലേ.... 🎶")       
    if x==43:      
        await event.edit("🎶 ആവണിപ്പൊന്നൂഞ്ഞാലാടിക്കാം നിന്നെ ഞാൻ ആയില്യം കാവിലെ വെണ്ണിലാവേ പാതിരാമുല്ലകൾ താലിപ്പൂ ചൂടുമ്പോൾ പൂജിക്കാം നിന്നെ ഞാൻ പൊന്നു പോലെ...🎶")       
    if x==44:        
        await event.edit("🎶 പണ്ടു പണ്ടേ പൂത്ത മലരുകൾ മിന്നും മിന്നാമിനുങ്ങുകൾ ഒരു കുറി ഇനി വരുമോ...🎶")    

@borg.on(admin_cmd(pattern=r"sing$", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Singing...")
    await asyncio.sleep(2)
    x=(random.randrange(1,66))    
    if x==1:
        await event.edit("🎶 Put your wings on me, wings on me \n When I was so heavy \n Pour on a symphony \n When I'm low, low, low, low \n Ah, oh-ah, oh-ah \nGot me feeling drunk and high \n So high, so high🎶")
    if x==2:
        await event.edit("🎶 I know it breaks your heart \n Moved to the city in a broke down car \n And four years, no calls \n Now you're looking pretty in a hotel bar... 🎶")
    if x==3:
        await event.edit("🎶 If we go down then we go down together... \n They'll say you could do anything... \n They'll say that I was clever🎶")
    if x==4:
        await event.edit("🎶 You were the shadow to my light \n Did you feel us? \n Another star,You fade away... 🎶")
    if x==5:
        await event.edit("🎶 Lately, I've been, I've been thinking \n I want you to be happier, I want you to be happier....  🎶")
    if x==6:
        await event.edit("🎶 You say you love me, I say you crazy \n We're nothing more than friends \n You're not my lover, more like a brother \n I known you since we were like ten, yeah...🎶")
    if x==7:
        await event.edit("🎶  Oh won't you stay for a while \n I'll take you on a ride \n If you can keep a secret\n Oh won't you stay for a while\n Show me darkness baby, show me deepness...🎶")    
    if x==8:
        await event.edit("🎶 Take me through the night \n Fall into the dark side \n We don't need the light\n We'll live on the dark side...🎶")
    if x==9:
        await event.edit("🎶I'm so alone \n Nothing feels like home \n I'm so alone \n Trying to find my way back home to you...  🎶")
    if x==10:
        await event.edit("🎶 I'm not looking for somebody \n With some superhuman gifts \n Some superhero\n Some fairytale bliss\n Just something I can turn to \n Somebody I can kiss... 🎶")   
    if x==11:
        await event.edit("🎶 What you don't understand is I'd catch a grenade for ya,yeah...yeah...\n Throw my hand on a blade for ya...yeah...yeah... \n I'd jump in front of a train for ya...yeah...yeah... \n You know I'd do anything for ya...yeah...yeah...🎶")
    if x==12:
        await event.edit("🎶 He said, One day you'll leave this world behind So live a life you will remember \n My father told me when I was just a child \n These are the nights that never die \n My father told me...🎶")   
    if x==13:
        await event.edit("🎶 So wake me up when it's all over \n When I'm wiser and I'm older \n All this time I was finding myself \n And I didn't know I was lost 🎶")
    if x==14:
        await event.edit("🎶Monday left me broken \n Tuesday, I was through with hoping \n Wednesday, my empty arms were open \n Thursday, waiting for love, waiting for love... 🎶")        
    if x==15:
        await event.edit("🎶 Yeah, I'm gonna take my horse to the old town road \n I'm gonna ride 'til I can't no more \n I'm gonna take my horse to the old town road \n I'm gonna ride 'til I can't no more... 🎶")
    if x==16:
        await event.edit("🎶 Then you're left in the dust \n Unless I stuck by ya \n You're a sunflower \n I think your love would be too much \n Or you'll be left in the dust \n Unless I stuck by ya \n You're the sunflower \n You're the sunflower 🎶")     
    if x==17:
        await event.edit("🎶 I love it when you call me señorita \n I wish I could pretend I didn't need ya \n But every touch is ooh la la la \n It's true, la la la \n Ooh, I should be running \n Ooh, you keep me coming for ya... 🎶")
    if x==18:
        await event.edit("🎶 Your sugar \n Yes, please \n Won't you come and put it down on me \n I'm right here, 'cause I need \n Little love and little sympathy...🎶")
    if x==19:
        await event.edit("🎶 Lately I been, I been losing sleep \n Dreaming about the things that we could be \n But baby I been, I been prayin' hard \n Said no more counting dollars \n We'll be counting stars \n Yeah, we'll be counting stars... 🎶")
    if x==20:
        await event.edit("🎶I've been running through the jungle \n I've been running with the wolves \n To get to you, to get to you \n I've been down the darkest alleys \n Saw the dark side of the moon \n To get to you, to get to you... 🎶")
    if x==21:        
        await event.edit("🎶 Hypnotized, this love out of me \n Without your air I can't even breathe \n Lead my way out into the light \n Sing your lu-lu-lu-lullaby... 🎶")       
    if x==22:        
        await event.edit("🎶I can feel your love pullin' me up from the underground, and \n I don't need my drugs, we could be more than just part-time lovers...🎶")       
    if x==23:
        await event.edit("🎶 Maybe we're perfect strangers \n Maybe it's not forever \n Maybe the night will change us \n Maybe we'll stay together \n Maybe we'll walk away \n Maybe we'll realize \n We're only human \n Maybe we don't need no reason...🎶")
    if x==24:
        await event.edit("🎶 Hey, I just met you and this is crazy \n But here's my number, so call me maybe \n It's hard to look right at you baby \n But here's my number, so call me maybe... 🎶")
    if x==25:        
        await event.edit("🎶 You just want attention, you don't want my heart \n Maybe you just hate the thought of me with someone new \n Yeah, you just want attention, I knew from the start \n You're just making sure I'm never gettin' over you...🎶")        
    if x==26:        
        await event.edit("🎶 We don't talk anymore, we don't talk anymore \n We don't talk anymore, like we used to do \n We don't love anymore \n What was all of it for? \n oh, we don't talk anymore, like we used to do...🎶")
    if x==27:        
        await event.edit("🎶 So love me like you do, lo-lo-love me like you do \n Love me like you do, lo-lo-love me like you do \n Touch me like you do, to-to-touch me like you do \n What are you waiting for?...🎶")        
    if x==28:        
        await event.edit("🎶 I've become so numb, I can't feel you there \n Become so tired, so much more aware \n By becoming this all I want to do \n Is be more like me and be less like you... 🎶")
    if x==29:     
        await event.edit("🎶 Cause girls like you \n Run around with guys like me \n Til sundown, when I come through \n I need a girl like you, yeah yeah... 🎶")        
    if x==30:        
        await event.edit("🎶Cold enough to chill my bones \n It feels like I don't know you anymore \n I don't understand why you're so cold to me \n With every breath you breathe \n I see there's something going on \n I don't understand why you're so cold... 🎶")   
    if x==31:        
        await event.edit("🎶 And if you feel you're sinking, I will jump right over \n Into cold, cold water for you \n And although time may take us into different places \n I will still be patient with you... 🎶")       
    if x==32:        
        await event.edit("🎶 I know I can treat you better \n Than he can... \n And any girl like you deserves a gentleman \n Tell me why are we wasting time \n On all your wasted cryin, When you should be with me instead \n I know I can treat you better \n Better than he can...🎶")        
    if x==33:        
        await event.edit("🎶 I'm in love with the shape of you \n We push and pull like a magnet do\n Although my heart is falling too \n I'm in love with your body \n And last night you were in my room \n And now my bedsheets smell like you \n Every day discovering something brand new 🎶  \n 🎶  I'm in love with your body \n Oh—I—oh—I—oh—I—oh—I \n I'm in love with your body \n Oh—I—oh—I—oh—I—oh—I \n I'm in love with your body \n Oh—I—oh—I—oh—I—oh—I \n I'm in love with your body 🎶 \n **-Shape of You**")                       
    if x==34:        
        await event.edit("🎶Youngblood \n Say you want me, Say you want me \n Back in your life \n So I'm just a dead man crawling tonight \n 'Cause I need it, yeah, I need it \n All of the time \n Yeah, ooh ooh ooh...🎶")
    if x==35:
        await event.edit("🎶 I've been reading books of old \n The legends and the myths \n Achilles and his gold \n Hercules and his gifts \n Spiderman's control \n And Batman with his fists \n And clearly I don't see myself upon that list 🎶 \n **-Something Just Like This **")
    if x==36:
        await event.edit("🎶 I don't wanna live forever \n 'Cause I know I'll be livin' in vain \n And I don't wanna fit wherever \n I just wanna keep callin' your name \n Until you come back home \n I just wanna keep callin' your name \n Until you come back home \n I just wanna keep callin' your name \n Until you come back home 🎶 \n **-I don't Wanna Live Forever **")
    if x==37:
        await event.edit("🎶 Oh, hush, my dear, it's been a difficult year \n And terrors don't prey on \n Innocent victims \n Trust me, darling, trust me darling \n It's been a loveless year \n I'm a man of three fears \n Integrity, faith and \n Crocodile tears \n Trust me, darling, trust me, darling 🎶 \n **-Bad Lier")
    if x==38:
        await event.edit("🎶 Walking down 29th and Park \n I saw you in another's arms \n Only a month we've been apart \n **You look happier** \n \n Saw you walk inside a bar \n He said something to make you laugh \n I saw that both your smiles were twice as wide as ours \n Yeah, you look happier, you do 🎶 \n **-Happier **")
    if x==39:
        await event.edit("🎶 I took the supermarket flowers from the windowsill \n I threw the day old tea from the cup \n Packed up the photo album Matthew had made \n Memories of a life that's been loved \n Took the get well soon cards and stuffed animals \n Poured the old ginger beer down the sink \n Dad always told me, 'don't you cry when you're down' \n But mum, there's a tear every time that I blink 🎶 \n **-Supermarket Flowers**")
    if x==40:
        await event.edit("🎶 And you and I we're flying on an aeroplane tonight \n We're going somewhere where the sun is shining bright \n Just close your eyes \n And let's pretend we're dancing in the street \n In Barcelona \n Barcelona \n Barcelona \n Barcelona 🎶 \n **-Barcelona **")    
    if x==41:
        await event.edit("🎶 Maybe I came on too strong \n Maybe I waited too long \n Maybe I played my cards wrong \n Oh, just a little bit wrong \n Baby I apologize for it \n \n I could fall, or I could fly \n Here in your aeroplane \n And I could live, I could die \n Hanging on the words you say \n And I've been known to give my all \n And jumping in harder than \n Ten thousand rocks on the lake 🎶 \n **-Dive**")
    if x==42:
        await event.edit("🎶 I found a love for me \n Darling just dive right in \n And follow my lead \n Well I found a girl beautiful and sweet \n I never knew you were the someone waiting for me \n 'Cause we were just kids when we fell in love \n Not knowing what it was \n \n I will not give you up this time \n But darling, just kiss me slow, your heart is all I own \n And in your eyes you're holding mine 🎶 \n **-Perfect**")
    if x==43:
        await event.edit("🎶 I was born inside a small town, I lost that state of mind \n Learned to sing inside the Lord's house, but stopped at the age of nine \n I forget when I get awards now the wave I had to ride \n The paving stones I played upon, they kept me on the grind \n So blame it on the pain that blessed me with the life 🎶 \n **-Eraser**")     
    if x==44:
        await event.edit("🎶 Say, go through the darkest of days \n Heaven's a heartbreak away \n Never let you go, never let me down \n Oh, it's been a hell of a ride \n Driving the edge of a knife. \n Never let you go, never let me down \n \n Don't you give up, nah-nah-nah \n I won't give up, nah-nah-nah \n Let me love you \n Let me love you 🎶 \n **-Let me Love You**")
    if x==45:
        await event.edit("🎶 I'll stop time for you \n The second you say you'd like me to \n I just wanna give you the loving that you're missing \n Baby, just to wake up with you \n Would be everything I need and this could be so different \n Tell me what you want to do \n \n 'Cause I know I can treat you better \n Than he can \n And any girl like you deserves a gentleman 🎶 **-Treat You Better**")    
    if x==46:
        await event.edit("🎶 You're the light, you're the night \n You're the color of my blood \n You're the cure, you're the pain \n You're the only thing I wanna touch \n Never knew that it could mean so much, so much \n You're the fear, I don't care \n 'Cause I've never been so high \n Follow me through the dark \n Let me take you past our satellites \n You can see the world you brought to life, to life \n \n So love me like you do, lo-lo-love me like you do \n Love me like you do, lo-lo-love me like you do 🎶 \n **-Love me Like you Do**")
    if x==47:
        await event.edit("🎶 Spent 24 hours \n I need more hours with you \n You spent the weekend \n Getting even, ooh ooh \n We spent the late nights \n Making things right, between us \n But now it's all good baby \n Roll that Backwood baby \n And play me close \n \n 'Cause girls like you \n Run around with guys like me \n 'Til sundown, when I come through \n I need a girl like you, yeah yeah 🎶 \n **-Girls Like You**")        
    if x==48:
        await event.edit("🎶 Oh, angel sent from up above \n You know you make my world light up \n When I was down, when I was hurt \n You came to lift me up \n Life is a drink and love's a drug \n Oh, now I think I must be miles up \n When I was a river dried up \n You came to rain a flood 🎶**-Hymn for the Weekend ** ")
    if x==49:
        await event.edit("🎶 I've known it for a long time \n Daddy wakes up to a drink at nine \n Disappearing all night \n I don’t wanna know where he's been lying \n I know what I wanna do \n Wanna run away, run away with you \n Gonna grab clothes, six in the morning, go 🎶 \n **-Runaway **")     
    if x==50:
        await event.edit("🎶 You were the shadow to my light \n Did you feel us \n Another start \n You fade away \n Afraid our aim is out of sight \n Wanna see us \n Alive 🎶 \n **-Faded**")
    if x==51:
        await event.edit("🎶 It's been a long day without you, my friend \n And I'll tell you all about it when I see you again \n We've come a long way from where we began \n Oh I'll tell you all about it when I see you again \n When I see you again 🎶 \n **-See you Again**")
    if x==52:
        await event.edit("🎶 I can swallow a bottle of alcohol and I'll feel like Godzilla \n Better hit the deck like the card dealer \n My whole squad's in here, walking around the party \n A cross between a zombie apocalypse and big Bobby 'The \n Brain' Heenan which is probably the \n Same reason I wrestle with mania 🎶 \n **-Godzilla**")
    if x==53:
        await event.edit("🎶 Yeah, I'm gonna take my horse to the old town road \n I'm gonna ride 'til I can't no more \n I'm gonna take my horse to the old town road \n I'm gonna ride 'til I can't no more (Kio, Kio) 🎶 \n **-Old Town Road**")
    if x==54:     
        await event.edit("🎶 Oh-oh, ooh \n You've been runnin' round, runnin' round, runnin' round throwin' that dirt all on my name \n 'Cause you knew that I, knew that I, knew that I'd call you up \n You've been going round, going round, going round every party in L.A. \n 'Cause you knew that I, knew that I, knew that I'd be at one, oh 🎶 \n **-Attention **")     
    if x==55:      
        await event.edit("🎶 This hit, that ice cold \n Michelle Pfeiffer, that white gold \n This one for them hood girls \n Them good girls straight masterpieces \n Stylin', wilin', livin' it up in the city \n Got Chucks on with Saint Laurent \n Gotta kiss myself, I'm so pretty \n \n I'm too hot (hot damn) \n Called a police and a fireman \n I'm too hot (hot damn) \n Make a dragon wanna retire man \n I'm too hot (hot damn) \n Say my name you know who I am \n I'm too hot (hot damn) \n And my band 'bout that money, break it down 🎶 \n **-Uptown Funk**")      
    if x==56:
        await event.edit("🎶 Just a young gun with the quick fuse \n I was uptight, wanna let loose \n I was dreaming of bigger things \n And wanna leave my own life behind \n Not a yes sir, not a follower \n Fit the box, fit the mold \n Have a seat in the foyer, take a number \n I was lightning before the thunder \n \n Thunder, feel the thunder \n Lightning then the thunder \n Thunder, feel the thunder \n Lightning then the thunder \n Thunder, thunder 🎶 \n **-Thunder**")
    if x==57:
        await event.edit("🎶 Oh, love \n How I miss you every single day \n When I see you on those streets \n Oh, love \n Tell me there's a river I can swim that will bring you back to me \n 'Cause I don't know how to love someone else \n I don't know how to forget your face \n No, love \n God, I miss you every single day and now you're so far away \n So far away 🎶 \n **-So Far Away**")
    if x==58:       
        await event.edit("🎶 And if you feel you're sinking, I will jump right over \n Into cold, cold water for you \n And although time may take us into different places \n I will still be patient with you \n And I hope you know 🎶 \n **-Cold Water**")      
    if x==59:        
        await event.edit("🎶 When you feel my heat \n Look into my eyes \n It's where my demons hide \n It's where my demons hide \n Don't get too close \n It's dark inside \n It's where my demons hide \n It's where my demons hide 🎶 \n **-Demons**")        
    if x==60:        
        await event.edit("🎶 Who do you love, do you love now? \n I wanna know the truth (whoa) \n Who do you love, do you love now? \n I know it's someone new \n You ain't gotta make it easy, where you been sleepin'? 🎶 \n **-Who do  Love? **")       
    if x==61:        
        await event.edit("🎶 Your touch is magnetic \n 'Cause I can't forget it \n (There's a power pulling me back to you) \n And baby I'll let it \n 'Cause you're so magnetic I get it \n (When I'm waking up with you, oh) 🎶 \n **-Magnetic**")
    if x==62:        
        await event.edit("🎶 Girl my body don't lie, I'm outta my mind \n Let it rain over me, I'm rising so high \n Out of my mind, so let it rain over me \n \n Ay ay ay, ay ay ay let it rain over me \n Ay ay ay, ay ay ay let it rain over me 🎶 \n **-Rain over Me**")        
    if x==63:        
        await event.edit("🎶 I miss the taste of a sweeter life \n I miss the conversation \n I'm searching for a song tonight \n I'm changing all of the stations \n I like to think that we had it all \n We drew a map to a better place \n But on that road I took a fall \n Oh baby why did you run away? \n \n I was there for you \n In your darkest times \n I was there for you \n In your darkest night 🎶 \n **-Maps**")    
    if x==64:        
        await event.edit("🎶 I wish—I wish that I was bulletproof, bulletproof \n I wish—I wish that I was bulletproof, bulletproof \n (Bullet-bulletproof, bullet-bullet-bulletproof) \n I'm trippin' on my words and my patience \n Writing every verse in a cadence \n To tell you how I feel, how I feel, how I feel (Yeah) \n This is how I deal, how I deal, how I deal (Yeah) \n With who I once was, now an acquaintance \n Think my confidence (My confidence) is in the basement \n Tryin' to keep it real, keep it real, keep it real (Yeah) \n 'Cause I'm not made of steel, made of steel 🎶 \n **-Bulletproof**")        
    if x==65:      
        await event.edit("🎶 You won't find him down on Sunset \n Or at a party in the hills \n At the bottom of the bottle \n Or when you're tripping on some pills \n When they sold you the dream you were just 16 \n Packed a bag and ran away \n And it's a crying shame you came all this way \n 'Cause you won't find Jesus in LA \n And it's a crying shame you came all this way \n 'Cause you won't find Jesus in LA 🎶 \n **-Jesus in LA**")      
    if x==66:        
        await event.edit("Not in a mood to sing. Sorry!")                         
