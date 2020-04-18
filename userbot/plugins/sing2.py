""" Sing a song... 
    Command .singint(finished)
            .singhi(pending)
            .singpu(pending)
    By @PhycoNinja13b """




from telethon import events

import asyncio

import os

import sys

import random

from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern=r"singint", outgoing=True))

async def _(event):

    if event.fwd_from:

        return

    await event.edit("Singing...")

    await asyncio.sleep(2)

    x=(random.randrange(1,33))

    if x==1:

        await event.edit("🎶 I'm in love with the shape of you \n We push and pull like a magnet do\n Although my heart is falling too \n I'm in love with your body \n And last night you were in my room \n And now my bedsheets smell like you \n Every day discovering something brand new 🎶  \n 🎶  I'm in love with your body \n Oh—I—oh—I—oh—I—oh—I \n I'm in love with your body \n Oh—I—oh—I—oh—I—oh—I \n I'm in love with your body \n Oh—I—oh—I—oh—I—oh—I \n I'm in love with your body 🎶 \n **-Shape of You**")

    if x==2:

        await event.edit("🎶 I've been reading books of old \n The legends and the myths \n Achilles and his gold \n Hercules and his gifts \n Spiderman's control \n And Batman with his fists \n And clearly I don't see myself upon that list 🎶 \n **-Something Just Like This **")

    if x==3:

        await event.edit("🎶 I don't wanna live forever \n 'Cause I know I'll be livin' in vain \n And I don't wanna fit wherever \n I just wanna keep callin' your name \n Until you come back home \n I just wanna keep callin' your name \n Until you come back home \n I just wanna keep callin' your name \n Until you come back home 🎶 \n **-I don't Wanna Live Forever **")

    if x==4:

        await event.edit("🎶 Oh, hush, my dear, it's been a difficult year \n And terrors don't prey on \n Innocent victims \n Trust me, darling, trust me darling \n It's been a loveless year \n I'm a man of three fears \n Integrity, faith and \n Crocodile tears \n Trust me, darling, trust me, darling 🎶 \n **-Bad Lier")

    if x==5:

        await event.edit("🎶 Walking down 29th and Park \n I saw you in another's arms \n Only a month we've been apart \n **You look happier** \n \n Saw you walk inside a bar \n He said something to make you laugh \n I saw that both your smiles were twice as wide as ours \n Yeah, you look happier, you do 🎶 \n **-Happier **")

    if x==6:

        await event.edit("🎶 I took the supermarket flowers from the windowsill \n I threw the day old tea from the cup \n Packed up the photo album Matthew had made \n Memories of a life that's been loved \n Took the get well soon cards and stuffed animals \n Poured the old ginger beer down the sink \n Dad always told me, 'don't you cry when you're down' \n But mum, there's a tear every time that I blink 🎶 \n **-Supermarket Flowers**")

    if x==7:

        await event.edit("🎶 And you and I we're flying on an aeroplane tonight \n We're going somewhere where the sun is shining bright \n Just close your eyes \n And let's pretend we're dancing in the street \n In Barcelona \n Barcelona \n Barcelona \n Barcelona 🎶 \n **-Barcelona **")    

    if x==8:

        await event.edit("🎶 Maybe I came on too strong \n Maybe I waited too long \n Maybe I played my cards wrong \n Oh, just a little bit wrong \n Baby I apologize for it \n \n I could fall, or I could fly \n Here in your aeroplane \n And I could live, I could die \n Hanging on the words you say \n And I've been known to give my all \n And jumping in harder than \n Ten thousand rocks on the lake 🎶 \n **-Dive**")

    if x==9:

        await event.edit("🎶 I found a love for me \n Darling just dive right in \n And follow my lead \n Well I found a girl beautiful and sweet \n I never knew you were the someone waiting for me \n 'Cause we were just kids when we fell in love \n Not knowing what it was \n \n I will not give you up this time \n But darling, just kiss me slow, your heart is all I own \n And in your eyes you're holding mine 🎶 \n **-Perfect**")

    if x==10:

        await event.edit("🎶 I was born inside a small town, I lost that state of mind \n Learned to sing inside the Lord's house, but stopped at the age of nine \n I forget when I get awards now the wave I had to ride \n The paving stones I played upon, they kept me on the grind \n So blame it on the pain that blessed me with the life 🎶 \n **-Eraser**")
     
    if x==11:

        await event.edit("🎶 Say, go through the darkest of days \n Heaven's a heartbreak away \n Never let you go, never let me down \n Oh, it's been a hell of a ride \n Driving the edge of a knife. \n Never let you go, never let me down \n \n Don't you give up, nah-nah-nah \n I won't give up, nah-nah-nah \n Let me love you \n Let me love you 🎶 \n **-Let me Love You**")

    if x==12:

        await event.edit("🎶 I'll stop time for you \n The second you say you'd like me to \n I just wanna give you the loving that you're missing \n Baby, just to wake up with you \n Would be everything I need and this could be so different \n Tell me what you want to do \n \n 'Cause I know I can treat you better \n Than he can \n And any girl like you deserves a gentleman 🎶 **-Treat You Better**")
    
    if x==13:

        await event.edit("🎶 You're the light, you're the night \n You're the color of my blood \n You're the cure, you're the pain \n You're the only thing I wanna touch \n Never knew that it could mean so much, so much \n You're the fear, I don't care \n 'Cause I've never been so high \n Follow me through the dark \n Let me take you past our satellites \n You can see the world you brought to life, to life \n \n So love me like you do, lo-lo-love me like you do \n Love me like you do, lo-lo-love me like you do 🎶 \n **-Love me Like you Do**")

    if x==14:

        await event.edit("🎶 Spent 24 hours \n I need more hours with you \n You spent the weekend \n Getting even, ooh ooh \n We spent the late nights \n Making things right, between us \n But now it's all good baby \n Roll that Backwood baby \n And play me close \n \n 'Cause girls like you \n Run around with guys like me \n 'Til sundown, when I come through \n I need a girl like you, yeah yeah 🎶 \n **-Girls Like You**")
        
    if x==15:

        await event.edit("🎶 Oh, angel sent from up above \n You know you make my world light up \n When I was down, when I was hurt \n You came to lift me up \n Life is a drink and love's a drug \n Oh, now I think I must be miles up \n When I was a river dried up \n You came to rain a flood 🎶**-Hymn for the Weekend ** ")

    if x==16:

        await event.edit("🎶 I've known it for a long time \n Daddy wakes up to a drink at nine \n Disappearing all night \n I don’t wanna know where he's been lying \n I know what I wanna do \n Wanna run away, run away with you \n Gonna grab clothes, six in the morning, go 🎶 \n **-Runaway **")
     
    if x==17:

        await event.edit("🎶 You were the shadow to my light \n Did you feel us \n Another start \n You fade away \n Afraid our aim is out of sight \n Wanna see us \n Alive 🎶 \n **-Faded**")

    if x==18:

        await event.edit("🎶 It's been a long day without you, my friend \n And I'll tell you all about it when I see you again \n We've come a long way from where we began \n Oh I'll tell you all about it when I see you again \n When I see you again 🎶 \n **-See you Again**")

    if x==19:

        await event.edit("🎶 I can swallow a bottle of alcohol and I'll feel like Godzilla \n Better hit the deck like the card dealer \n My whole squad's in here, walking around the party \n A cross between a zombie apocalypse and big Bobby 'The \n Brain' Heenan which is probably the \n Same reason I wrestle with mania 🎶 \n **-Godzilla**")

    if x==20:

        await event.edit("🎶 Yeah, I'm gonna take my horse to the old town road \n I'm gonna ride 'til I can't no more \n I'm gonna take my horse to the old town road \n I'm gonna ride 'til I can't no more (Kio, Kio) 🎶 \n **-Old Town Road**")

    if x==21:
        
        await event.edit("🎶 Oh-oh, ooh \n You've been runnin' round, runnin' round, runnin' round throwin' that dirt all on my name \n 'Cause you knew that I, knew that I, knew that I'd call you up \n You've been going round, going round, going round every party in L.A. \n 'Cause you knew that I, knew that I, knew that I'd be at one, oh 🎶 \n **-Attention **")
        
    if x==22:
        
        await event.edit("🎶 This hit, that ice cold \n Michelle Pfeiffer, that white gold \n This one for them hood girls \n Them good girls straight masterpieces \n Stylin', wilin', livin' it up in the city \n Got Chucks on with Saint Laurent \n Gotta kiss myself, I'm so pretty \n \n I'm too hot (hot damn) \n Called a police and a fireman \n I'm too hot (hot damn) \n Make a dragon wanna retire man \n I'm too hot (hot damn) \n Say my name you know who I am \n I'm too hot (hot damn) \n And my band 'bout that money, break it down 🎶 \n **-Uptown Funk**")
       
    if x==23:

        await event.edit("🎶 Just a young gun with the quick fuse \n I was uptight, wanna let loose \n I was dreaming of bigger things \n And wanna leave my own life behind \n Not a yes sir, not a follower \n Fit the box, fit the mold \n Have a seat in the foyer, take a number \n I was lightning before the thunder \n \n Thunder, feel the thunder \n Lightning then the thunder \n Thunder, feel the thunder \n Lightning then the thunder \n Thunder, thunder 🎶 \n **-Thunder**")

    if x==24:

        await event.edit("🎶 Oh, love \n How I miss you every single day \n When I see you on those streets \n Oh, love \n Tell me there's a river I can swim that will bring you back to me \n 'Cause I don't know how to love someone else \n I don't know how to forget your face \n No, love \n God, I miss you every single day and now you're so far away \n So far away 🎶 \n **-So Far Away**")

    if x==25:
        
        await event.edit("🎶 And if you feel you're sinking, I will jump right over \n Into cold, cold water for you \n And although time may take us into different places \n I will still be patient with you \n And I hope you know 🎶 \n **-Cold Water**")
        
    if x==26:
        
        await event.edit("🎶 When you feel my heat \n Look into my eyes \n It's where my demons hide \n It's where my demons hide \n Don't get too close \n It's dark inside \n It's where my demons hide \n It's where my demons hide 🎶 \n **-Demons**")
        
    if x==27:
        
        await event.edit("🎶 Who do you love, do you love now? \n I wanna know the truth (whoa) \n Who do you love, do you love now? \n I know it's someone new \n You ain't gotta make it easy, where you been sleepin'? 🎶 \n **-Who do  Love? **")
        
    if x==28:
        
        await event.edit("🎶 Your touch is magnetic \n 'Cause I can't forget it \n (There's a power pulling me back to you) \n And baby I'll let it \n 'Cause you're so magnetic I get it \n (When I'm waking up with you, oh) 🎶 \n **-Magnetic**")

    if x==29:
        
        await event.edit("🎶 Girl my body don't lie, I'm outta my mind \n Let it rain over me, I'm rising so high \n Out of my mind, so let it rain over me \n \n Ay ay ay, ay ay ay let it rain over me \n Ay ay ay, ay ay ay let it rain over me 🎶 \n **-Rain over Me**")
        
    if x==30:
        
        await event.edit("🎶 I miss the taste of a sweeter life \n I miss the conversation \n I'm searching for a song tonight \n I'm changing all of the stations \n I like to think that we had it all \n We drew a map to a better place \n But on that road I took a fall \n Oh baby why did you run away? \n \n I was there for you \n In your darkest times \n I was there for you \n In your darkest night 🎶 \n **-Maps**")
    
    if x==31:
        
        await event.edit("🎶 I wish—I wish that I was bulletproof, bulletproof \n I wish—I wish that I was bulletproof, bulletproof \n (Bullet-bulletproof, bullet-bullet-bulletproof) \n I'm trippin' on my words and my patience \n Writing every verse in a cadence \n To tell you how I feel, how I feel, how I feel (Yeah) \n This is how I deal, how I deal, how I deal (Yeah) \n With who I once was, now an acquaintance \n Think my confidence (My confidence) is in the basement \n Tryin' to keep it real, keep it real, keep it real (Yeah) \n 'Cause I'm not made of steel, made of steel 🎶 \n **-Bulletproof**")
        
    if x==32:
        
        await event.edit("🎶 You won't find him down on Sunset \n Or at a party in the hills \n At the bottom of the bottle \n Or when you're tripping on some pills \n When they sold you the dream you were just 16 \n Packed a bag and ran away \n And it's a crying shame you came all this way \n 'Cause you won't find Jesus in LA \n And it's a crying shame you came all this way \n 'Cause you won't find Jesus in LA 🎶 \n **-Jesus in LA**")
        
    if x==33:
        
        await event.edit("Not in a mood to sing. Sorry!")
