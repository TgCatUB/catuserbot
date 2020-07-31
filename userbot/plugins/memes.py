# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
#

""" Userbot module for having some fun with people. """

import sys
import asyncio
import random
import re
import time

from collections import deque

import requests
from telethon import events, functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

from cowpy import cow

from userbot import CMD_HELP 
from userbot.utils import register, admin_cmd
from userbot import ALIVE_NAME

BOTLOG = True
BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID

# ================= CONSTANT =================

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "@Sur_vivor"

RENDISTR = [
    "`I Know Uh ez Rendi Bhay Dont show Your Randi Pesa Here`",
    "`Jag Suna suna laage Sab #maderchod bhay`",
    "`you talking behind meh wew uh iz my fan now bhay`",
    "`Wanna pass in Life Goto BRAZZER.CAM BHAY`",
    "`Uh iz Pro i iz noob your boob is landi uh are Randi`",
    "`Sellers Nasa calling Uh bhay😆`",
    "`Badwoo ki yojna behan bna ke ch*da uh iz badwa its your yozja?`",
    "`CHAND PE CHADA HAI CHANDYAAN KA GHODA TERA NAAM HAI MANSUR TU HAI BEHAN KA LOD*😂`",
    "`Jab se dil lga baithe tanhai me maa chu*da baithe wo kho gyi kisi aur ke pyar hum apne hi jaato me aag lga baithe`",
    "`Chadii ke ander se lal pani kha se ata hai ky teri masuka ka bhosda bhi paan khata hai😂`",
    "`Sun bhosdi ke By anonyCrew MOHABBAT KE SIWA AUR BHI GAM HAI JAMANE ME BSDK GAND PAHAT JATI HAI PAISA KAMANE ME`",
    "`Thaan liya tha Sayri nhi krege Unka pichwada dekha Alfaaz nikal gye`",
    "`Ravivaar ko dekha Chand Ka Tukra Itna Baar Dekha par Jaath na Ukra`",
    "`Katal kro Tir se Talwar me Ky Rkkha hai Maal Chodo Sari Me Salwar me Ky Rkkha hai`",
]
NOOBSTR = [
    "`YOU PRO NIMBA DONT MESS WIDH MEH`",
    "`NOOB NIMBA TRYING TO BE FAMOUS KEK`",
    "`Sometimes one middle finger isn’t enough to let someone know how you feel. That’s why you have two hands`",
    "`Some Nimbas need to open their small minds instead of their big mouths`",
    "`UH DONT KNOW MEH SO STAY AWAY LAWDE`",
    "`Kysa kysaaaa haaan? Phir MAAR nhi Khayega tu?`",
    "`Zikr Jinka hota hai galiyo meh woh bhosdika ajj paya gya naliyo me`",
]

INSULT_STRINGS = [
    "Active Volcano is the best swimming pool for you.",
    "Alas! Your neurotransmitters are no more working.",
    "Are you crazy you fool.",
    "As an outsider, what do you think of the human race?",
    "Believe me you are not normal.",
    "Bot rule 420 section 69 prevents me from replying to stupid nubfuks like you.",
    "Bot rule 544 section 9 prevents me from replying to stupid humans like you.",
    "Brains aren't everything. In your case they're nothing.",
    "Come back and talk to me when your I.Q. exceeds your age.",
    "Command not found. Just like your brain.",
    "Dance naked on a couple of HT wires.",
    "Don't drink and type.",
    "Do you realize you are making a fool of yourself? Apparently not.",
    "Everyone has the right to be stupid but you are abusing the privilege.",
    "Go Green! Stop inhaling Oxygen.",
    "God was searching for you. You should leave to meet him.",
    "Have you tried shooting yourself as high as 100m using a canon.",
    "Head shots are fun. Get yourself one.",
    "Hit Uranium with a slow moving neutron in your presence. It will be a worthwhile experience.",
    "How about you stop breathing for like 1 day? That'll be great.",
    "I'm not saying you're stupid, I'm just saying you've got bad luck when it comes to thinking.",
    "I'm sorry I hurt your feelings when I called you stupid. I thought you already knew that.",
    "I bet your brain feels as good as new, seeing that you never use it.",
    "I don't know what makes you so stupid, but it really works.",
    "If I wanted to kill myself I'd climb your ego and jump to your IQ.",
    "If you’re talking behind my back then you’re in a perfect position to kiss my a**!.",
    "I heard phogine is poisonous but i guess you wont mind inhaling it for fun.",
    "I think you should go home or better a mental asylum.",
    "I would ask you how old you are but I know you can't count that high.",
    "Keep talking, someday you'll say something intelligent!.......(I doubt it though)",
    "Launch yourself into outer space while forgetting oxygen on Earth.",
    "Ordinarily people live and learn. You just live.",
    "Owww ... Such a stupid idiot.",
    "People like you are the reason we have middle fingers.",
    "Pick up a gun and shoot yourself.",
    "Shock me, say something intelligent.",
    "Sorry, we do not sell brains.",
    "Stop talking BS and jump in front of a running bullet train.",
    "Stupidity is not a crime so you are free to go.",
    "Try bathing with Hydrochloric Acid instead of water.",
    "Try jumping from a hundred story building but you can do it only once.",
    "Try playing catch and throw with RDX its fun.",
    "Try provoking a tiger while you both are in a cage.",
    "Try this: if you hold your breath underwater for an hour, you can then hold it forever.",
    "Try to spend one day in a coffin and it will be yours forever.",
    "Volunteer for target in an firing range.",
    "What language are you speaking? Cause it sounds like bullshit.",
    "When your mom dropped you off at the school, she got a ticket for littering.",
    "You are proof that evolution CAN go in reverse.",
    "You can be the first person to step on sun. Have a try.",
    "You can stay underwater for the rest of your life without coming back up.",
    "You can type better than that.",
    "You could make a world record by jumping from a plane without parachute.",
    "You didn't evolve from apes, they evolved from you.",
    "Your IQ's lower than your shoe size.",
    "Your enzymes are meant to digest rat poison.",
    "You should Volunteer for target in an firing range.",
    "You should donate your brain seeing that you never used it.",
    "You should paint yourself red and run in a bull marathon.",
    "You should try holding TNT in your mouth and igniting it.",
    "You should try hot bath in a volcano.",
    "You should try playing snake and ladders, with real snakes and no ladders.",
    "You should try sleeping forever.",
    "You should try swimming with great white sharks.",
    "You should try tasting cyanide.",
    "You’re so ugly that when you cry, the tears roll down the back of your head…just to avoid your face.",
    "Zombies eat brains... you're safe.",
    "give your 100%. Now, go donate blood."
]

