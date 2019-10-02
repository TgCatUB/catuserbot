from telethon import events
import random, re
from uniborg.util import admin_cmd

METOOSTR = [
    "`Me too thanks`",
    "`Haha yes, me too`",
    "`Same lol`",
    "`Haha yash`",
    "`Same pinch bsdk`",
    "`Bhai Bhai`",
    "`Bhai BSDK :)`",
    "`Dil Vit it`",
    "`Ja dekh jake Recaard me, Insaan hu ya Bhagwaan!`",
    "`Bawaal cheez hai be, Saara system hiladia`",
    "`Helpme, Bhai BSDK`",
]
RUNSREACTS = [
    "`Runs to Thanos`",
    "`Runs far, far away from earth`",
    "`Running faster than usian bolt coz I'mma Bot`",
    "`Runs to Marie`",
    "`This Group is too cancerous to deal with.`",
    "`Cya bois`",
    "`I am a mad person. Plox Ban me.`",
    "`I go away`",
    "`I am just walking off, coz me is too fat.`",
    "`I Fugged off!`",
]
RAPE_STRINGS = [
     "`Rape Done Drink The Cum`",
     "`The user has been successfully raped`",
     "`Dekho Bhaiyya esa hai! Izzat bachailo apni warna Gaand maar lenge tumhari`",
     "`Relax your Rear, ders nothing to fear,The Rape train is finally here`",
     "`Rape coming... Raped! haha 😆`",
     "`Lodu Andha hai kya Yaha tera rape ho raha hai aur tu abhi tak yahi gaand mara raha hai lulz`",
] 
GAALI_STRINGS = [
       "`Madharchod`",
	   "`Gaandu`",
	   "`Chutiya hi rah jayega`",
	   "`Ja be Gaandu`",
	   "`Ma ka Bhodsa madharchod`",
	   "`mml`",
	   "`You MotherFukcer`",
	   "`Muh Me Lega Bhosdike ?`"
	   "`Bhai BSDK`",
	   "`Madarchod Bhsodike macchar ki jhaat gandu makichut teri, tatto ke saudagar`",
	   "`Mene tere se bola madarchud?`",
]
ABUSEHARD_STRING = [
	"`Madarchod Randi ke bacche.Oye bosdike madarchod bhen ke lode tere gand me lohe ka danda garam karke dalu randwe tujhetho gali ke kutte gand pe chut rakh ke katenge me bata raha hu tere lode pe madhu makkhi Katelode ke ando pe Road roller chale tu kab bathroom me muthne Jaye tho Tera loda ghir Jaye fir tere ando me se lizard ke bacche nikle teko kidnap Kare aur childporn banaye maa ke chuttad ke lode tere saat Johnny sins rape Kare aur jab wo teko anal de tab loda andar fas Jaye bkl tere jhaat pe waxing karunga me dhek lio fir jab tu chillayega na tab tere muh me Mai gai ka gobar dalunga sale tere gand ke balo pe tel laga ke jala du me teko Anaconda leke gand me dalu tho muh se nikle maa ke lode hamesha chutiyo jaisa bartav kartha he tu maa ke Dai chawal drugs tere gand Me dalunga thi tatti nahi nikle maa darchod kabhi teko Marne ka mouka mil gaya na tho bas I'll do my best to get that tatti outof you aur tere jaise chutio ko is duniya me jagaha bhi nahi maa ke lode bandarchod tere gand me chitiya Kate wo bhi bullet ants maadarchod samj nahi aaraha tere baap NE teko kya khake paida kiya Tha kesa chutiya he tu rand ke bacche teko shadi me khana khane na mile teko gand pe 4 thappad mare sab log aur blade se likhe I want anal madarchod bosdike maccharki tatte ke baal chutiye maa ke chut pe ghode ka Lund tere gand me jaltha hu koila Dale bhen ke lode MAA KI CHUT MAI TALWAR DUNGA BC CHUT FAT JAEGI AUR USME SE ITNA KHOON NIKLEGA MZA AJAEGA DEKHNE KA SALE MAA KE BHOSDE SE BAHR AJA FIR BAAP SE ZUBAN DA TERI MAA KI CHUT CHOD CHOD KE BHOSDABNADU MADARCHOD AUR USKE UPAR CENENT LAGADU KI TERE JESA GANDU INSAAN KABHI BAHR NA A SKE ESI GANDI CHUT MAI SE LODA LASUN MADRCHOD TERI MAA KI CHUT GASTI AMA KA CHUTIA BACHA TERI MAA KO CHOD CHOD K PAGAL KAR DUNGA MAA K LODY KISI SASTIII RANDII K BACHY TERI MAA KI CHOOT MAIN TEER MAARUN GANDU HARAMI TERI COLLEGE JATI BAJI KA ROAD PEY RAPE KARONGANDU KI OLAAD HARAM KI NASAL PAPA HUN TERA BHEN PESH KAR AB PAPA KO TERI MAA KKALE KUSS MAIN KIS`",
	"`Main roz teri behno ki banjar chut me apna lawda daalke andar haryali lata tha magar aaj unke ke baare me sunke mujhe bhut afsos huwa..ki unko ab bada loudha chahye..ab mera balatkaaari lawda lagataar 4 ghante tk apne muh me kon rakhega..vo teri behne hi thi jo apni kaali magar rasilli chut mere saamne khol deti aur zameen pe naagin ki tarah rengne lgti thi jaise ki kisine unki chut pe naariyal tod diya ho vo b bada wala mumbai ka naariyal..apni chennal maa ko b nhi bhej rahe mere paas to main kaixe tum logo se vaada karu ki main teri maa chodd dungaw..ab agar tun sach me chahta hai ki main tum dono k mc ki chut me dhammal karu to mera lawda apne muh me rakho aur kaho Sameer hamare sage papa hain... Aur agar tb b the apni maa ki kaali chut mere saamne nahi rakhi to tumhare ghar me ghuske tumhari maa ka balatkaar kar dungaw jaixe delhi me huwa tha...ab teri chudi hui kuttiyo ki tarah apni gaand hilaate hue mere aage kalapna mt ni to tumhari fatti bhoxdi me 100 ched karunga`",
]
GEY_STRINGS = [
     "`you gey bsdk`",
     "`you gey`",
     "`you gey in the house`",
     "`you chakka`",
     "`you gey gey gey gey gey gey gey gey`",
     "`you gey go away`",
     "`Bhago BC, chakka aya`",
]
PRO_STRINGS = [
     "`This gey is pro as phack.`",
     "`Pros Is Here, Don't Leave`",
	"`What are you bsdk?Human or Gawd` (+_+)",
     "`Aye pedo gey, send moni pls`",
     "`U iz pru & I iz nub`",
     "`PROness Level : 696969`",
]
INSULT_STRINGS = [ 
    "`Owww ... Such a stupid idiot.`",
    "`Don't drink and type.`",
    "`Command not found. Just like your brain.`",
    "`Bot rule 544 section 9 prevents me from replying to stupid humans like you.`",
    "`Sorry, we do not sell brains.`",
    "`Believe me you are not normal.`",
    "`I bet your brain feels as good as new, seeing that you never use it.`",
    "`If I wanted to kill myself I'd climb your ego and jump to your IQ.`",
    "`You didn't evolve from apes, they evolved from you.`",
    "`What language are you speaking? Cause it sounds like bullshit.`",
    "`You are proof that evolution CAN go in reverse.`",
    "`As an outsider, what do you think of the human race?`",
    "`Ordinarily people live and learn. You just live.`",
    "`Keep talking, someday you'll say something intelligent!.......(I doubt it though)`",
    "`Everyone has the right to be stupid but you are abusing the privilege.`",
    "`I'm sorry I hurt your feelings when I called you stupid. I thought you already knew that.`",
    "`You should try tasting cyanide.`",
    "`You should try sleeping forever.`",
    "`Pick up a gun and shoot yourself.`",
    "`Try bathing with Hydrochloric Acid instead of water.`",
    "`Go Green! Stop inhaling Oxygen.`",
    "`God was searching for you. You should leave to meet him.`",
    "`You should Volunteer for target in an firing range.`",
    "`Try playing catch and throw with RDX its fun.`",
    "`People like you are the reason we have middle fingers.`",
    "`You’re so ugly that when you cry, the tears roll down the back of your head…just to avoid your face.`",
    "`If you’re talking behind my back then you’re in a perfect position to kiss my a**!.`",
    "`Taare hain aasmaan me very very bright jhaant na jala bsdk dekh le apni height.`",
    "`Yaar ajab tere nkhare,gazab tera style hain, gand dhone ki tameez nahi, haath main mobile hai`",
    "`Saawan ka mahina pawan kare shor jake gand mara bskd kahi aur.`", 
    "`Dil ke armaa ansuon me beh jaye tum bskd ke chutiye hi reh gye.`",
]
# ===========================================
                          

