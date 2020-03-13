"""
Random Anime Chooser Plugin for Userbot
usage = .{anime_genre} number of times(integer) 
By : - @Zero_cool7870

"""
from telethon import events
import asyncio
import os
import sys
import random
from userbot.utils import admin_cmd


action_list = ['6 Angels ', '12 Beast ', 'Accel World ', 'Accel World: Infinite Burst ', 'Adventures of Kotetsu ', 'Afro Samurai ', 'Agent Aika ', 'Aika R-16: Virgin Mission ', 'Air Gear ', 'Air Master ', 'Akakichi no Eleven ', 'Akashic Records of Bastard Magic Instructor ', 'Akumetsu ', 'Alive: The Final Evolution ', 'All Purpose Cultural Cat-Girl Nuku Nuku DASH! ', 'Amakusa 1637 ', 'Amefurashi ', 'Angel/Dust ', 'Angel Links ', "Angel's Feather ", 'Anne Freaks ', 'Apocalypse Zero ', 'Aquarion Evol ', 'Aquarion Logos ', 'Arc the Lad ', 'Aria the Scarlet Ammo ', "Armed Girl's Machiavellism ", 'Armitage III ', 'Armored Trooper Votoms ', 'Armored Trooper Votoms: Pailsen Files ', 'Arpeggio of Blue Steel ', 'Ashizuri Suizokukan ', 'The Asterisk War ', 'Aventura (manga) ', 'B.B. (manga) ', 'Bakumatsu Gijinden Roman ', 'Bambi and Her Pink Gun ', 'Baoh ', 'Basquash! ', 'Bastard!! ', 'Bat-Manga!: The Secret History of Batman in Japan ', 'Battle Rabbits ', 'Beelzebub (manga) ', 'Ben-To ', 'Berserk (2016 TV series) ', 'Birdy the Mighty ', 'Birth (anime) ', 'Black Bullet ', 'Black God (manga) ', 'Blame! ', 'Blame! (film) ', 'Blassreiter ', 'Blood-C: The Last Dark ', 'Blood: The Last Vampire ', 'Blue Blink ', 'Blue Seed ', 'Blue Sheep Reverie ', 'Bogle (manga) ', 'Boruto: Naruto the Movie ', 'Brave 10 ', 'Broken Blade ', 'Brotherhood: Final Fantasy XV ', 'Btooom! ', 'Bubblegum Crisis ', 'Bungo Stray Dogs ', 'Burn Up! ', 'Burn-Up Excess ', 'Burn-Up Scramble ', 'Burn-Up W ', 'Butlers: Chitose Momotose Monogatari ', 'C (TV series) ', 'C3 (novel series) ', 'Campus Special Investigator Hikaruon ', 'Caravan Kidd ', 'The Castle of Cagliostro ', 'Cat Paradise ', 'A Certain Magical Index ', 'Chivalry of a Failed Knight ', 'Chōsoku Henkei Gyrozetter ', 'Chronos Ruler ', 'City Hunter ', 'Clockwork Planet ', 'Cluster Edge ', 'Comedy (2002 film) ', 'Coppelion ', 'Cowboy Bebop ', 'Cowboy Bebop: The Movie ', 'Crimson Spell ', 'Crown (manga) ', 'Crusher Joe ', 'D4 Princess ', 'The Dagger of Kamui ', 'Daigunder ', 'Dance in the Vampire Bund ', 'Daphne in the Brilliant Blue ', 'Darkside Blues ', 'Debutante Detective Corps ', 'Demon City Shinjuku ', 'Demonizer Zilch ', 'Dennō Bōkenki Webdiver ', 'Desert Punk ', 'The Devil of the Earth ', 'Devilman ', 'Dimension W ', 'DJ (2013 anime) ', 'Dog Days (Japanese TV series) ', 'Dragon Ball Z: Bardock – The Father of Goku ', 'Dragon Ball Z: The History of Trunks ', 'Dragon Crisis! ', 'Dream Eater Merry ', 'Durarara!! ', 'Dynamic Heroes ', "E's ", "Eden: It's an Endless World! ", "Eden's Bowy ", 'Ehrgeiz (TV series) ', 'Elementalors ', "The Enemy's the Pirates! ", 'Fairy Gone ', 'Final Fantasy: Unlimited ', 'Flag (TV series) ', 'FLCL ', 'Freesia (manga) ', 'Freezing (manga) ', 'Full Metal Panic! ', "Full-Blast Science Adventure – So That's How It Is ", 'Futakoi Alternative ', 'G-On Riders ', 'Ga-Rei ', 'Gaist Crusher ', 'The Galaxy Railways ', 'Gantz ', 'Gantz: O ', 'Genesis of Aquarion ', 'Ghost in the Shell: Stand Alone Complex ', 'Giant Gorg ', 'Girls und Panzer ', 'Glass Maiden ', 'Gokudo the Adventurer ', 'Grenadier (manga) ', 'Grey (manga) ', 'Gulliver Boy ', 'Gunslinger Stratos: The Animation ', 'Guyver: The Bioboosted Armor ', 'Hajime no Ippo ', 'Hanako and the Terror of Allegory ', 'Hand Shakers ', 'Happy World! ', 'Hayate × Blade ', 'Hero Heel ', 'Hero Mask ', 'Hidamari no Ki ', 'Highlander: The Search for Vengeance ', 'Holy Talker ', 'Hyakka Ryōran ', 'Immortal Grand Prix ', 'Iron Virgin Jun ', 'The Irregular at Magic High School The Movie: The Girl Who Calls the Stars ', 'The Irregular at Magic High School ', 'Sword Oratoria ', 'Isuca ', 'Izetta: The Last Witch ', 'Japan (1992 manga) ', 'Jibaku-kun ', 'Jungle Book Shōnen Mowgli ', 'Jungle King Tar-chan ', 'Junk Force (manga) ', 'Junk: Record of the Last Hero ', 'Jushin Liger (TV series) ', 'The Kabocha Wine ', 'Kacchū no Senshi Gamu ', 'Kaiji (manga) ', 'Kamikaze (manga) ', 'Kamiyadori ', 'Kämpfer ', 'Kamui (manga series) ', 'Karakuri Circus ', 'Katanagatari ', 'Kaze ga Gotoku ', 'Kaze no Stigma ', 'Kemurikusa ', 'Kengan Ashura ', 'Kenka Shōbai ', 'Kick-Heart ', 'Kill la Kill ', 'The King Kong Show ', 'The King of Braves GaoGaiGar Final ', 'Kinnikuman ', 'Kishin Corps ', 'Kite (1998 film) ', 'Kite Liberator ', 'Kiznaiver ', 'Knights of Ramune ', 'Koihime Musō ', 'Kon Kon Kokon ', 'Kongō Banchō ', 'Kōtetsu Sangokushi ', 'Kōya no Shōnen Isamu ']
adventure_list = ['3×3 Eyes ', '12 Beast ', '801 T.T.S. Airbats ', '3000 Leagues in Search of Mother ', 'Acrobunch ', 'The Adventure of Rock ', 'The Adventures of Hutch the Honeybee ', 'The Adventures of Pepero ', 'The Adventures of Peter Pan ', 'The Adventures of Lolo the Penguin ', 'Adventures of the Little Koala ', 'The Adventures of the Little Prince (TV series) ', 'Aesop World ', 'Age of Adventure ', 'Agent Aika ', 'Ai Tenchi Muyo! ', 'Aika R-16: Virgin Mission ', 'Akame ga Kill! ', 'Aladdin and the Wonderful Lamp (1982 film) ', 'Alakazam the Great ', 'Alice SOS ', 'Alive: The Final Evolution ', 'All You Need Is Kill ', 'Allison (novel series) ', 'Allison & Lillia ', 'Amon Saga ', 'Angel Links ', 'Angelic Layer ', 'Anime Ganbare Goemon ', 'Aqua Knight ', 'Arata: The Legend ', 'Arcadia of My Youth ', 'Arcadia of My Youth: Endless Orbit SSX ', 'Argento Soma ', 'Armitage III ', 'Astro Boy ', 'Attack on Titan ', 'Attack on Titan: No Regrets ', 'Aura Battler Dunbine ', "B't X ", 'Baby Birth ', 'Baccano! ', 'BakéGyamon ', 'Bakugan Battle Brawlers ', 'Barrage (manga) ', 'Basilisk (manga) ', 'Bat-Manga!: The Secret History of Batman in Japan ', 'Battle B-Daman ', 'Battle Tendency ', 'Bayonetta: Bloody Fate ', "Beast Wars II: Lio Convoy's Close Call! ", 'Beet the Vandel Buster ', 'Berserk (1997 TV series) ', 'Berserk (manga) ', 'Berserk: The Golden Age Arc ', 'The Betrayal Knows My Name ', 'Betterman (TV series) ', 'Beyond the Beyond (manga) ', 'Big Wars ', 'Birth (anime) ', 'Black Cat (manga) ', 'Black Clover ', 'Black Lagoon ', 'Blade of the Phantom Master ', 'Blank Slate (manga) ', 'Bleach (manga) ', 'Bleach (TV series) ', 'Blood Blockade Battlefront ', 'Blood Lad ', 'Blood-C ', 'Blue Dragon (TV series) ', 'Blue Exorcist ', 'Blue Inferior ', 'Blue Sonnet ', 'Bobobo-bo Bo-bobo ', 'Bomberman Jetters ', 'Boruto: Naruto Next Generations ', 'Boruto: Naruto the Movie ', 'Bosco Adventure ', 'Brave Story ', 'Bumpety Boo ', 'Burst Angel ', 'Buso Renkin ', 'Campus Special Investigator Hikaruon ', 'Capricorn (manga) ', 'Captain Harlock: Dimensional Voyage ', 'Caravan Kidd ', 'Castle in the Sky ', 'The Castle of Cagliostro ', 'The Cat Returns ', 'Cat Soup ', "Cat's Eye (manga) ", 'A Certain Scientific Railgun ', 'Chrono Crusade ', 'Cinnamoroll ', 'Classical Medley ', 'Claymore (manga) ', 'Cleopatra DC ', 'Cobra (manga) ', 'Code Geass ', 'Cosmo Warrior Zero ', 'The Cosmopolitan Prayers ', 'Cowa! ', 'Coyote Ragtime Show ', 'Crimson Spell ', 'Croket! ', 'Cross Manage ', 'Crusher Joe ', 'Cutie Honey Universe ', 'D.Gray-man ', 'The Dagger of Kamui ', 'Dai-Guard ', 'Dangaioh ', 'Dead Leaves ', 'Deadman Wonderland ', 'Dear (manga) ', 'Demon Slayer: Kimetsu no Yaiba ', 'Detonator Orgun ', 'Devil May Cry: The Animated Series ', 'The Devil of the Earth ', 'Devils and Realist ', 'Diamond Is Unbreakable ', 'Digimon Adventure ', 'Digimon Adventure 02 ', 'Digimon Adventure tri. ', 'Digimon Data Squad ', 'Digimon Frontier ', 'Digimon Fusion ', 'Digimon Tamers ', 'Dinozaurs ', 'Divergence Eve ', 'Dōbutsu no Mori (film) ', 'Dog Days (Japanese TV series) ', 'Dogs (manga) ', 'Doraemon: Nobita and the Birth of Japan 2016 ', 'Dorohedoro ', 'Double Decker! Doug & Kirill ', 'Dr. Stone ', 'Dragon Ball (manga) ', 'Dragon Ball (TV series) ', 'Dragon Ball GT ', 'Dragon Ball Super ', 'Dragon Ball Super: Broly ', 'Dragon Ball Z ', 'Dragon Drive ', 'Dragon Eye (manga) ', 'Dragon Half ', 'Dragon Knights ', 'Dragon Quest: The Adventure of Dai ', 'Drifters (manga) ', 'DT Eightron ', 'Eagle Riders ', 'Eat-Man ', "Eden's Bowy ", 'El Cazador de la Bruja ', 'ĒlDLIVE ', 'Elementalors ', 'Ellcia ', "Elmer's Adventure: My Father's Dragon ", 'Engage Planet Kiss Dum ', 'Eureka Seven ', 'Fairy Tail ', 'Famous Dog Lassie ', 'Fate/Zero ', 'Fighting Foodons ', 'Fire Force ', 'Firestorm (TV series) ', 'The First King Adventure ', 'Flame of Recca ', 'Flint the Time Detective ', 'Flower in a Storm ', 'Food Wars!: Shokugeki no Soma ', 'The Fossil Island ', "Full-Blast Science Adventure – So That's How It Is ", 'Fullmetal Alchemist ', 'Fullmetal Alchemist (TV series) ', 'Fullmetal Alchemist: Brotherhood ', 'Future Boy Conan ', 'Future War 198X ', 'Gaba Kawa ', 'Gad Guard ', 'Galactic Gale Baxingar ', 'Galactic Whirlwind Sasuraiger ', 'Galaxy Cyclone Braiger ', 'Gall Force ', 'Gamba no Bōken ', 'Gangsta (manga) ', 'Gatchaman (OVA) ', 'Gatchaman Fighter ', 'Gatchaman II ', 'Gate Keepers ', 'Generator Gawl ', 'Geneshaft ', 'Genesis Climber MOSPEADA ', 'Gestalt (manga) ', 'GetBackers ', 'Gin Tama ', 'God Mazinger ', 'Golden Kamuy ']
harem_list = ['1+2=Paradise ', 'Ah My Buddha ', 'Ai Tenchi Muyo! ', 'Ai Yori Aoshi ', 'Akashic Records of Bastard Magic Instructor ', 'Amagami ', 'The Ambition of Oda Nobuna ', 'Angel/Dust Neo ', 'Angel Tales ', "Arifureta: From Commonplace to World's Strongest ", 'The Asterisk War ', 'Behind Closed Doors (anime) ', 'Bladedance of Elementalers ', 'Brothers Conflict ', 'C3 (novel series) ', 'Campione! ', 'Cat Planet Cuties ', 'Change 123 ', 'Clear (visual novel) ', 'D-Frag! ', 'Da Capo (visual novel) ', 'Da Capo III ', 'Death March to the Parallel World Rhapsody ', 'Demon King Daimao ', 'Dog Days (Japanese TV series) ', 'Dual! Parallel Trouble Adventure ', 'Ebiten: Kōritsu Ebisugawa Kōkō Tenmonbu ', 'Elf-ban Kakyūsei ', 'FairlyLife ', 'The Familiar of Zero ', 'Fortune Arterial ', 'Futakoi ', 'G-On Riders ', 'Gift (visual novel) ', 'Girls Bravo ', 'Girls Saurus ', 'A Good Librarian Like a Good Shepherd ', 'Guardian Hearts ', 'Haganai ', 'Hakuoki ', 'Hanaukyo Maid Team ', 'Hand Maid May ', 'Happiness! (visual novel) ', 'Happy Lesson ', 'Harukoi Otome ', 'He Is My Master ', "Heaven's Lost Property ", 'Hello, Good-bye ', 'The "Hentai" Prince and the Stony Cat. ', 'High School DxD ', 'Highschool of the Dead ', 'HoneyComing ', 'Hoshiuta ', 'Hoshizora e Kakaru Hashi ', 'How Not to Summon a Demon Lord ', "I Couldn't Become a Hero, So I Reluctantly Decided to Get a Job. ", "I Don't Like You at All, Big Brother!! ", "I'm Gonna Be An Angel! ", 'If Her Flag Breaks ', 'Iketeru Futari ', 'Imouto Paradise 2 ', 'Imouto Paradise! ', 'In Another World with My Smartphone ', 'Invaders of the Rokujouma!? ', 'Iono-sama Fanatics ', 'Is This a Zombie? ', 'Kage Kara Mamoru! ', 'Kamikaze Explorer! ', 'Kämpfer ', 'Kannagi: Crazy Shrine Maidens ', 'Kanojo × Kanojo × Kanojo ', 'Kanokon ', 'Kanon (visual novel) ', 'Kenkō Zenrakei Suieibu Umishō ', 'Kimi ga Aruji de Shitsuji ga Ore de ', 'KimiKiss ', 'Koi Koi Seven ', 'Koi suru Tenshi Angelique ', 'Koihime Musō ', 'Labyrinth of Flames ', 'Ladies versus Butlers! ', 'Like Life ', 'Lime-iro Senkitan ', 'Little Busters! ', 'Lord Marksman and Vanadis ', 'Lotte no Omocha! ', 'Love Hina ', 'Love Love? ', 'Love, Election and Chocolate ', 'Lovely Idol ', 'Maburaho ', 'Maga-Tsuki ', "Magician's Academy ", 'Magikano ', 'Maji de Watashi ni Koi Shinasai! ', 'Maken-ki! ', 'Makura no Danshi ', 'Maple Colors ', 'Marriage Royale ', 'Mashiroiro Symphony ', 'The Master of Ragnarok & Blesser of Einherjar ', 'Mayo Chiki! ', 'MM! ', 'Monster Musume ', 'My Bride is a Mermaid ', 'My First Girlfriend Is a Gal ', 'Nagasarete Airantō ', 'Nakaimo – My Sister Is Among Them! ', 'Negima! Magister Negi Magi ', 'Night Shift Nurses ', 'Ninja Girls ', 'Nogizaka Haruka no Himitsu ', 'North Wind (visual novel) ', 'Nyan Koi! ', 'Ohime-sama Navigation ', 'Omamori Himari ', 'One: Kagayaku Kisetsu e ', 'OniAi ', 'Onihime VS ', 'Oreimo ', 'Oreshura ', 'Otome wa Boku ni Koishiteru ', 'Please Twins! ', 'Princess Lover! ', 'Princess Resurrection ', 'The Quintessential Quintuplets ', 'R-15 (novel series) ', 'Rizelmine ', 'Rosario + Vampire ', 'S.L.H Stray Love Hearts! ', 'Saber Marionette ', 'Sakura Wars ', 'Samurai Harem: Asu no Yoichi ', 'School Days (visual novel) ', 'See Me After Class ', 'Sekirei ', 'Sex Taxi ', 'Shomin Sample ', 'Shuffle! ', 'Shukufuku no Campanella ', 'Sister Princess ', 'Sky Wizards Academy ', 'Strawberry 100% ', 'Summer (visual novel) ', 'Suzunone Seven! ', 'Tayutama: Kiss on my Deity ', 'Tears to Tiara ', 'Tenchi Forever! The Movie ', 'Tenchi Muyo! ', 'Tenchi Muyo! GXP ', 'Tenchi Muyo! Ryo-Ohki ', 'Tenchi Muyo! War on Geminar ', 'Tenchi the Movie 2: The Daughter of Darkness ', 'Tenchi the Movie: Tenchi Muyo in Love ', 'Tenchi Universe ', 'Tenshin Ranman: Lucky or Unlucky!? ', 'To Heart ', 'To Heart 2 ', 'To Love-Ru ', 'Trinity Seven ', 'Tsugumomo ', 'Tsuki wa Higashi ni Hi wa Nishi ni ', 'Unbalance ×2 ', 'Unlimited Fafnir ', 'Utawarerumono ', 'Valkyrie Complex ', 'Vandread ', 'W Wish ', 'We Never Learn ', 'White Album (visual novel) ', 'Wind: A Breath of Heart ', 'Words Worth ', 'World Break: Aria of Curse for a Holy Swordsman ', 'Yomeiro Choice ', 'Yosuga no Sora ', 'Yumeria ', 'Yuuna and the Haunted Hot Springs ']
romance_list = ['3×3 Eyes ', 'Absolute Boyfriend ', 'Accel World ', 'After the Rain (manga) ', 'Age 12 ', 'Ai-Ren ', 'Air (2005 film) ', 'Aishite Knight ', 'Aishiteruze Baby ', 'Akatsuki-iro no Senpuku Majo ', 'Akogare ', 'Alice 19th ', 'Alice the 101st ', 'All My Darling Daughters ', 'Allison & Lillia ', 'Alpen Rose ', 'Amnesia Labyrinth ', 'Anata to Scandal ', 'Ane no Kekkon ', 'Angel Lip ', 'Angel Nest ', 'Angelique (video game series) ', 'Ani-Imo ', 'Animated Classics of Japanese Literature ', 'Ano Ko ni 1000% ', 'Anoko no Toriko ', 'Anonymous Noise ', 'Aokana: Four Rhythm Across the Blue ', 'Aozora Yell ', 'Aquarion Evol ', 'Armitage III ', 'Ashita no Nadja ', 'Ask Dr. Rin! ', 'Attack No. 1 ', 'Attack on Tomorrow ', 'Attacker You! ', 'Azuki-chan ', 'B.O.D.Y. (manga) ', 'Baby Love (manga) ', 'Backstage Prince ', 'Banner of the Stars ', 'Bara no Tame ni ', 'Barairo no Ashita ', 'Barefoot Waltz ', 'Beast Master (manga) ', 'Beauty is the Beast ', 'Beauty Pop ', 'Beck (manga) ', 'Believers (manga) ', 'Beyond the Boundary ', 'Binetsu Shōjo ', 'Bitter Virgin ', 'Black Bird (manga) ', 'Black Rose Alice ', 'Blood Alone ', 'Blood Hound (manga) ', 'Bloom Into You ', 'Blue Friend (manga) ', 'Blue Gender ', 'Blue Spring Ride ', 'Bonjour Sweet Love Patisserie ', 'Book Girl (film) ', "Boy's Next Door ", 'Boyfriend (manga) ', 'Boys Be... ', "A Bride's Story ", 'Broken Angels (manga) ', "Cactus's Secret ", 'Call Me Princess ', 'Candy Candy ', 'Canon (manga) ', 'Canvas 2: Akane-iro no Palette ', 'Captive Hearts (manga) ', 'Castle in the Sky ', 'Cat Street (manga) ', 'Cause of My Teacher ', 'Challengers (manga) ', 'Chance Pop Session ', 'Cherry Juice ', 'Chihayafuru ', 'Children Who Chase Lost Voices ', 'Chirality (manga) ', 'ChocoTan! ', 'Chōyaku Hyakunin isshu: Uta Koi ', 'Clannad (film) ', 'Clannad (visual novel) ', 'Clear (visual novel) ', 'Clover (Toriko Chiya manga) ', 'Codename: Sailor V ', 'Coicent ', 'The Cosmopolitan Prayers ', 'Crimson Spell ', 'Crown (manga) ', 'Crown of Love (manga) ', 'D.N.Angel ', 'Da Capo III ', 'Dance in the Vampire Bund ', 'Dance with Devils ', 'A Dark Rabbit Has Seven Lives ', 'Darling in the Franxx ', 'Dawn of the Arcana ', 'Dear (manga) ', 'The Demon Ororon ', 'The Demon Prince of Momochi House ', 'Demonizer Zilch ', 'Dengeki Daisy ', 'A Devil and Her Love Song ', 'The Devil Does Exist ', 'Dolis ', 'Domestic Girlfriend ', "Don't Say Anymore, Darling ", 'Dōse Mō Nigerarenai ', 'Dragon Eye (manga) ', 'Dream Saga ', "Dreamin' Sun ", 'A Drifting Life ', 'Drifting Net Cafe ', 'Drowning Love ', 'Dusk Maiden of Amnesia ', 'The Earl and the Fairy ', 'Eden* ', "Eden's Bowy ", 'Eerie Queerie! ', 'El-Hazard ', 'Embracing Love ', 'Emma (manga) ', 'Eureka Seven ', 'FairlyLife ', 'Final Approach (visual novel) ', 'Fire Tripper ', 'First Love Sisters ', 'Fish in the Trap ', 'Flower in a Storm ', 'Fortune Arterial ', 'Four Shōjo Stories ', 'Four-Eyed Prince ', 'Foxy Lady (manga) ', 'From Far Away ', 'Fruits Basket ', 'Full Metal Panic? Fumoffu ', 'Full Moon o Sagashite ', 'Fushigi Yûgi ', 'Future Diary ', 'Gaba Kawa ', 'Gakuen Polizi ', 'Garden Dreams ', 'Gatcha Gacha ', 'Genesis of Aquarion ', 'Genji Monogatari Sennenki ', 'A Gentle Breeze in the Village ', 'Georgie! ', 'Gerard & Jacques ', 'Gift (visual novel) ', 'Girl Friend (manga) ', 'Girl Friend Beta ', 'Girl Friends (manga) ', 'Girl Got Game ', 'The Girl Who Leapt Through Time (2006 film) ', 'Girls Beyond the Wasteland ', 'Glass Wings ', 'Glasslip ', 'A Good Librarian Like a Good Shepherd ', 'Good Morning Call ', 'Gosick ', 'Gou-dere Sora Nagihara ', 'Gravitation (manga) ', 'Green Green (TV series) ', 'Gunparade March ', 'Hachimitsu ni Hatsukoi ', 'Haikara-San: Here Comes Miss Modern ', 'Hakuba no Ōji-sama ', 'Hal (2013 film) ', 'Hana & Hina After School ', 'Hana to Akuma ', 'Hana-Kimi ', 'Hana-kun to Koisuru Watashi ', 'Hanasakeru Seishōnen ', 'Hanbun no Tsuki ga Noboru Sora ', 'Handsome na Kanojo ', 'Hanjuku-Joshi ', 'Haou Airen ', 'Happy Hustle High ', 'Happy Marriage!? ', 'Haru Natsu Aki Fuyu ', 'Haruka: Beyond the Stream of Time (manga) ', 'Harukoi Otome ', "He's My Only Vampire ", 'The Heart of Thomas ', 'Hello! Lady Lynn ', "Her Majesty's Dog ", 'Here Is Greenwood ', 'Heroine Shikkaku ', 'Hiatari Ryōkō! ', 'Hibi Chōchō ', 'High School Debut ', 'Hikari no Densetsu ', 'Himitsu no Akko-chan ', 'Himitsu no Recipe ', 'Hirunaka no Ryuusei ']
mecha_list = ['Ai City ', 'Akane Maniax ', 'Aldnoah.Zero ', 'All Purpose Cultural Cat-Girl Nuku Nuku DASH! ', 'AM Driver ', 'Ambassador Magma ', 'Aquarion Logos ', 'Argento Soma ', 'Argevollen ', 'Ariel (anime) ', 'Ark (2005 film) ', 'Armitage III ', 'Armored Trooper Votoms: Pailsen Files ', 'Assemble Insert ', 'Aura Battler Dunbine ', 'Baldr Force ', 'Basquash! ', 'Battle Skipper ', "Beast Wars II: Lio Convoy's Close Call! ", 'Betterman (TV series) ', 'Blue Comet SPT Layzner ', 'Blue Gender ', 'Brain Powerd ', 'Broken Blade ', 'Bubblegum Crisis ', 'Bubblegum Crisis Tokyo 2040 ', 'Buddy Complex ', 'Burn-Up W ', 'Busou Shinki ', 'The Candidate for Goddess ', 'Cannon God Exaxxion ', 'Castle in the Sky ', 'Cat City ', 'Chō Jikū Robo Meguru ', 'Chō Kōsoku Galvion ', 'Chōsoku Henkei Gyrozetter ', 'Chōgattai Majutsu Robo Ginguiser ', 'Choriki Robo Galatt ', 'Code Geass ', 'Combat Mecha Xabungle ', 'Comet Lucifer ', 'The Cosmopolitan Prayers ', 'Cross Ange ', 'Cybuster ', 'D.I.C.E. ', 'Dai-Shogun – Great Revolution ', 'Daigunder ', 'Daimajū Gekitō: Hagane no Oni ', 'Daimidaler: Prince vs Penguin Empire ', 'Darling in the Franxx ', 'Dennō Bōkenki Webdiver ', 'Detonator Orgun ', 'Devadasy ', 'Dinosaur War Izenborg ', 'Dinozaurs ', 'Dual! Parallel Trouble Adventure ', 'Dynamic Heroes ', 'Ehrgeiz (TV series) ', 'The End of Evangelion ', 'Engage Planet Kiss Dum ', 'Escaflowne (film) ', 'Eureka Seven ', 'Evangelion: 1.0 You Are (Not) Alone ', 'Evangelion: 2.0 You Can (Not) Advance ', 'Evangelion: 3.0 You Can (Not) Redo ', 'Evangelion: 3.0+1.0 ', 'Expelled from Paradise ', 'Fafner in the Azure ', 'Fang of the Sun Dougram ', 'Fight! Iczer One ', 'Firestorm (TV series) ', 'First Squad ', 'Flag (TV series) ', 'Force Five ', 'Frame Arms Girl ', 'Gad Guard ', 'Galaxy Fräulein Yuna ', 'Gargantia on the Verdurous Planet ', 'Geneshaft ', 'Genesis Survivor Gaiarth ', 'Giant Gorg ', "Gin'iro no Olynssis ", 'Ginga Hyōryū Vifam ', 'The Girl Who Leapt Through Space ', 'God Mazinger ', 'Godzilla: City on the Edge of Battle ', 'Godzilla: Planet of the Monsters ', 'Good Morning Althea ', 'Grey (manga) ', 'Guilty Crown ', 'Gunbuster ', 'Gunparade March ', 'Gurren Lagann ', 'Heavy Metal L-Gaim ', 'Heroic Age (TV series) ', 'Hikarian ', 'Ichigeki Sacchu!! HoiHoi-san ', 'Idolmaster: Xenoglossia ', 'Immortal Grand Prix ', 'Infinite Ryvius ', 'Infinite Stratos ', 'Innocent Venus ', 'Invincible King Tri-Zenon ', 'Jinki: Extend ', 'Jushin Liger (TV series) ', 'K.O. Beast ', 'Kannazuki no Miko ', 'Key the Metal Idol ', 'Kikaider ', 'Kirameki Project ', 'Kishin Corps ', 'Kishin Taisen Gigantic Formula ', "Knight's & Magic ", 'Knights of Ramune ', 'Knights of Sidonia ', 'Kurogane Communication ', 'Kuromukuro ', 'Lime-iro Senkitan ', 'Linebarrels of Iron ', 'M3: The Dark Metal ', 'Machine Robo Rescue ', 'Macross ', 'Macross Delta ', 'Magic Knight Rayearth ', 'Majestic Prince (manga) ', 'Mars Daybreak ', 'Martian Successor Nadesico: The Motion Picture – Prince of Darkness ', 'Mazinger Z ', 'Mazinger Z vs. The Great General of Darkness ', 'MazinSaga ', 'MD Geist ', 'Melody of Oblivion ', 'Metal Armor Dragonar ', 'Negadon: The Monster from Mars ', 'Neo Ranga ', 'Neon Genesis Evangelion ', 'Neon Genesis Evangelion (franchise) ', 'Neon Genesis Evangelion: Death & Rebirth ', 'NG Knight Ramune & 40 ', 'Nobunaga the Fool ', 'Overman King Gainer ', 'Panzer World Galient ', 'Patlabor: The New Files ', 'Patlabor: The TV Series ', 'Planet With ', 'Planzet ', 'Plastic Little ', 'Platinumhugen Ordian ', 'Plawres Sanshiro ', 'Power Stone (TV series) ', 'Psycho Armor Govarian ', 'RahXephon ', 'Red Baron (TV series) ', 'Red Eyes ', 'Regalia: The Three Sacred Stars ', 'Rideback ', 'Robo Formers ', 'Robot Carnival ', 'Robot Girls Z ', 'Robotech ', 'Robotech II: The Sentinels ', 'Robotech: Love Live Alive ', 'Robotech: The Movie ', 'Robotics;Notes ', 'RS Project -Rebirth Storage- ', 'Sailor Victory ', 'Sakura Wars ', 'Samurai 7 ', 'School Shock ', 'Science Ninja Team Gatchaman ', 'Shattered Angels ', 'Shinkansen Henkei Robo Shinkalion ', 'Sky Girls ', 'SSSS.Gridman ', 'Star Driver ', 'Starship Troopers (OVA) ', 'Stellvia ', 'Strain: Strategic Armored Infantry ', 'Super Dimension Century Orguss ', 'The Super Dimension Fortress Macross ', 'Super Robot Wars Original Generation: Divine Wars ', 'Super Robot Wars Original Generation: The Animation ', 'Super Robot Wars Original Generation: The Inspector ', 'Techno Police 21C ', 'Tekkaman Blade ', 'Tenchi Muyo! War on Geminar ', 'Tokio Private Police ', 'Tomica Hyper Rescue Drive Head Kidō Kyūkyū Keisatsu ', 'Transformers Go! ', 'Transformers: Armada ', 'Transformers: Armada (comics) ', 'Transformers: Cybertron ', 'Transformers: Energon ', 'Transformers: Robot Masters ', 'Transformers: Super-God Masterforce ', 'Transformers: The Headmasters ', 'Transformers: Victory ', 'Transformers: Zone ']
slice_of_life_list = ['A Channel (manga) ', 'Abandon the Old in Tokyo ', 'Age 12 ', 'Aho-Girl ', 'Aiura ', 'Akiba-chan (TV series) ', 'Akogare ', 'Amanchu! ', 'Amano Megumi wa Sukidarake! ', 'And Yet the Town Moves ', 'Ane no Kekkon ', 'Anime-Gatari ', 'Asahinagu ', 'Asari-chan ', 'Ashizuri Suizokukan ', 'Azumanga Daioh ', 'Baby & Me ', 'Baby Princess ', 'Bakuman ', 'Barairo no Ashita ', 'Barakamon ', 'Best Student Council ', 'Binbō Shimai Monogatari ', 'Blend S ', "A Centaur's Life ", 'Chihayafuru ', 'Chimpui ', 'Chitose Get You!! ', 'Choir! ', 'Cinnamoroll ', 'Clannad (visual novel) ', 'The Comic Artist and His Assistants ', 'The Cosmopolitan Prayers ', 'Crayon Shin-chan ', 'Crossing Time ', 'Dagashi Kashi ', 'Daily Lives of High School Boys ', 'Dareka no Manazashi ', 'DD Fist of the North Star ', "Dead Dead Demon's Dededede Destruction ", 'Doki Doki School Hours ', "Dreamin' Sun ", 'Drowning Love ', 'Encouragement of Climb ', 'Endro! ', 'Flower of Life (manga) ', 'Flying Witch ', 'Food Wars!: Shokugeki no Soma ', 'Futagashira ', 'Futaribeya: A Room for Two ', 'GA Geijutsuka Art Design Class ', 'Ganbare!! Tabuchi-kun!! ', 'Genshiken ', 'A Gentle Breeze in the Village ', "Girls' Last Tour ", 'Glasslip ', 'Gokicha ', 'Goodnight Punpun ', 'Gourmet Girl Graffiti ', 'Green Green (TV series) ', 'Hachimitsu ni Hatsukoi ', 'Hakumei and Mikochi ', 'Hana-kun to Koisuru Watashi ', 'Hanamaru Kindergarten ', 'Hanasaku Iroha ', 'Hanayamata ', 'Happy Happy Clover ', 'Hayate the Combat Butler ', 'Hello! Lady Lynn ', 'Hello! Sandybell ', 'Heroine Shikkaku ', 'Hibi Chōchō ', 'Hibi Rock ', 'Hidamari Sketch ', 'Hitori Bocchi no Marumaru Seikatsu ', 'Hōkago Play ', 'Hori-san to Miyamura-kun ', 'House of the Sun ', 'Human Crossing ', 'Hyakko ', 'Hyouka ', "If It's for My Daughter, I'd Even Defeat a Demon Lord ", 'Is the Order a Rabbit? ', 'Jūhan Shuttai! ', 'K-On! ', 'Kamichu! ', 'Kamisama Minarai: Himitsu no Cocotama ', 'Kamurobamura-e ', 'Kanamemo ', 'Teasing Master Takagi-san ', 'Karakuri Odette ', 'Kenka Shōbai ', 'Kids on the Slope ', 'Kill Me Baby ', 'Kimi ni Todoke ', 'Kira Kira Happy Hirake! Cocotama ', 'Kokoro Button ', 'Kono Oto Tomare! Sounds of Life ', 'Konohana Kitan ', 'Koro Sensei Quest ', 'Kū Neru Futari Sumu Futari ', 'Kyō, Koi o Hajimemasu ', 'L DK ', 'Liar × Liar ', 'Little Forest ', 'Love Celeb ', 'Love Hina ', 'Love Live! ', 'Lucky Star (manga) ', 'Maestro (manga) ', 'Mai Mai Miracle ', 'Mainichi Kaasan ', 'Manga Dogs ', 'Maple Town ', 'Meganebu! ', 'Mitsuboshi Colors ', 'Mitsudomoe (manga) ', 'Morita-san wa Mukuchi ', 'Mushishi ', 'My Roommate Is a Cat ', 'Nagareboshi Lens ', 'Naisho no Tsubomi ', 'Nasu (manga) ', 'Natsuiro Kiseki ', 'Ningen Karimenchū ', "No Matter How I Look at It, It's You Guys' Fault I'm Not Popular! ", 'Non Non Biyori ', 'Nōnai Poison Berry ', 'Nono-chan ', 'Noucome ', "Nurse Hitomi's Monster Infirmary ", 'Ojamanga Yamada-kun ', 'The One I Love (manga) ', 'One Off (miniseries) ', 'Orange (manga) ', 'Otoko no Isshō ', 'Paboo & Mojies ', 'Place to Place ', 'Poyopoyo Kansatsu Nikki ', 'Princess Maison ', 'Project 575 ', 'The Push Man and Other Stories ', 'Recorder and Randsell ', 'Recovery of an MMO Junkie ', 'ReRe Hello ', 'Rin-ne ', 'Robot Girls Z ', 'S.S. Astro ', 'Sabagebu! ', 'Saint Young Men ', 'Sakura Quest ', 'Sakura Trick ', 'Sanrio Boys ', 'Sanzoku Diary ', 'Sayonara Sorcier ', 'Sayonara, Tama-chan ', 'Sazae-san ', 'School Days (visual novel) ', 'Seitokai Yakuindomo ', 'Senryu Girl ', 'Servant × Service ', 'Shitsuren Chocolatier ', 'Silver Spoon (manga) ', 'Sketchbook (manga) ', 'Slow Start (manga) ', 'Solanin ', 'Soul Eater Not! ', 'Sound of the Sky ', 'Space Brothers (manga) ', 'Star-Myu ', 'Stella Women’s Academy, High School Division Class C³ ', 'Strawberry Marshmallow ', "Student Council's Discretion ", 'Sukimasuki ', 'Sunny (manga) ', 'Super Seisyun Brothers ', 'Sweetness and Lightning ', 'Sylvanian Families (OVA series) ', 'Tamagotchi! (TV series) ', 'Tenshi Nanka Ja Nai ', 'Tesagure! Bukatsu-mono ', "Today's Menu for the Emiya Family ", 'Tokyo Alice ', 'Tonari no Kashiwagi-san ', 'Toradora! ', 'Town Doctor Jumbo!! ', 'True Love (manga) ', 'True Tears (TV series) ', 'The Tyrant Falls in Love ', 'Uchi no Sanshimai ', 'Ultimate Otaku Teacher ', 'Undercurrent (manga) ', 'Wake Up, Girls! ', 'Welcome to the N.H.K. ', 'What a Wonderful World! ', 'Working!! ', 'Yokohama Kaidashi Kikō ', 'Yotsuba&! ', 'YuruYuri ']
isekai_list = ['12 Beast ', '100 Sleeping Princes and the Kingdom of Dreams ', "Arifureta: From Commonplace to World's Strongest ", 'Ascendance of a Bookworm ', 'Aura Battler Dunbine ', 'The Brave-Tuber ', 'Captain N: The Game Master ', 'Conception (video game) ', 'Death March to the Parallel World Rhapsody ', "Didn't I Say to Make My Abilities Average in the Next Life?! ", 'Digimon Adventure ', 'Do You Love Your Mom and Her Two-Hit Multi-Target Attacks? ', 'Dog Days (Japanese TV series) ', 'Drifters (manga) ', 'El-Hazard ', 'Endride ', 'The Familiar of Zero ', 'Fushigi Yûgi ', 'Gate (novel series) ', 'Grimgar of Fantasy and Ash ', 'Hachinantte Sore wa Inai Deshō! ', 'The Hero is Overpowered but Overly Cautious ', 'High School Prodigies Have It Easy Even In Another World ', 'How a Realist Hero Rebuilt the Kingdom ', 'How Not to Summon a Demon Lord ', "I've Been Killing Slimes for 300 Years and Maxed Out My Level ", 'In Another World with My Smartphone ', 'Infinite Dendrogram ', 'Inuyasha ', 'Isekai Cheat Magician ', 'Isekai Izakaya "Nobu" ', 'Isekai Quartet ', 'Kemonomichi ', 'Kiba (TV series) ', "Knight's & Magic ", 'KonoSuba ', 'Kyo Kara Maoh! ', 'Log Horizon ', 'Magic Knight Rayearth ', 'Magical Shopping Arcade Abenobashi ', 'Maō-sama, Retry! ', 'MÄR ', 'The Master of Ragnarok & Blesser of Einherjar ', 'Mushoku Tensei ', 'My Next Life as a Villainess: All Routes Lead to Doom! ', 'New Life+: Young Again in Another World ', 'No Game No Life ', 'No Game, No Life Zero ', 'Outbreak Company ', 'Overlord (novel series) ', 'Pop in Q ', "Problem Children Are Coming from Another World, Aren't They? ", 'Re:Zero − Starting Life in Another World ', 'Reborn as a Vending Machine, I Now Wander the Dungeon ', 'Restaurant to Another World ', 'The Rising of the Shield Hero ', 'The Saga of Tanya the Evil ', "So I'm a Spider, So What? ", 'Spirited Away ', 'Sword Art Online ', 'That Time I Got Reincarnated as a Slime ', 'Tweeny Witches ', 'The Twelve Kingdoms ', "Wise Man's Grandchild "]

