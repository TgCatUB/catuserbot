# ------ Plugin by @Lal_Bakthan-----------#

import asyncio
import random
from difflib import get_close_matches

from . import catub, edit_or_reply

plugin_category = "fun"

collection = [
    ["Saadhanam Kaiyyil undo?", "Akkare Akkare Akkare"],
    ["Kochi pazhaya kochiyellennariyam… pakshe Bilal pazhaya Bilal thanneya", "Big B"],
    [
        "…namukku chodichu chodichu pokaam. Namukku chodichu chodichu chodichu pokam.",
        "Ayal Kadha Ezhuthukayanu",
    ],
    ["Case Kodukkanam Pillecha!", "Meesha Madhavan"],
    [
        "Ninney thookkaan ividathe niyamathinu bhayam aayirunnu… marikkaan ninakkum. Pakshe ithinu randinum Mannadiyarku bhayamilla.",
        "Dhruvam",
    ],
    ["Kaanaan oru look illanney ullu… bhayankara budhiya.", "Meesha Madhavan"],
    ["Namukku gramangalil chennu raapaarkaam…", "Namukku Parkkan Munthirithoppukal"],
    [
        "Njan ee polytechnic’il onnum poyittillallo. Athukondee yanthrathinte pravarthanonnum enikku nishchayilla. Angana sambhavichatha.",
        "Thalayana Manthram",
    ],
    ["Sagar… alias… Jacky", "Irupatham Noottandu"],
    ["Ithalla ithinapparam chaadi kadannavananee K.K. Joseph!", "Vietnam Colony"],
    ["My phone number is double-two double-five", "Rajavinte Makan"],
    ["Kaakka thoori…", "In Harihar Nagar"],
    ["Varrierey… Enthado njan inganey aayi poyathu?", "Devasuram"],
    ["… naaley kaaviley paattumalsarathinu kaanaam!", "Yodha"],
    [
        "Njan oru thevidisshy ayathintey mahathwam ippozhaanenikku manasilayathu!",
        "Avalude Ravukal",
    ],
    ["Adichu mole!", "Kilukkam"],
    [
        "Orikkalum oru SSLC’karan oru Degree’karaney vedhanippikkarauthu.",
        "Nadodikkattu",
    ],
    ["Ormayundo ee mugham?", "Commissioner"],
    ["Kittiya Ootty, allenkil chatti!", "Kilukkam"],
    [
        "Pempillerey roattikoodey nadakkaan nee sammathikkilla, alley?... Da, neeyaanee alavaladi Shaji alley?",
        "Lisa",
    ],
    [
        "Athu enne uddheshichanu… enne thanney uddheshichanu… enne maatram uddheshichanu!",
        "C.I.D. Moosa",
    ],
    [
        "Varkkicha… yevan puliyanu ketta. Puliyennu paranja verum puli alla… oru simham!",
        "Rajamanikyam",
    ],
    [
        "Raju mon orikkal ennodu chodichu, uncle’intey father aaraannu.",
        "Rajavinte Makan",
    ],
    ["Kochu kuttikal kuttam cheithaal kolu mittai dai dai!", "Thoovalsparsham"],
    ["Njanalla… Ente garbham ingana alla!", "Meleparambil Aanveedu"],
    ["I am the answer! Kilometers and kilometers…", "Mazha Peyyunnu Maddalam Kottunnu"],
    ["Ramji Rao speaking.", "Ramji Rao Speaking"],
    ["Thali aaney panineeru!", "Godfather"],
    ["Mudhu-gavu!", "Thenmavin Kombath"],
    ["Polandiney patti nee oraksharam mindaruthu! Enikkathu ishtalla.", "Sandesham"],
    ["… sense undavenam! Sensibility undavenam! Sensitivity undavenam!", "The King"],
    ["Purushu enne anugrahikkanam!", "Meesha Madhavan"],
    ["Thomassootty vittoda!", "In Harihar Nagar"],
    ["Vattanalley?", "Kilukkam"],
    ["Velakkaari aayirunthaalum neeyenn mohavalli.", "Meleparambil Aanveedu"],
    ["Karuthammaa… Ennodishtamano?", "Chemmeen"],
    ["Sangeetham… ariyum thorum akalam koodunna mahaasaagaram.", "Aaraam Thampuran"],
    ["Gafoor ka Dost!", "Nadodikattu"],
    [
        "Marakkano? Pazhayathokke njan marakkano? Enthokkeyado njan marakendathu?",
        "Godfather",
    ],
    ["I’m Bharathchandran! Just remember that!", "Commissioner"],
    ["Beedi undo saghave, oru theepetti edukkan?", "Lal Salam"],
    ["Poyi Taaski viliyeda!", "Thenmavin Kombath"],
    ["Ayyo! Acha povalley!", "Shyamala"],
    ["Ippo sheriyakithara… ippo sheriyakithara…", "Vellanakalude Naadu"],
    ["Enne kollathirikkan pattuo? Illa alley?", "Chithram"],
    ["Maybe we are poor, coolies, trolley-pullers… But we are not beggars!", "Angaadi"],
    [
        "Chanduviney tholpikkaan ningalkavilla. Jeevitathil Chanduviney tholpichittundu… palarum… palavattom…",
        "Oru Vadakkan Veeragatha",
    ],
    ["Kathi thazhe idada! Nintachanaada parayunney, kathi thazhe idada!", "Kireedam"],
    ["Angana Pavanai shavamai!", "Nadodikkattu"],
    ["Vida-matte?", "Manichitrathazhu"],
    ["Police’ukaarkentha ee veetti kaaryam?", "Azhakiya Ravanan"],
    [
        "Alla... ithaara? Varyampalliley Meenakshi alleyo? Entha moley scooter'lu!",
        "Manichitrathazhu",
    ],
    [
        "Ente bheeshaneennu paranjaal, kanda oochali raashtriyakkare koottu sthalam maatti kalayoonnonnum aavilla… konnu kalayum njan!",
        "Devasuram",
    ],
    ["Njan Thiruvanathapurathekku onnu vilikkam.", "Meesha Madhavan"],
    ["Kolothey thambrattiyado… mashe!", "Aaraam Thampuran"],
    [
        "Oru manoroga chikilsakanum sancharichittillatha vazhikaliloodey okke njan sanjarichennirikkum… Oru bhrathaney pole.",
        "Manichitrathazhu",
    ],
    ["Ente maranam… oru nimishathekkenkilum ningal ellarum aagrahichilley?", "Hitler"],
    ["Thaan oru budhi-rakshasan thanney!", "His Highness Abdullah"],
    [
        "Theerumbo theerumbo pani tharaan njan entha kuppeennu vanna bhootha?",
        "Punjabi House",
    ],
    ["Sarale… Sarale… Vaathil thurakku…", "Kankettu"],
    ["Athaanu Urumees!", "Aadyathe Kanmani"],
    [
        "Ente thala, ente full-figure… Ente thala, ente full-figure… Angane… Angane… Angane…",
        "Udayananu Tharam",
    ],
    ["Kaashokke paalisayirikya Lorenz’ey.", "Chanthupottu"],
    ["Ambada kema… Sunny kutta!", "Manichitrathazhu"],
    ["Nadeshaa… kollanda!", "Ravanaprabhu"],
    ["Maanda!", "His Highness Abdullah"],
    ["Arinjilla… Ithu njan arinjilla.", "Sargam"],
    ["Annie mone snehikkunna poley, Maggie’kku enne snehikkamo?", "Dasharatham"],
    ["Aarada Naaree Nee?", "Kouthuka Varthakal"],
    ["Errr… Munpu kandittilley?", "Aaraam Thampuran"],
    ["Oh my god! CID! Escape!", "Nadodikattu"],
    ["I am the sorry, aliya… I am the sorry…", "Thilakkam"],
    ["Kalangiyilla…", "Yodha"],
    [
        "Nee ithrem bhayanakaranaya kaaryam njaan arinjilla!",
        "Sanmanassullavarkku Samadhanam",
    ],
    ["Thoma chettayalla.", "Spadikam"],
    ["Neraa Thirumeni… Eapachan pallikudathee poyittilla…", "Lelam"],
    ["Njan pinney OK’nnu paranju.", "Kilukkam"],
    [
        "Krishnavilasom Bageerathan Pilla… valiya vedi naalu… cheriya vedi naalu…",
        "Meesha Madhavan",
    ],
    ["Overact cheitu chalavaakkalleda pulley!", "In Harihar Nagar"],
    ["Govindankutty… aa kutti mindunnilla!", "Aaraam Thampuran"],
    ["Shesham bhaagam screen’il.", "Nadodikkattu"],
    [
        "Bhoogolathintey oro spandanavum kanakkilaanu. Without mathematics, bhoomi oru vatta-poojyava!",
        "Spadikam",
    ],
    [
        "Bhavani onnu manassu vechaal… ee kalavara namukkoru maniyara aakkaam.",
        "Kalyanaraman",
    ],
    ["Kuttimamakku enne vishwasam illellonnorthappo njan njetti mama.", "Yodha"],
    ["Mmakkoro naranga vellam kaachiyalo?", "Thoovanathumbikal"],
    ["Prabhakaraa….!", "Pattanapravesham"],
    ["Ashokan kudikkanda… Ashokanu Ksheenamavaam.", "Yodha"],
    ["Athokkey annan'tey lucky poley irikkum.", "Boeing Boeing"],
    ["Dasaa… oronninum athintedaaya samayam undu mone.", "Nadodikkattu"],
    ["Echoos me…", "Mukha Chithram"],
    ["Vellam… Vellam… Vellam!", "Manichitrathazhu"],
    [
        "Nee adakkamulla penvargam mattarum kaanaathatu kaanum. Ningal shapichu kondu konjum, chirichu kondu karayum, mohichu kondu verukkum.",
        "Oru Vadakkan Veeragatha",
    ],
    ["Welcome to Ootty… Nice to meet you!", "Kilukkam"],
    ["Enthino vendi thilakkunna Sambar!", "Kalyanaraman"],
    ["Ente Kochumuthalalee…", "Chemmeen"],
    ["Nee po, mone Dinesha!", "Narasimham"],
    ["Eeashwara... paavathingalku ingane soundaryam tharalley!", "Mr. Brahmachari"],
    ["Njan oru vikaara jeeviyanu…", "Mooladhanam"],
    ["Thamarasherry Churam!", "Vellanakalude Naadu"],
    ["Kambili pothappu… Kambili pothappu…", "Ramji Rao Speaking"],
    [
        "Juice juice juice, kummatti ka juice. Mammoottykka’kishtapettta kummatti ka juice!",
        "Maheshinte Prathikaaram",
    ],
    ["Porathu nalla mazhayundu… Nananjalo?", "Ennu Ninte Moideen"],
    [
        "Nee Kaanan kollavunna pen-pillerudey kaamukanmaarey kandittiley? Thani Oolanmaar aayirikkum!",
        "Thattathin Maraythu",
    ],
    [
        "Enthaannariyilla, oraalku nalla kaaryam varunnoonn’aryimbol nenjinte ividey oru vingala.",
        "Rani Padmini",
    ],
    ["Kismatu’nonnundu Faizi. Ainey aarkum thadukkaan kayyoola.", "Usatad Hotel"],
    ["Dark scene aan’ta, machaaney.", "Honey Bee"],
    ["Ente manassil… Oru classic sambhavam uruthirinju varunnundu.", "Rosapoo"],
    [
        "Nee theernneda, nee theernnu! Ithrem ahankaaram padillada. Nee theernneda, nee theernnu!",
        "Left Right Left",
    ],
    ["Ivaleym kothippichu kadannu kalanjalo?", "Amar Akbar Anthony"],
    ["Aaninu ariyathathaayi onney ullu ee bhoomiyil… athu penna.", "Vettah"],
    [
        "Wow! Psychological move! Prathiyogikale maanasikamayi thalarthanulla neekam!",
        "Memories",
    ],
    ["Kouthukam lesham kooduthala… Maapakkanam.", "Godha"],
    ["Korachu kanji edukkattey, Manikya?", "Odiyan"],
    ["Ayyo cheta, njan ee hindi cinema’yonnum kaanarilla.", "1983"],
    [
        "Nee wholesale’um cheyilla, retail’um cheyilla… oru mattethum cheyilla!",
        "Angamly Diaries",
    ],
    [
        "Premathinennum pathinaaru vayassa… Valli-nikkaril ninnum otta-mundilekku kerunna prayam.",
        "Munthirivallikal Thalirkumbol",
    ],
    ["Ithrakku cheap aano Artist Baby?", "Maheshinte Prathikaaram"],
    ["Tante thantha alla ente thantha.", "Lucifer"],
    ["Apo sheri, whatsapp’i kaana.", "Sudani From Nigeria"],
    [
        "Angana njaan pani eduthittu Pakistan nannavanda… Bharat Mata Ki…Jai!",
        "Kattappanayile Rithwik Roshan",
    ],
    ["Enikku ninte pinnaala nadakkaanalla, oppam nadakkaana ishtam.", "Bangalore Days"],
    ["Ayyo… pakalu poya enikku vazhi thettum chechi.", "Charlie"],
    [
        "Chellu ikka… poyi idikku ikka. Avantey nilpu kandilley! Poyi idikkikka.",
        "Annayum Rasoolum",
    ],
    [
        "Ho! Ithineyokke kaanumbozha, veeti irikkunnenayokke eduthu kinattil idaan thonunnathu.",
        "2 Countries",
    ],
    [
        "Enikku enne poley aavanam, Govind… iniyenkilum. Ninakku venda enne poley alla, enikku venda enne poley.",
        "Uyare",
    ],
    ["Enthoru Guhaathuratham!", "Thattathin Maraythu"],
    ["Ente sundari… Ee kadalinu ninte kanneerinte uppu venda.", "Charlie"],
    ["Oru kuthi-thirippu undaakkiyappo, enthoraashwasam!", "Amen"],
    ["Ente Ponnu Baby Moley!", "Kumbalangi Nights"],
    ["Prathibhayanu! Prathibhasamaanu!", "Pranchiyettan & the Saint"],
    ["Chill Sara, chill!", "Maheshinte Prathikaaram"],
    [
        "Daivathinte maalakhamaar ennokke vilipere ullu, Sir. Vilikkunnavar aarum maalakhamaarudey veetiley avastha chodikkarilla.",
        "TakeOff",
    ],
    [
        "Maapu Jayan parayulla… keta? Azhi engi azhi, kayar engi kayar!",
        "Left Right Left",
    ],
    [
        "Ente idea aayipoyi… ninte idea aayirunnenkil, ninna njan konnene patti!",
        "Maheshinte Prathikaaram",
    ],
    ["Thaanundello… thaan oru van-dhurandhaanu!", "Kohinoor"],
    [
        "Girls’nu athyaavashyam freedom anuvadichu kodukkunna oru modern family aanu njangadey.",
        "Kumbalangi Nights",
    ],
    ["Chettanu ithine patti valya dhaarana illa alley?", "Maheshinte Prathikaaram"],
    [
        "Aarokke enthokke paranjalum… vellavum, mannum, pennum nammale nattile thanneya nallathu!",
        "Bangalore Days",
    ],
    ["Veshannu kodelu thallakku vilikkunnu!", "Trivandrum Lodge"],
    ["Itrem kaalam evidey aayirunnu?", "Indian Rupee"],
    ["O ennathina? Aa flow angu poyi.", "Vellimoonga"],
    ["Santhoshayilley?", "Diamond Necklace"],
    ["Nee Marana Mass’ada!", "Oru Vadakkan Selfie"],
    ["Thottontey vedhana thottoney ariyoo, Punyala.", "Pranchiyettan & the Saint"],
    ["Shammi hero aada hero!", "Kumbalangi Nights"],
    ["… Scene Contra!", "Premam"],
    [
        "Chin up…shoulder down… chin down… chin podik-up… eyes open… READY!",
        "Maheshinte Prathikaaram",
    ],
    ["Java valarey simple aanu… Powerful! Bhayankara powerful aanu.", "Premam"],
    ["Pakachu poyi ente baalyam!", "Premam"],
    ["Enthu prahasana Saji!", "Kumbalangi Nights"],
]