UWUS = [
    "(・`ω´・)",
    ";;w;;",
    "owo",
    "UwU",
    ">w<",
    "^w^",
    r"\(^o\) (/o^)/",
    "( ^ _ ^)∠☆",
    "(ô_ô)",
    "~:o",
    ";-;",
    "(*^*)",
    "(>_",
    "(♥_♥)",
    "*(^O^)*",
    "((+_+))",
]

FACEREACTS = [
    "ʘ‿ʘ",
    "ヾ(-_- )ゞ",
    "(っ˘ڡ˘ς)",
    "(´ж｀ς)",
    "( ಠ ʖ̯ ಠ)",
    "(° ͜ʖ͡°)╭∩╮",
    "(ᵟຶ︵ ᵟຶ)",
    "(งツ)ว",
    "ʚ(•｀",
    "(っ▀¯▀)つ",
    "(◠﹏◠)",
    "( ͡ಠ ʖ̯ ͡ಠ)",
    "( ఠ ͟ʖ ఠ)",
    "(∩｀-´)⊃━☆ﾟ.*･｡ﾟ",
    "(⊃｡•́‿•̀｡)⊃",
    "(._.)",
    "{•̃_•̃}",
    "(ᵔᴥᵔ)",
    "♨_♨",
    "⥀.⥀",
    "ح˚௰˚づ ",
    "(҂◡_◡)",
    "ƪ(ړײ)‎ƪ​​",
    "(っ•́｡•́)♪♬",
    "◖ᵔᴥᵔ◗ ♪ ♫ ",
    "(☞ﾟヮﾟ)☞",
    "[¬º-°]¬",
    "(Ծ‸ Ծ)",
    "(•̀ᴗ•́)و ̑̑",
    "ヾ(´〇`)ﾉ♪♪♪",
    "(ง'̀-'́)ง",
    "ლ(•́•́ლ)",
    "ʕ •́؈•̀ ₎",
    "♪♪ ヽ(ˇ∀ˇ )ゞ",
    "щ（ﾟДﾟщ）",
    "( ˇ෴ˇ )",
    "눈_눈",
    "(๑•́ ₃ •̀๑) ",
    "( ˘ ³˘)♥ ",
    "ԅ(≖‿≖ԅ)",
    "♥‿♥",
    "◔_◔",
    "⁽⁽ଘ( ˊᵕˋ )ଓ⁾⁾",
    "乁( ◔ ౪◔)「      ┑(￣Д ￣)┍",
    "( ఠൠఠ )ﾉ",
    "٩(๏_๏)۶",
    "┌(ㆆ㉨ㆆ)ʃ",
    "ఠ_ఠ",
    "(づ｡◕‿‿◕｡)づ",
    "(ノಠ ∩ಠ)ノ彡( \\o°o)\\",
    "“ヽ(´▽｀)ノ”",
    "༼ ༎ຶ ෴ ༎ຶ༽",
    "｡ﾟ( ﾟஇ‸இﾟ)ﾟ｡",
    "(づ￣ ³￣)づ",
    "(⊙.☉)7",
    "ᕕ( ᐛ )ᕗ",
    "t(-_-t)",
    "(ಥ⌣ಥ)",
    "ヽ༼ ಠ益ಠ ༽ﾉ",
    "༼∵༽ ༼⍨༽ ༼⍢༽ ༼⍤༽",
    "ミ●﹏☉ミ",
    "(⊙_◎)",
    "¿ⓧ_ⓧﮌ",
    "ಠ_ಠ",
    "(´･_･`)",
    "ᕦ(ò_óˇ)ᕤ",
    "⊙﹏⊙",
    "(╯°□°）╯︵ ┻━┻",
    r"¯\_(⊙︿⊙)_/¯",
    "٩◔̯◔۶",
    "°‿‿°",
    "ᕙ(⇀‸↼‶)ᕗ",
    "⊂(◉‿◉)つ",
    "V•ᴥ•V",
    "q(❂‿❂)p",
    "ಥ_ಥ",
    "ฅ^•ﻌ•^ฅ",
    "ಥ﹏ಥ",
    "（ ^_^）o自自o（^_^ ）",
    "ಠ‿ಠ",
    "ヽ(´▽`)/",
    "ᵒᴥᵒ#",
    "( ͡° ͜ʖ ͡°)",
    "┬─┬﻿ ノ( ゜-゜ノ)",
    "ヽ(´ー｀)ノ",
    "☜(⌒▽⌒)☞",
    "ε=ε=ε=┌(;*´Д`)ﾉ",
    "(╬ ಠ益ಠ)",
    "┬─┬⃰͡ (ᵔᵕᵔ͜ )",
    "┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻",
    r"¯\_(ツ)_/¯",
    "ʕᵔᴥᵔʔ",
    "(`･ω･´)",
    "ʕ•ᴥ•ʔ",
    "ლ(｀ー´ლ)",
    "ʕʘ̅͜ʘ̅ʔ",
    "（　ﾟДﾟ）",
    r"¯\(°_o)/¯",
    "(｡◕‿◕｡)",
]

