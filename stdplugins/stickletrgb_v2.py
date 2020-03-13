# Random RGB Sticklet by @PhycoNinja13b

#Exclusive for My personal Repo
#Requirement of this plugin is very high (Kumbhkaran ki aulad) 
#Currently Loaded 74 Font Options 
#Dare To edit this part! U will be tored apart! 

import io
import textwrap
import random
from telethon import events

from PIL import Image, ImageDraw, ImageFont

from uniborg.util import admin_cmd

@borg.on(admin_cmd(pattern="plet (.*)"))
async def sticklet(event):
    
    R = random.randint(0,256)
    G = random.randint(0,256)
    B = random.randint(0,256)
    FC = random.randint(1,75)
    sticktext = event.pattern_match.group(1)

    if not sticktext:
        await event.edit("`I need text to sticklet!`")
        return

    await event.delete()

    sticktext = textwrap.wrap(sticktext, width=10)
    sticktext = '\n'.join(sticktext)

    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 230

    if FC==1:
      FONT_FILE = "Fonts/Aksana-8KnB.ttf"
    if FC==2:
      FONT_FILE = "Fonts/AlChevrolaPersonaluseonly-Ea47r.ttf"
    if FC==3:
      FONT_FILE = "Fonts/AlChevrolaPersonaluseonly-axY2a.otf"
    if FC==4:
      FONT_FILE = "Fonts/AlLeporschePersonaluseonly-Eaqln.otf"
    if FC==5:
      FONT_FILE = "Fonts/AlLeporschePersonaluseonly-OVZ24.ttf"
    if FC==6:
      FONT_FILE = "Fonts/Alberto-yx2q.ttf"
    if FC==7:
      FONT_FILE = "Fonts/AlexBrush-Regular.ttf"
    if FC==8:
      FONT_FILE = "Fonts/Alienzmonkey-ze7l.ttf"
    if FC==9:
      FONT_FILE = "Fonts/Allura-Regular.otf"
    if FC==10:
      FONT_FILE = "Fonts/ArchitectsDaughter.ttf"
    if FC==11:
      FONT_FILE = "Fonts/Arizonia-Regular.ttf"
    if FC==12:
      FONT_FILE = "Fonts/BetterCaramel-ajrK.otf"
    if FC==13:
      FONT_FILE = "Fonts/BetterCaramelSans-EjRW.otf"
    if FC==14:   
      FONT_FILE = "Fonts/BetterCaramelSansBold-Oj76.otf"
    if FC==15:
      FONT_FILE = "Fonts/BetterCaramelSansHollow-Zjl3.otf"
    if FC==16:
      FONT_FILE = "Fonts/BetterCaramelSerif-37Kp.otf"
    if FC==17:
      FONT_FILE = "Fonts/BetterCaramelSerifBold-x0Ym.otf"
    if FC==18:
      FONT_FILE = "Fonts/BetterCaramelSerifHollow-pm0d.otf"
    if FC==19:
      FONT_FILE = "Fonts/BlackthornsDemoBlack-L2GE.ttf"
    if FC==20:
      FONT_FILE = "Fonts/BlackthornsDemoRegular-X0MZ.ttf"
    if FC==21:
      FONT_FILE = "Fonts/Bulgatti-xgMV.ttf"
    if FC==22:
      FONT_FILE = "Fonts/ChampagneAndLimousines-7KRB.ttf"
    if FC==23:
      FONT_FILE = "Fonts/ChampagneAndLimousinesBold-myr2.ttf"
    if FC==24:
      FONT_FILE = "Fonts/ChampagneAndLimousinesBoldItalic-dqex.ttf"
    if FC==25:
      FONT_FILE = "Fonts/ChampagneAndLimousinesItalic-PlRZ.ttf"
    if FC==26:
      FONT_FILE = "Fonts/Entreaty-5Y7V.ttf"
    if FC==27:
      FONT_FILE = "Fonts/Fancy-GxRO.otf"
    if FC==28:
      FONT_FILE = "Fonts/Gardenparty-p0MD.ttf"
    if FC==29:
      FONT_FILE = "Fonts/GreatVibes-Regular.otf"
    if FC==30:
      FONT_FILE = "Fonts/Jolly-OOw6.ttf"
    if FC==31:
      FONT_FILE = "Fonts/JollyBold-ZGW3.ttf"
    if FC==32:
      FONT_FILE = "Fonts/JollyBoldItalic-3wmp.ttf"
    if FC==33:
      FONT_FILE = "Fonts/JollyItalic-xxjm.ttf"
    if FC==34:
      FONT_FILE = "Fonts/KaushanScript-Regular.otf"
    if FC==35:
      FONT_FILE = "Fonts/LitleSimpleSt-2lZ3.ttf"
    if FC==36:
      FONT_FILE = "Fonts/LobsterTwo-Bold.otf"
    if FC==37:
      FONT_FILE = "Fonts/LobsterTwo-BoldItalic.otf"
    if FC==38:
      FONT_FILE = "Fonts/LobsterTwo-Italic.otf"
    if FC==39:
      FONT_FILE = "Fonts/LobsterTwo-Regular.otf"
    if FC==40:
      FONT_FILE = "Fonts/LordZeddLjStudios-4YzB.ttf"
    if FC==41:
      FONT_FILE = "Fonts/LuisSmartTx-rW6y.ttf"
    if FC==42:
      FONT_FILE = "Fonts/MountainsofChristmas.ttf"
    if FC==43:
      FONT_FILE = "Fonts/NightmarePills-BV2w.ttf"
    if FC==44:
      FONT_FILE = "Fonts/Pacifico.ttf"
    if FC==45:
      FONT_FILE = "Fonts/PierceRegular-6OWY.ttf"
    if FC==46:
      FONT_FILE = "Fonts/Pierceregular-BgeV.otf"
    if FC==47:
      FONT_FILE = "Fonts/Pixeboy-z8XGD.ttf"
    if FC==48:
      FONT_FILE = "Fonts/PussyCat-Dy69.ttf"
    if FC==49:
      FONT_FILE = "Fonts/RaconteurNf-LOlE.ttf"
    if FC==50:
      FONT_FILE = "Fonts/Rolande-8Ydg.ttf"
    if FC==51:
      FONT_FILE = "Fonts/RolandeBold-YLaO.ttf"
    if FC==52:
      FONT_FILE = "Fonts/Sail-Regular.otf"
    if FC==53:
      FONT_FILE = "Fonts/Skarpalt-qx4V.ttf"
    if FC==54:
      FONT_FILE = "Fonts/Sofia-Regular.otf"
    if FC==55:
      FONT_FILE = "Fonts/Tangerine_Bold.ttf"
    if FC==56:
      FONT_FILE = "Fonts/Tangerine_Regular.ttf"
    if FC==57:
      FONT_FILE = "Fonts/ThechampDemo-2OvqK.ttf"
    if FC==58:
      FONT_FILE = "Fonts/ThechampDemoGradient-K7V2p.ttf"
    if FC==59:
      FONT_FILE = "Fonts/ThechampDemoItalic-MVAwr.ttf"
    if FC==60:
      FONT_FILE = "Fonts/ThechampDemoStroke-vmneO.ttf"
    if FC==61:
      FONT_FILE = "Fonts/Timeburner-xJB8.ttf"
    if FC==62:
      FONT_FILE = "Fonts/TimeburnerBold-peGR.ttf"
    if FC==63:
      FONT_FILE = "Fonts/Windsong.ttf"
    if FC==64:
      FONT_FILE = "Fonts/Zexo-0Myd.ttf"
    if FC==65:
      FONT_FILE = "Fonts/Zexo-4wl4.otf"
    if FC==66:
      FONT_FILE = "Fonts/blackjack.otf"
    if FC==67:
      FONT_FILE = "Fonts/1942.ttf"
    if FC==68:
      FONT_FILE = "Fonts/AguafinaScript-Regular.ttf"
    if FC==69:
      FONT_FILE = "Fonts/AirAmerica-Regular.otf"
    if FC==70:
      FONT_FILE = "Fonts/Airstream.ttf"
    if FC==71:
      FONT_FILE = "Fonts/Amadeus.ttf"
    if FC==72:
      FONT_FILE = "Fonts/berkshireswash-regular.ttf"
    if FC==73:
      FONT_FILE = "Fonts/DEFTONE.ttf"
    if FC==74:
      FONT_FILE = "Fonts/FontleroyBrown.ttf"

    font = ImageFont.truetype(FONT_FILE, size=fontsize)

    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 3
        font = ImageFont.truetype(FONT_FILE, size=fontsize)

    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(((512-width)/2,(512-height)/2), sticktext, font=font, fill=(R, G, B))

    image_stream = io.BytesIO()
    image_stream.name = "sticker.webp"
    image.save(image_stream, "WebP")
    image_stream.seek(0)

    await event.client.send_file(event.chat_id, image_stream, reply_to=event.message.reply_to_msg_id)
    await event.delete()