@borg.on(admin_cmd("anime"))
async def _(event):
    if event.fwd_from:
        return   
    number_of_times = event.text[7:]
    number_of_times = int(number_of_times)
    i = 0
    anime_list = []
    while i != number_of_times:
        anime = random.choice(action_list)
        anime_list.append(anime+"\n")
        i = i + 1
    counter = 1
    msg_str = []   
    for i in anime_list:
        msg_str.append(str(counter)+". "+i)
        counter = counter + 1
    msg_str = str(msg_str)
    msg_str = msg_str.replace("['","")
    msg_str = msg_str.replace(",","")
    msg_str = msg_str.replace("']","")
    msg_str = msg_str.replace("' '","")
    msg_str_front = "Here's Top "+str(number_of_times)+" Action Anime List For you !\n"
    msg_str = msg_str_front+ msg_str
    msg_str = msg_str.replace("\\n","\n")
    msg_str = msg_str.replace("'","")
    msg_str = msg_str.replace('"',"")
    await event.edit("**"+msg_str+"**")    
     
@borg.on(admin_cmd(pattern=r"harem"))
async def action(event):
    if event.fwd_from:
        return   
    number_of_times = event.text[7:]
    number_of_times = int(number_of_times)
    i = 0
    anime_list = []
    while i != number_of_times:
        anime = random.choice(harem_list)
        anime_list.append(anime+"\n")
        i = i + 1
    counter = 1
    msg_str = []   
    for i in anime_list:
        msg_str.append(str(counter)+". "+i)
        counter = counter + 1
    msg_str = str(msg_str)
    msg_str = msg_str.replace("['","")
    msg_str = msg_str.replace(",","")
    msg_str = msg_str.replace("']","")
    msg_str = msg_str.replace("' '","")
    msg_str_front = "Here's Top "+str(number_of_times)+" Harem Anime List For you !\n"
    msg_str = msg_str_front+ msg_str
    msg_str = msg_str.replace("\\n","\n")
    msg_str = msg_str.replace("'","")
    msg_str = msg_str.replace('"',"")
    await event.edit("**"+msg_str+"**")