RUNSREACTS = [
    "`Runs to Thanos`",
    "`Runs far, far away from earth`",
    "`Running faster than supercomputer, cuzwhynot`",
    "`Runs to SunnyLeone`",
    "`ZZzzZZzz... Huh? what? oh, just them again, nevermind.`",
    "`Look out for the wall!`",
    "`Don't leave me alone with them!!`",
    "`You run, you die.`",
    "`Jokes on you, I'm everywhere`",
    "`You could also try /kickme, I hear that's fun.`",
    "`You can run, but you can't hide.`",
    "`I'm behind you...`",
    "`We can do this the easy way, or the hard way.`",
    "`You just don't get it, do you?`",
    "`Yeah, you better run!`",
    "`I'd run faster if I were you.`",
    "`May the odds be ever in your favour.`",
    "`Famous last words.`",
    "`And they disappeared forever, never to be seen again.`",
    "`\"Oh, look at me! I'm so cool, I can run from a bot!\" - this person`",
    "`Yeah yeah, just tap /kickme already.`",
    "`Here, take this ring and head to Mordor while you're at it.`",
    "`Legend has it, they're still running...`",
    "`Unlike Harry Potter, your parents can't protect you from me.`",
    "`Fear leads to anger. Anger leads to hate. Hate leads to suffering. If you keep running in fear, you might`"
    "`Be the next Vader.`",
    "`Keep it up, not sure we want you here anyway.`",
    "`You're a wiza- Oh. Wait. You're not Harry, keep moving.`",
    "`NO RUNNING IN THE HALLWAYS!`",
    "`Hasta la vista, baby.`",
    "`Who let the dogs out?`",
    "`My milkshake brings all the boys to yard... So run faster!`",
    "`A long time ago, in a galaxy far far away... Someone would've cared about that. Not anymore though.`",
    "`Hey, look at them! They're running from the inevitable banhammer... Cute.`",
    "`What are you running after, a white rabbit?`",
    "`As The Doctor would say... RUN!`",
    "`Running a marathon...there's an app for that.`",
    "`Where do you think you're going?`",
    "`Huh? what? did they get away?`",
    "`Get back here!`",
    "`Not so fast...`",
    "`You're gonna regret that...`",
    "`Go bother someone else, no-one here cares.`",
    "`Is that all you've got?`",    
    "`You've got company!`",
    "`We can do this the easy way, or the hard way.`",    
    "`Please, remind me how much I care?`",    
    "`That's definitely the droid we're looking for.`",       
    "`Multiple calculations later, I have decided my interest in your shenanigans is exactly 0.`",              
    "`It's funny, because no one cares.`",
    "`Ah, what a waste. I liked that one.`",
    "`Frankly, my dear, I don't give a damn.`",    
    "`You can't HANDLE the truth!`",
    "`Han shot first. So will I.`",
]

