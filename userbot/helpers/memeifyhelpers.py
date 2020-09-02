from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from os import getcwd
from os.path import join
from textwrap import wrap
from wand.drawing import Drawing
from wand.image import Image as catimage
from wand.color import Color

MARGINS = [50, 150, 250, 350, 450]


def get_warp_length(width):
    return int((20.0 / 1024.0) * (width + 0.0))


async def cat_meme(topString, bottomString, filename, endname):
    img = Image.open(filename)
    imageSize = img.size
    # find biggest font size that works
    fontSize = int(imageSize[1] / 5)
    font = ImageFont.truetype("userbot/helpers/styles/impact.ttf", fontSize)
    topTextSize = font.getsize(topString)
    bottomTextSize = font.getsize(bottomString)
    while topTextSize[0] > imageSize[0] - \
            20 or bottomTextSize[0] > imageSize[0] - 20:
        fontSize = fontSize - 1
        font = ImageFont.truetype(
            "userbot/helpers/styles/impact.ttf", fontSize)
        topTextSize = font.getsize(topString)
        bottomTextSize = font.getsize(bottomString)

    # find top centered position for top text
    topTextPositionX = (imageSize[0] / 2) - (topTextSize[0] / 2)
    topTextPositionY = 0
    topTextPosition = (topTextPositionX, topTextPositionY)

    # find bottom centered position for bottom text
    bottomTextPositionX = (imageSize[0] / 2) - (bottomTextSize[0] / 2)
    bottomTextPositionY = imageSize[1] - bottomTextSize[1]
    bottomTextPosition = (bottomTextPositionX, bottomTextPositionY)
    draw = ImageDraw.Draw(img)
    # draw outlines
    # there may be a better way
    outlineRange = int(fontSize / 15)
    for x in range(-outlineRange, outlineRange + 1):
        for y in range(-outlineRange, outlineRange + 1):
            draw.text((topTextPosition[0] +
                       x, topTextPosition[1] +
                       y), topString, (0, 0, 0), font=font)
            draw.text((bottomTextPosition[0] +
                       x, bottomTextPosition[1] +
                       y), bottomString, (0, 0, 0), font=font)
    draw.text(topTextPosition, topString, (255, 255, 255), font=font)
    draw.text(bottomTextPosition, bottomString, (255, 255, 255), font=font)
    img.save(endname)


async def cat_meeme(upper_text, lower_text, picture_name, endname):
    main_image = catimage(filename=picture_name)
    main_image.resize(1024, int(
        ((main_image.height * 1.0) / (main_image.width * 1.0)) * 1024.0))
    upper_text = "\n".join(
        wrap(
            upper_text,
            get_warp_length(
                main_image.width))).upper()
    lower_text = "\n".join(
        wrap(
            lower_text,
            get_warp_length(
                main_image.width))).upper()
    lower_margin = MARGINS[lower_text.count("\n")]
    text_draw = Drawing()
    text_draw.font = join(getcwd(), "userbot/helpers/styles/impact.ttf")
    text_draw.font_size = 100
    text_draw.text_alignment = "center"
    text_draw.stroke_color = Color("black")
    text_draw.stroke_width = 3
    text_draw.fill_color = Color("white")
    if upper_text:
        text_draw.text((main_image.width) // 2, 80, upper_text)
    if lower_text:
        text_draw.text(
            (main_image.width) //
            2,
            main_image.height -
            lower_margin,
            lower_text)
    text_draw(main_image)
    main_image.save(filename=endname)