@borg.on(admin_cmd(pattern=r"mecha"))
async def action(event):
    if event.fwd_from:
        return   
    number_of_times = event.text[7:]
    number_of_times = int(number_of_times)
    i = 0
    anime_list = []
    while i != number_of_times:
        anime = random.choice(mecha_list)
        anime_list.append(anime+"\n")
        i = i + 1
    counter = 1
    msg_str = []   
    for i in anime_list:
        msg_str.append(str(counter)+". "+i)
        counter = counter + 1
    msg_str = str(msg_str)
    msg_str = msg_str.replace("['","")
    msg_str = msg_str.replace(",","")
    msg_str = msg_str.replace("']","")
    msg_str = msg_str.replace("' '","")
    msg_str_front = "Here's Top "+str(number_of_times)+" Mecha Anime List For you !\n"
    msg_str = msg_str_front+ msg_str
    msg_str = msg_str.replace("\\n","\n")
    msg_str = msg_str.replace("'","")
    msg_str = msg_str.replace('"',"")
    await event.edit("**"+msg_str+"**")

@borg.on(admin_cmd(pattern=r"romance"))
async def action(event):
    if event.fwd_from:
        return   
    number_of_times = event.text[9:]
    number_of_times = int(number_of_times)
    i = 0
    anime_list = []
    while i != number_of_times:
        anime = random.choice(romance_list)
        anime_list.append(anime+"\n")
        i = i + 1
    counter = 1
    msg_str = []   
    for i in anime_list:
        msg_str.append(str(counter)+". "+i)
        counter = counter + 1
    msg_str = str(msg_str)
    msg_str = msg_str.replace("['","")
    msg_str = msg_str.replace(",","")
    msg_str = msg_str.replace("']","")
    msg_str = msg_str.replace("' '","")
    msg_str_front = "Here's Top "+str(number_of_times)+" Romance Anime List For you !\n"
    msg_str = msg_str_front+ msg_str
    msg_str = msg_str.replace("\\n","\n")
    msg_str = msg_str.replace("'","")
    msg_str = msg_str.replace('"',"")
    await event.edit("**"+msg_str+"**")