RAPE_STRINGS = [
     "`Rape Done Drink The Cum`",
     "`EK baat yaad rkhio, Chut ka Chakkar matlab maut se takkar`",
     "`The user has been successfully raped`",
     "`Dekho Bhaiyya esa hai! Izzat bachailo apni warna Gaand maar lenge tumhari`",
     "`Relax your Rear, ders nothing to fear,The Rape train is finally here`",
     "`Rape coming... Raped! haha 😆`",
     "`Kitni baar Rape krvyega mujhse?`",
     "`Tu Randi hai Sabko pta hai😂`",
     "`Don't rape too much bossdk, else problem....`",
     "`Tu sasti rendi hai Sabko pta hai😂`",
     "`Lodu Andha hai kya Yaha tera rape ho raha hai aur tu abhi tak yahi gaand mara raha hai lulz`",
] 
ABUSE_STRINGS = [
       "`Chutiya he rah jaye ga`",
       "`Ja be Gaandu`",
       "`Muh Me Lega Bhosdike ?`",
       "`Kro Gandu giri kam nhi toh Gand Maar lenge tumhari hum😂`",
       "`Suno Lodu Jyda muh na chalo be muh me lawda pel Diyaa jayega`",
       "`Sharam aagyi toh aakhe juka lijia land me dam nhi hai apke toh Shilajit kha lijia`",
       "`Kahe Rahiman Kaviraaj C**t Ki Mahima Aisi,L**d Murjha Jaaye Par Ch**t Waisi Ki Waisi`",
       "`Chudakkad Raand Ki Ch**T Mein Pele L*Nd Kabeer, Par Aisa Bhi Kya Choda Ki Ban Gaye Fakeer`",
]
GEY_STRINGS = [
     "`you gey bsdk`",
     "`you gey`",
     "`you gey in the house`",
     "`you chakka`",
     "`Bhago BC! Chakka aya`",
     "`you gey gey gey gey gey gey gey gey`",
     "`you gey go away`",
]
PRO_STRINGS = [
     "`This gey is pro as phack.`",
     "`Proness Lebel: 6969696969`",
     "`Itna pro banda dekhlia bc, ab to marna hoga.`",
     "`U iz pro but i iz ur DAD, KeK`",
     "`NOOB NIMBA TRYING TO BE FAMOUS KEK`",
     "`Sometimes one middle finger isnâ€™t enough to let someone know how you feel. Thatâ€™s why you have two hands`",
     "`Some Nimbas need to open their small minds instead of their big mouths`",
     "`UH DONT KNOW MEH SO STAY AWAY LAWDE`",
     "`Kysa kysaaaa haaan? Phir MAAR nhi Khayega tu?`",
     "`Zikr Jinka hota hai galiyo meh woh bhosdika ajj paya gya naliyo me`",

]
CHU_STRINGS = [
     "`Taare hai Asmaan me very very bright jaat na jla bskd dekh le apni hight.`",
     "`jindagi ki na toote lari iski lulli hoti nhi khadi`",
     "`Kbhi kbhi meri dil me khyaal ata hai ayse chutiyo ko kon paida kr jata hai😂.`",
     "`Saawan ka mahina pawan kare shor jake gand mara bskd kahi aur.`", 
     "`Dil ke armaa ansuon me beh jaye tum bskd ke chutiye hi reh gye.`",
     "`Ishq Se Tabiyat Ne Zeest Ka Mazaa aya maine is lodu ko randi khane me paya.`",
     "`Mirza galib ki yeh khani hai tu bhosdika hai yeh sab ki jubani hai.`",
]
FUK_STRINGS = [
   "`It's better to let someone think you are an Idiot than to open your mouth and prove it.`",
   "`Talking to a liberal is like trying to explain social media to a 70 years old`",
   "`CHAND PE HAI APUN LAWDE.`",
   "`Pehle main tereko chakna dega, fir daru pilayega, fir jab aap dimag se nahi L*nd se sochoge, tab bolega..`",
   "`Pardhan mantri se number liya, parliament apne :__;baap ka hai...`",
   "`Cachaa Ooo bhosdi wale Chacha`",
   "`Aaisi Londiya Chodiye, L*nd Ka Aapa Khoye, Auro Se Chudi Na Ho, Biwi Wo Hi Hoye`",
   "`Nachoo Bhosdike Nachoo`",
   "`Jinda toh jaat ke baal bhi hai`",
   "`Sab ko pta tu randi ka baccha hai (its just a joke)`", 
]
THANOS_STRINGS = [
     "`Mashoor Rand, Ne Arz Kiya Hai. Aane Wale Aate Hai, Jaane Wale Jaate Hai. Yaade Bas Unki Reh Jaati Hai, Jo G**Nd Sujaa Ke Jaate Hai`",
     "`Pani kam hai matkey me ga*d mardunga teri ek jatke me`",
     "`Aand kitne bhi bade ho, lund ke niche hi rehte hai`",
     "`Tum Ameer hum gareeb hum jhopdiwale Tum bhosiwale`",
     "`Sisi Bhari Gulab ki padi palang ke pass chodne wale chod gye ab q baitha udaas`",
     "`Phuloo Ka Raja Gulaab Kaato me Rehta hai Jeewan ka Nirmata jaato me rehta hai😂`",
     "`Chude hue maal ko yaad mt krna Jo Chut na de usse kabhi friyad mt karna jise chudna hai wo chud ke rhegi bekar me muth maar ke apni jindagi barbaad mt krna`",
     "`Gand mare gandu Chut mare Chutiya Sabse accha mutti 2 mint me chutti😛`",
     "`Marzi Ka Sex Pap Nahi Hota.. Piche Se Dalne Wala Kabhi Baap Nahi Hota.. Condom Zarur Lagana Mere Dost Qki.. Sex K Waqt Popat Ke Pass Dimag Nahi Hota.`",
     "`Uss Ne Hothon Se Chhu Kar Lowd* Pe Nasha Kar Diya; Lu*D Ki Baat To Aur Thi, Uss Ne To Jhato* Ko Bhi Khada Kar Diya!`",
]
ABUSEHARD_STRING = [
	"`Madarchod Randi ke bacche.Oye bosdike madarchod bhen ke lode tere gand me lohe ka danda garam karke dalu randwe tujhetho gali ke kutte gand pe chut rakh ke katenge me bata raha hu tere lode pe madhu makkhi Katelode ke ando pe Road roller chale tu kab bathroom me muthne Jaye tho Tera loda ghir Jaye fir tere ando me se lizard ke bacche nikle teko kidnap Kare aur childporn banaye maa ke chuttad ke lode tere saat Johnny sins rape Kare aur jab wo teko anal de tab loda andar fas Jaye bkl tere jhaat pe waxing karunga me dhek lio fir jab tu chillayega na tab tere muh me Mai gai ka gobar dalunga sale tere gand ke balo pe tel laga ke jala du me teko Anaconda leke gand me dalu tho muh se nikle maa ke lode hamesha chutiyo jaisa bartav kartha he tu maa ke Dai chawal drugs tere gand Me dalunga thi tatti nahi nikle maa darchod kabhi teko Marne ka mouka mil gaya na tho bas I'll do my best to get that tatti outof you aur tere jaise chutio ko is duniya me jagaha bhi nahi maa ke lode bandarchod tere gand me chitiya Kate wo bhi bullet ants maadarchod samj nahi aaraha tere baap NE teko kya khake paida kiya Tha kesa chutiya he tu rand ke bacche teko shadi me khana khane na mile teko gand pe 4 thappad mare sab log aur blade se likhe I want anal madarchod bosdike maccharki tatte ke baal chutiye maa ke chut pe ghode ka Lund tere gand me jaltha hu koila Dale bhen ke lode MAA KI CHUT MAI TALWAR DUNGA BC CHUT FAT JAEGI AUR USME SE ITNA KHOON NIKLEGA MZA AJAEGA DEKHNE KA SALE MAA KE BHOSDE SE BAHR AJA FIR BAAP SE ZUBAN DA TERI MAA KI CHUT CHOD CHOD KE BHOSDABNADU MADARCHOD AUR USKE UPAR CENENT LAGADU KI TERE JESA GANDU INSAAN KABHI BAHR NA A SKE ESI GANDI CHUT MAI SE LODA LASUN MADRCHOD TERI MAA KI CHUT GASTI AMA KA CHUTIA BACHA TERI MAA KO CHOD CHOD K PAGAL KAR DUNGA MAA K LODY KISI SASTIII RANDII K BACHY TERI MAA KI CHOOT MAIN TEER MAARUN GANDU HARAMI TERI COLLEGE JATI BAJI KA ROAD PEY RAPE KARONGANDU KI OLAAD HARAM KI NASAL PAPA HUN TERA BHEN PESH KAR AB PAPA KO TERI MAA KKALE KUSS MAIN KIS`",
	"`Main roz teri behno ki banjar chut me apna lawda daalke andar haryali lata tha magar aaj unke ke baare me sunke mujhe bhut afsos huwa..ki unko ab bada loudha chahye..ab mera balatkaaari lawda lagataar 4 ghante tk apne muh me kon rakhega..vo teri behne hi thi jo apni kaali magar rasilli chut mere saamne khol deti aur zameen pe naagin ki tarah rengne lgti thi jaise ki kisine unki chut pe naariyal tod diya ho vo b bada wala mumbai ka naariyal..apni chennal maa ko b nhi bhej rahe mere paas to main kaixe tum logo se vaada karu ki main teri maa chodd dungaw..ab agar tun sach me chahta hai ki main tum dono k mc ki chut me dhammal karu to mera lawda apne muh me rakho aur kaho Sameer hamare sage papa hain... Aur agar tb b the apni maa ki kaali chut mere saamne nahi rakhi to tumhare ghar me ghuske tumhari maa ka balatkaar kar dungaw jaixe delhi me huwa tha...ab teri chudi hui kuttiyo ki tarah apni gaand hilaate hue mere aage kalapna mt ni to tumhari fatti bhoxdi me 100 ched karunga`",
	"`Taare hai Asmaan me very very bright jaat na jla bskd dekh le apni hight.`",
        "`Zindagi ki na toote lari iski lulli hoti nhi khadi`",
        "`Kbhi kbhi meri dil me khyaal ata hai ayse chutiyo ko kon paida kr jata hai😂.`",
        "`Saawan ka mahina pawan kare shor jake gand mara bskd kahi aur.`", 
        "`Dil ke armaa ansuon me beh jaye tum bskd ke chutiye hi reh gye.`",
        "`Ishq Se Tabiyat Ne Zeest Ka Mazaa aya maine is lodu ko randi khane me paya.`",
        "`Mirza galib ki yeh khani hai tu bhosdika hai yeh sab ki jubani hai.`",
	"`Mashoor Rand, Ne Arz Kiya Hai. Aane Wale Aate Hai, Jaane Wale Jaate Hai. Yaade Bas Unki Reh Jaati Hai, Jo G**Nd Sujaa Ke Jaate Hai`",
        "`Pani kam hai matke me gand marlunga jhatke me.`",
        "`Aand kitne bhi bade ho, lund ke niche hi rehte hai`",
        "`Tum Ameer hum gareeb hum jhopdiwale Tum bhosiwale`",
        "`Sisi Bhari Gulab ki padi palang ke pass chodne wale chod gye ab q baitha udaas`",
        "`Phuloo Ka Raja Gulaab Kaato me Rehta hai Jeewan ka Nirmata jaato me rehta hai😂`",
        "`Chude hue maal ko yaad mt krna Jo Chut na de usse kabhi friyad mt karna jise chudna hai wo chud ke rhegi bekar me muth maar ke apni jindagi barbaad mt krna`",
        "`Gand mare gandu Chut mare Chutiya Sabse accha mutti 2 mint me chutti😛`",
        "`Marzi Ka Sex Pap Nahi Hota.. Piche Se Dalne Wala Kabhi Baap Nahi Hota.. Condom Zarur Lagana Mere Dost Qki.. Sex K Waqt Popat Ke Pass Dimag Nahi Hota.`",
        "`Uss Ne Hothon Se Chhu Kar Lowd* Pe Nasha Kar Diya; Lu*D Ki Baat To Aur Thi, Uss Ne To Jhato* Ko Bhi Khada Kar Diya!`",
]
HELLOSTR = [
    "`Hi !`",
    "`‘Ello, gov'nor!`",
    "`What’s crackin’?`",
    "`‘Sup, homeslice?`",
    "`Howdy, howdy ,howdy!`",
    "`Hello, who's there, I'm talking.`",
    "`You know who this is.`",
    "`Yo!`",
    "`Whaddup.`",
    "`Greetings and salutations!`",
    "`Hello, sunshine!`",
    "`Hey, howdy, hi!`",
    "`What’s kickin’, little chicken?`",
    "`Peek-a-boo!`",
    "`Howdy-doody!`",
    "`Hey there, freshman!`",
    "`I come in peace!`",
    "`Ahoy, matey!`",
    "`Hiya!`",
    "`Oh retarded gey! Well Hello`",
]