def get_all_mov():
    mov_list = []
    for item in collection:
        if item[1] not in mov_list:
            mov_list.append(item[1])
    mov_list.sort()
    return mov_list


def get_closest(movie):
    movies = get_all_mov()
    return get_close_matches(movie, movies)


def get_from_mov(movie):
    mov_list = [item[0] for item in collection if item[1] == movie]
    mov_list.sort()
    return mov_list


@catub.cat_cmd(
    pattern="dlog$",
    command=("dlog", plugin_category),
    info={
        "header": "Random Dialogue from Malayalam Movies",
        "description": "Fetch a random dialog from malayalam movie",
        "usage": "{tr}dlog",
    },
)
async def dialogue(event):
    "Random Dialogue from Malayalam Movies"
    if event.fwd_from:
        return
    newevent = await edit_or_reply(event, "Fetching...")
    await asyncio.sleep(1)
    dialogue = random.choice(collection)
    await newevent.edit(dialogue[0])


@catub.cat_cmd(
    pattern="dlogm (.*)",
    command=("dlogm", plugin_category),
    info={
        "header": "Random Dialogue from a Specific Movie",
        "description": "Fetch a random dialog from a specific movie",
        "usage": "{tr}dlogm Spadikam",
    },
)
async def dialoguemovie(event):
    "Random Dialogue from a Specific Movie"
    match = event.pattern_match.group(1)
    newevent = await edit_or_reply(event, "Fetching...")
    movie = get_closest(match)
    if not movie:
        await newevent.edit("This movie is not available to get dialogues.")
        return
    dialogues = get_from_mov(movie[0])
    dialogue = random.choice(dialogues)
    await newevent.edit(dialogue)


@catub.cat_cmd(
    pattern="getdlogm$",
    command=("getdlogm", plugin_category),
    info={
        "header": "Movies available in Dialogues plugin",
        "description": "Fetch all movies from dialogues plugin",
        "usage": "{tr}getdlogm",
    },
)
async def getdialoguemovie(event):
    "Movies available in Dialogues plugin"
    result = "**Available Movies in Dialoges Plugin**\n\n"
    newevent = await edit_or_reply(event, "Fetching all Movies.....")
    await asyncio.sleep(1)
    movies = get_all_mov()
    for movie in movies:
        result += f"`{movie}`\n"
    await newevent.edit(result)
