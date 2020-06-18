""" Sing a Malayalam song... 
    Command .sing 
    By @Deonnn """



# BY @Deonnn

from telethon import events

import asyncio

import os

import sys

import random



@borg.on(events.NewMessage(pattern=r"\.sing", outgoing=True))

async def _(event):

    if event.fwd_from:

        return

    await event.edit("Singing...")

    await asyncio.sleep(2)

    x=(random.randrange(1,67))
    
    if x==1:

        await event.edit("`🎶 Put your wings on me, wings on me \n When I was so heavy \n Pour on a symphony \n When I'm low, low, low, low \n Ah, oh-ah, oh-ah \nGot me feeling drunk and high \n So high, so high🎶`")

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
        
        await event.edit("🎶I'm in love with the shape of you \n We push and pull like a magnet do \n Although my heart is falling too \n I'm in love with your body...🎶")
                         
    if x==34:
        
        await event.edit("🎶Youngblood \n Say you want me, Say you want me \n Back in your life \n So I'm just a dead man crawling tonight \n 'Cause I need it, yeah, I need it \n All of the time \n Yeah, ooh ooh ooh...🎶")

    if x==35:

        await event.edit("🎶 ഒരുനാൾ തരളമിവനിൽ... പടരൂ വനലതികയായ്... മുറുകെ... മതിവരുവോളം സഖീ... 🎶")

    if x==36:

        await event.edit("🎶 അഴലിന്റെ ആഴങ്ങളിൽ അവൾ മാഞ്ഞുപോയ്... നോവിന്റെ തീരങ്ങളിൽ ഞാൻ മാത്രമായ്... 🎶")

    if x==37:

        await event.edit("🎶 ആവണിപ്പൊന്നൂഞ്ഞാലാടിക്കാം നിന്നെ ഞാൻ... ആയില്ല്യം കാവിലെ വെണ്ണിലാവേ... 🎶")

    if x==38:

        await event.edit("🎶 ഇന്ദ്രനീലിമയോലും ഈ മിഴി പൊയ്കകളിൽ... ഇന്നലെ നിൻ മുഖം നീ നോക്കി നിന്നൂ... 🎶")

    if x==39:

        await event.edit("🎶 മയിലായ് പറന്നുവാ മഴവില്ലു തോൽക്കുമെന്നഴകേ... 🎶")

    if x==40:

        await event.edit("🎶 നിലാവിന്റെ നീലഭസ്മ കുറിയണിഞ്ഞവളേ... കാതിലോലക്കമ്മലിട്ടു കുണുങ്ങി നിന്നവളേ... 🎶")

    if x==41:

        await event.edit("🎶 നീയൊരു പുഴയായ് തഴുകുമ്പോൾ ഞാൻ പ്രണയം വിടരും കരയാവും... 🎶")    

    if x==42:

        await event.edit("🎶 അരികിൽ നീയുണ്ടായിരുന്നെങ്കിലെന്നു ഞാൻ... ഒരുമാത്ര വെറുതേ നിനച്ചുപോയി... 🎶")

    if x==43:

        await event.edit("🎶 എത്രയോ ജന്മമായ് നിന്നെഞാൻ തേടുന്നു... അത്രമേൽ ഇഷ്ടമായ് നിന്നെയെൻ പുണ്യമേ... 🎶")

    if x==44:

        await event.edit("🎶 മഴത്തുള്ളികൾ പൊഴിഞ്ഞീടുമീ നാടൻ വഴി... നനഞ്ഞോടിയെൻ കുടക്കീഴിൽ നീ വന്ന നാൾ... 🎶")
     
    if x==45:

        await event.edit("🎶 കരളേ നിൻ കൈ പിടിച്ചാൽ, കടലോളം വെണ്ണിലാവ്... ഉൾക്കണ്ണിൻ കാഴ്ചയിൽ നീ, കുറുകുന്നൊരു വെൺപിറാവ്... 🎶")

    if x==46:

        await event.edit("🎶 മറന്നിട്ടുമെന്തിനോ മനസ്സിൽ തുളുമ്പുന്നു മൗനാനുരാഗത്തിൻ ലോലഭാവം... 🎶")
    
    if x==47:

        await event.edit("🎶 മഴക്കാലം എനിക്കായി മയിൽ ചെലുള്ള പെണ്ണേ നിന്നെത്തന്നേ... 🎶")

    if x==48:

        await event.edit("🎶 മിഴിയറിയാതെ വന്നു നീ മിഴിയൂഞ്ഞാലിൽ... കനവറിയാതെയേതോ കിനാവു പോലെ... 🎶")
        
    if x==49:

        await event.edit("🎶 ചന്ദനച്ചോലയിൽ മുങ്ങിനീരാടിയെൻ ഇളമാൻ കിടാവേ ഉറക്കമായോ... 🎶")

    if x==50:

        await event.edit("🎶 കറുത്തപെണ്ണേ നിന്നെ കാണാഞ്ഞിട്ടൊരു നാളുണ്ടേ... 🎶")
     
    if x==51:

        await event.edit("🎶 താമരപ്പൂവിൽ വാഴും ദേവിയല്ലോ നീ... പൂനിലാക്കടവിൽ പൂക്കും പുണ്യമല്ലോ നീ... 🎶")

    if x==52:

        await event.edit("🎶 പാടം പൂത്തകാലം പാടാൻ വന്നു നീയും... 🎶")

    if x==53:

        await event.edit("🎶 രാജഹംസമേ മഴവിൽ കുടിലിൽ... സ്നേഹദൂതുമായ് വരുമോ... 🎶")

    if x==54:

        await event.edit("🎶 പത്തുവെളുപ്പിന് മുറ്റത്തു നിക്കണ കസ്തൂരി മുല്ലയ്ക്ക് കാത്തുകുത്ത്... എന്റെ കസ്തൂരി മുല്ലയ്ക്ക് കാത്തുകുത്ത്... 🎶")

    if x==55:
        
        await event.edit("🎶 മഞ്ഞൾ പ്രസാദവും നെറ്റിയിൽ ചാർത്തി... മഞ്ഞക്കുറിമുണ്ടു ചുറ്റി... 🎶")
        
    if x==56:
        
        await event.edit("🎶 അന്തിപ്പൊൻവെട്ടം കടലിൽ മെല്ലെത്താഴുമ്പോൾ... മാനത്തെ മുല്ലത്തറയില് മാണിക്യച്ചെപ്പ്... 🎶")
       
    if x==57:

        await event.edit("🎶 അമ്പലപ്പുഴെ ഉണ്ണിക്കണ്ണനോടു നീ... എന്തുപരിഭവം മെല്ലെയോതിവന്നുവോ... 🎶")

    if x==58:

        await event.edit("🎶 കുടജാദ്രിയിൽ കുടചൂടുമാ കോടമഞ്ഞുപോലെയീ പ്രണയം... തഴുകുന്നു, എന്നെ പുണരുന്നു... 🎶")

    if x==59:
        
        await event.edit("🎶 ശ്യാമാംബരം പുൽകുന്നൊരാ വെൺചന്ദ്രനായ് നിൻ പൂമുഖം... 🎶")
        
    if x==60:
        
        await event.edit("🎶 ശ്രീരാഗമോ തേടുന്നിതെൻ വീണതൻ പൊൻ തന്ത്രിയിൽ... 🎶")
        
    if x==61:
        
        await event.edit("🎶 എന്തിനു വേറൊരു സൂര്യോദയം... നീയെൻ പൊന്നുഷസ്സന്ധ്യയല്ലേ... 🎶")
        
    if x==62:
        
        await event.edit("🎶 അനുരാഗിണീ ഇതായെൻ കരളിൽ വിരിഞ്ഞ പൂക്കൾ... 🎶")

    if x==63:
        
        await event.edit("🎶 പാടാം നമുക്കു പാടാം... വീണ്ടുമൊരു പ്രേമഗാനം... 🎶")
        
    if x==64:
        
        await event.edit("🎶 അല്ലിമലർ കാവിൽ പൂരം കാണാൻ... അന്നു നമ്മൾ പോയി രാവിൽ നിലാവിൽ... 🎶")
    
    if x==65:
        
        await event.edit("🎶 കറുകവയൽ കുരുവീ... മുറിവാലൻ കുരുവീ... തളിർ വെറ്റിലയുണ്ടോ... വരദക്ഷിണ വെക്കാൻ... 🎶")
        
    if x==66:
        
        await event.edit("🎶 കുന്നിമണിച്ചെപ്പു തുറന്നെണ്ണി നോക്കും നേരം, പിന്നിൽവന്നു കണ്ണു പൊത്തും കള്ളനെങ്ങു പോയി... 🎶")
        
    if x==67:
        
        await event.edit("Not in a mood to sing. Sorry!")