SHGS = [
    "┐(´д｀)┌",
    "┐(´～｀)┌",
    "┐(´ー｀)┌",
    "┐(￣ヘ￣)┌",
    "╮(╯∀╰)╭",
    "╮(╯_╰)╭",
    "┐(´д`)┌",
    "┐(´∀｀)┌",
    "ʅ(́◡◝)ʃ",
    "ლ(ﾟдﾟლ)",
    "┐(ﾟ～ﾟ)┌",
    "┐('д')┌",
    "ლ｜＾Д＾ლ｜",
    "ლ（╹ε╹ლ）",
    "ლ(ಠ益ಠ)ლ",
    "┐(‘～`;)┌",
    "ヘ(´－｀;)ヘ",
    "┐( -“-)┌",
    "乁༼☯‿☯✿༽ㄏ",
    "ʅ（´◔౪◔）ʃ",
    "ლ(•ω •ლ)",
    "ヽ(゜～゜o)ノ",
    "ヽ(~～~ )ノ",
    "┐(~ー~;)┌",
    "┐(-。ー;)┌",
    "¯\_(ツ)_/¯",
    "¯\_(⊙_ʖ⊙)_/¯",
    "乁ʕ •̀ ۝ •́ ʔㄏ",
    "¯\_༼ ಥ ‿ ಥ ༽_/¯",
    "乁( ⁰͡  Ĺ̯ ⁰͡ ) ㄏ",
]