@borg.on(admin_cmd(pattern=r"isekai"))
async def action(event):
    if event.fwd_from:
        return   
    number_of_times = event.text[8:]
    number_of_times = int(number_of_times)
    i = 0
    anime_list = []
    while i != number_of_times:
        anime = random.choice(isekai_list)
        anime_list.append(anime+"\n")
        i = i + 1
    counter = 1
    msg_str = []   
    for i in anime_list:
        msg_str.append(str(counter)+". "+i)
        counter = counter + 1
    msg_str = str(msg_str)
    msg_str = msg_str.replace("['","")
    msg_str = msg_str.replace(",","")
    msg_str = msg_str.replace("']","")
    msg_str = msg_str.replace("' '","")
    msg_str_front = "Here's Top "+str(number_of_times)+" Isekai Anime List For you !\n"
    msg_str = msg_str_front+ msg_str
    msg_str = msg_str.replace("\\n","\n")
    msg_str = msg_str.replace("'","")
    msg_str = msg_str.replace('"',"")
    await event.edit("**"+msg_str+"**")

@borg.on(admin_cmd(pattern=r"adventure"))
async def action(event):
    if event.fwd_from:
        return   
    number_of_times = event.text[10:]
    number_of_times = int(number_of_times)
    i = 0
    anime_list = []
    while i != number_of_times:
        anime = random.choice(adventure_list)
        anime_list.append(anime+"\n")
        i = i + 1
    counter = 1
    msg_str = []   
    for i in anime_list:
        msg_str.append(str(counter)+". "+i)
        counter = counter + 1
    msg_str = str(msg_str)
    msg_str = msg_str.replace("['","")
    msg_str = msg_str.replace(",","")
    msg_str = msg_str.replace("']","")
    msg_str = msg_str.replace("' '","")
    msg_str_front = "Here's Top "+str(number_of_times)+" Adventure Anime List For you !\n"
    msg_str = msg_str_front+ msg_str
    msg_str = msg_str.replace("\\n","\n")
    msg_str = msg_str.replace("'","")
    msg_str = msg_str.replace('"',"")
    await event.edit("**"+msg_str+"**") 

@borg.on(admin_cmd(pattern=r"slice"))
async def action(event):
    if event.fwd_from:
        return   
    number_of_times = event.text[7:]
    number_of_times = int(number_of_times)
    i = 0
    anime_list = []
    while i != number_of_times:
        anime = random.choice(slice_of_life_list)
        anime_list.append(anime+"\n")
        i = i + 1
    counter = 1
    msg_str = []   
    for i in anime_list:
        msg_str.append(str(counter)+". "+i)
        counter = counter + 1
    msg_str = str(msg_str)
    msg_str = msg_str.replace("['","")
    msg_str = msg_str.replace(",","")
    msg_str = msg_str.replace("']","")
    msg_str = msg_str.replace("' '","")
    msg_str_front = "Here's Top "+str(number_of_times)+" Slice of life Anime List For you !\n"
    msg_str = msg_str_front+ msg_str
    msg_str = msg_str.replace("\\n","\n")
    msg_str = msg_str.replace("'","")
    msg_str = msg_str.replace('"',"")
    await event.edit("**"+msg_str+"**")                   
    