@borg.on(admin_cmd("runs ?(.*)"))
async def _(event):
    if event.fwd_from:
         return
    bro = random.randint(0, len(RUNSREACTS) - 1)    
    input_str = event.pattern_match.group(1)
    reply_text = RUNSREACTS[bro]
    await event.edit(reply_text)


@borg.on(admin_cmd("metoo ?(.*)"))
async def _(event):
    if event.fwd_from:
         return
    bro = random.randint(0, len(METOOSTR) - 1)    
    input_str = event.pattern_match.group(1)
    reply_text = METOOSTR[bro]
    await event.edit(reply_text)


@borg.on(admin_cmd("rape ?(.*)"))
async def _(event):
    if event.fwd_from:
         return
    bro = random.randint(0, len(RAPE_STRINGS) - 1)    
    input_str = event.pattern_match.group(1)
    reply_text = RAPE_STRINGS[bro]
    await event.edit(reply_text)
			  
                          
@borg.on(admin_cmd("insult ?(.*)"))
async def _(event):
    if event.fwd_from:
         return
    bro = random.randint(0, len(INSULT_STRINGS) - 1)    
    input_str = event.pattern_match.group(1)
    reply_text = INSULT_STRINGS[bro]
    await event.edit(reply_text)
			  
			  
@borg.on(admin_cmd("pro ?(.*)"))
async def _(event):
    if event.fwd_from:
         return
    bro = random.randint(0, len(PRO_STRINGS) - 1)    
    input_str = event.pattern_match.group(1)
    reply_text = PRO_STRINGS[bro]
    await event.edit(reply_text)
			  
			  
@borg.on(admin_cmd("gaali ?(.*)"))
async def _(event):
    if event.fwd_from:
         return
    bro = random.randint(0, len(GAALI_STRINGS) - 1)    
    input_str = event.pattern_match.group(1)
    reply_text = GAALI_STRINGS[bro]
    await event.edit(reply_text)
			  
@borg.on(admin_cmd("abusehard ?(.*)"))
async def _(event):
    if event.fwd_from:
         return
    bro = random.randint(0, len(ABUSEHARD_STRING) - 1)    
    input_str = event.pattern_match.group(1)
    reply_text = ABUSEHARD_STRING[bro]
    await event.edit(reply_text)
	
	
@borg.on(admin_cmd("gey ?(.*)"))
async def _(event):
    if event.fwd_from:
         return
    bro = random.randint(0, len(GEY_STRINGS) - 1)    
    input_str = event.pattern_match.group(1)
    reply_text = GEY_STRINGS[bro]
    await event.edit(reply_text)                    