CRI = [
    "أ‿أ",
    "╥﹏╥",
    "(;﹏;)",
    "(ToT)",
    "(┳Д┳)",
    "(ಥ﹏ಥ)",
    "（；へ：）",
    "(T＿T)",
    "（πーπ）",
    "(Ｔ▽Ｔ)",
    "(⋟﹏⋞)",
    "（ｉДｉ）",
    "(´Д⊂ヽ",
    "(;Д;)",
    "（>﹏<）",
    "(TдT)",
    "(つ﹏⊂)",
    "༼☯﹏☯༽",
    "(ノ﹏ヽ)",
    "(ノAヽ)",
    "(╥_╥)",
    "(T⌓T)",
    "(༎ຶ⌑༎ຶ)",
    "(☍﹏⁰)｡",
    "(ಥ_ʖಥ)",
    "(つд⊂)",
    "(≖͞_≖̥)",
    "(இ﹏இ`｡)",
    "༼ಢ_ಢ༽",
    "༼ ༎ຶ ෴ ༎ຶ༽",
]

# ===========================================


@borg.on(admin_cmd(outgoing=True, pattern=r"(\w+)say (.*)"))
async def univsaye(cowmsg):
        arg = cowmsg.pattern_match.group(1).lower()
        text = cowmsg.pattern_match.group(2)

        if arg == "cow":
            arg = "default"
        if arg not in cow.COWACTERS:
            return
        cheese = cow.get_cow(arg)
        cheese = cheese()

        await cowmsg.edit(f"`{cheese.milk(text).replace('`', '´')}`")
			  
			  
@register(outgoing=True, pattern="^:/$")	 
async def kek(keks):
    if not keks.text[0].isalpha() and keks.text[0] not in ("/", "#", "@", "!"):
        """ Check yourself ;)"""
        uio = ["/", "\\"]
        for i in range(1, 15):
            time.sleep(0.3)
            await keks.edit(":" + uio[i % 2])
			  
@register(outgoing=True, pattern="^-_-$")
async def lol(lel):
    if not lel.text[0].isalpha() and lel.text[0] not in ("/", "#", "@", "!"):
        """ Ok... """
        okay = "-_-"
        for _ in range(10):
            okay = okay[:-1] + "_-"
            await lel.edit(okay)			  

@borg.on(admin_cmd(outgoing=True, pattern="(yes|no|maybe|decide)$"))
async def decide(event):
    decision = event.pattern_match.group(1).lower()
    message_id = event.reply_to_msg_id if event.reply_to_msg_id else None
    if decision != "decide":
        r = requests.get(f"https://yesno.wtf/api?force={decision}").json()
    else:
        r = requests.get(f"https://yesno.wtf/api").json()
    await event.delete()
    await event.client.send_message(event.chat_id,
                                    str(r["answer"]).upper(),
                                    reply_to=message_id,
                                    file=r["image"])
			  
			  
@register(outgoing=True, pattern="^;_;")
async def fun(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        t = ";__;"
        for j in range(10):
            t = t[:-1] + "_;"
            await e.edit(t)
			  
@borg.on(admin_cmd(outgoing=True, pattern="cry$"))
async def cry(e):
        await e.edit(random.choice(CRI))
		     
@borg.on(admin_cmd(outgoing=True, pattern="insult$"))
async def insult(e):
        await e.edit(random.choice(INSULT_STRINGS))


			  
@borg.on(admin_cmd(outgoing=True, pattern="repo$"))
async def source(e):
	await e.edit("Click [here](https://github.com/Sur-vivor/CatUserbot) to open this lit af repo.")
			  
		     
@borg.on(admin_cmd(outgoing=True, pattern="hey$"))
async def hoi(hello):
        await hello.edit(random.choice(HELLOSTR))
			  

			  			  
@borg.on(admin_cmd(outgoing=True, pattern="rape$"))
async def raping (raped):
        index = random.randint(0, len(RAPE_STRINGS) - 1)
        reply_text = RAPE_STRINGS[index]
        await raped.edit(reply_text)
			  			  
@borg.on(admin_cmd(outgoing=True, pattern="pro$"))
async def proo (pros):
        index = random.randint(0, len(PRO_STRINGS) - 1)
        reply_text = PRO_STRINGS[index]
        await pros.edit(reply_text)

@borg.on(admin_cmd(outgoing=True, pattern="fuck$"))
async def chutiya (fuks):
        index = random.randint(0, len(CHU_STRINGS) - 1)
        reply_text = FUK_STRINGS[index]
        await fuks.edit(reply_text)

			  			  
@borg.on(admin_cmd(outgoing=True, pattern="thanos$"))
async def thanos (thanos):
        index = random.randint(0, len(THANOS_STRINGS) - 1)
        reply_text = THANOS_STRINGS[index]
        await thanos.edit(reply_text)	
			  
@borg.on(admin_cmd(outgoing=True, pattern="abusehard$"))
async def fuckedd (abusehard):
        index = random.randint(0, len(ABUSEHARD_STRING) - 1)
        reply_text = ABUSEHARD_STRING[index]
        await abusehard.edit(reply_text)
			  
@register(outgoing=True, pattern="^.gey$")
async def geys (geyed):
        index = random.randint(0, len(GEY_STRINGS) - 1)
        reply_text = GEY_STRINGS[index]
        await geyed.edit(reply_text)
			  
			  
@borg.on(admin_cmd(outgoing=True, pattern="abuse$"))
async def abusing (abused):
        index = random.randint(0, len(ABUSE_STRINGS) - 1)
        reply_text = ABUSE_STRINGS[index]
        await abused.edit(reply_text)


@borg.on(admin_cmd(outgoing=True, pattern="owo (.*)"))
async def faces(owo):
        textx = await owo.get_reply_message()
        message = owo.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await owo.edit("` UwU no text given! `")
            return

        reply_text = re.sub(r"(r|l)", "w", message)
        reply_text = re.sub(r"(R|L)", "W", reply_text)
        reply_text = re.sub(r"n([aeiou])", r"ny\1", reply_text)
        reply_text = re.sub(r"N([aeiouAEIOU])", r"Ny\1", reply_text)
        reply_text = re.sub(r"\!+", " " + random.choice(UWUS), reply_text)
        reply_text = reply_text.replace("ove", "uv")
        reply_text += " " + random.choice(UWUS)
        await owo.edit(reply_text)


@borg.on(admin_cmd(outgoing=True, pattern="freact$"))
async def react_meme(react):
        await react.edit(random.choice(FACEREACTS))


@borg.on(admin_cmd(outgoing=True, pattern="shg$"))
async def shrugger(shg):
        await shg.edit(random.choice(SHGS))


@borg.on(admin_cmd(outgoing=True, pattern="runs$"))
async def runner_lol(run):
        await run.edit(random.choice(RUNSREACTS))

@borg.on(admin_cmd(outgoing=True, pattern="noob$"))
async def metoo(hahayes):
        await hahayes.edit(random.choice(NOOBSTR))
			  
@borg.on(admin_cmd(outgoing=True, pattern="rendi$"))
async def metoo(hahayes):
        await hahayes.edit(random.choice(RENDISTR))
			 			  
@borg.on(admin_cmd(outgoing=True, pattern="oof$"))
async def Oof(e):
        t = "Oof"
        for j in range(15):
            t = t[:-1] + "of"
            await e.edit(t)

@borg.on(admin_cmd(outgoing=True, pattern="10iq$"))
async def iqless(e):
        await e.edit("♿")

@borg.on(admin_cmd(pattern="ccry$"))
async def cry(e):
        await e.edit("(;´༎ຶД༎ຶ`)")			  

@borg.on(admin_cmd(outgoing=True, pattern="clap(?: |$)(.*)"))
async def claptext(event):
    textx = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif textx.message:
        query = textx.message
    else:
        await event.edit("Hah, I don't clap pointlessly!")
        return  
    reply_text = "👏 "
    reply_text += query.replace(" ", " 👏 ")
    reply_text += " 👏"
    await event.edit(reply_text)   


@borg.on(admin_cmd(outgoing=True, pattern="smk(?: |$)(.*)"))
async def smrk(smk):
    textx = await smk.get_reply_message()
    if event.pattern_match.group(1):
        message = event.pattern_match.group(1)
    elif textx.message:
        message = textx.message
    else:
        await smk.edit("ツ")
        return			  
    if message == 'dele':
        await smk.edit( message +'te the hell' + "ツ" )
        await smk.edit("ツ")
    else:
        smirk = " ツ"
        reply_text = message + smirk
        await smk.edit(reply_text)


@borg.on(admin_cmd(outgoing=True, pattern="bt$"))
async def bluetext(bt_e):
    """ Believe me, you will find this useful. """
    if bt_e.is_group:
        await bt_e.edit(
            "/BLUETEXT /MUST /CLICK.\n"
            "/ARE /YOU /A /STUPID /ANIMAL /WHICH /IS /ATTRACTED /TO /COLOURS?")
			  
@borg.on(admin_cmd(outgoing=True, pattern="lfy (.*)"))
async def let_me_google_that_for_you(lmgtfy_q):
        textx = await lmgtfy_q.get_reply_message()
        query = lmgtfy_q.text
        if query[5:]:
            query = str(query[5:])
        elif textx:
            query = textx
            query = query.message
        query_encoded = query.replace(" ", "+")
        lfy_url = f"http://lmgtfy.com/?s=g&iie=1&q={query_encoded}"
        payload = {'format': 'json', 'url': lfy_url}
        r = requests.get('http://is.gd/create.php', params=payload)
        await lmgtfy_q.edit(f"[{query}]({r.json()['shorturl']})")
        if BOTLOG:
            await bot.send_message(
                BOTLOG_CHATID,
                "LMGTFY query `" + query + "` was executed successfully",
            )
			  
@borg.on(admin_cmd(pattern="type (.*)"))
async def typewriter(typew):
        textx = await typew.get_reply_message()
        message = typew.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await typew.edit("`Give a text to type!`")
            return
        sleep_time = 0.03
        typing_symbol = "|"
        old_text = ''
        await typew.edit(typing_symbol)
        await asyncio.sleep(sleep_time)
        for character in message:
            old_text = old_text + "" + character
            typing_text = old_text + "" + typing_symbol
            await typew.edit(typing_text)
            await asyncio.sleep(sleep_time)
            await typew.edit(old_text)
            await asyncio.sleep(sleep_time)
			  

CMD_HELP.update({
    "memes": ".cowsay\
\nUsage: cow which says things.\
\n\n.milksay\
\nUsage: Weird Milk that can speak\
\n\n:/\
\nUsage: Check yourself ;)\
\n\n-_-\
\nUsage: Ok...\
\n\n;_;\
\nUsage: Like `-_-` but crying.\
\n\n.10iq\
\nUsage: You retard !!\
\n\n.oof\
\nUsage: Ooooof\
\n\n.moon\
\nUsage: kensar moon animation.\
\n\n.clock\
\nUsage: kensar clock animation.\
\n\n.earth\
\nUsage: kensar earth animation.\
\n\n.hey\
\nUsage: Greet everyone!\
\n\n.coinflip <heads/tails>\
\nUsage: Flip a coin !!\
\n\n.owo\
\nUsage: UwU\
\n\n.react\
\nUsage: Make your userbot react to everything.\
\n\n.cry\
\nUsage: y u du dis, i cri.\
\n\n.shg\
\nUsage: Shrug at it !!\
\n\n.runs\
\nUsage: Run, run, RUNNN! [`.disable runs`: disable | `.enable runs`: enable]\
\n\n.metoo\
\nUsage: Haha yes\
\n\n.clap\
\nUsage: Praise people!\
\n\n.smk <text/reply>\
\nUsage: A shit module for ツ , who cares.\
\n\n.type\
\nUsage: Just a small command to make your keyboard become a typewriter!\
\n\n.lfy <query>\
\nUsage: Let me Google that for you real quick !!\
\n\n.decide\
\nUsage: Make a quick decision.\
\n\n.abusehard\
\nUsage: You already got that! Ain't?.\
\n\n.chu\
\nUsage: Incase, the person infront of you is....\
\n\n.fuk\
\nUsage: The onlu word that can be used fucking everywhere.\
\n\n.thanos\
\nUsage: Try and then Snap.\
\n\n.noob\
\nUsage: Whadya want to know? Are you a NOOB?\
\n\n.pro\
\nUsage: If you think you're pro, try this.\
\n\n.abuse\
\nUsage: Protects you from unwanted peeps.\
\n\n.gey\
\nUsage: if you are gey.\
\n\n.bt\
\nUsage: Believe me, you will find this useful.\
"
})
