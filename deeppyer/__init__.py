#    Copyright (c) 2017 Ovyerus

#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:

#    The above copyright notice and this permission notice shall be included in all
#    copies or substantial portions of the Software.

#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE

from PIL import Image, ImageOps, ImageEnhance
from io import BytesIO
from enum import Enum
import aiohttp, asyncio, math, argparse


class DeepfryTypes(Enum):
    """
    Enum for the various possible effects added to the image.
    """
    RED = 1
    BLUE = 2


class Colours:
    RED = (254, 0, 2)
    YELLOW = (255, 255, 15)
    BLUE = (36, 113, 229)
    WHITE = (255, ) * 3


# TODO: Replace face recognition API with something like OpenCV.


async def deepfry(img: Image,
                  *,
                  token: str = None,
                  url_base: str = 'westcentralus',
                  session: aiohttp.ClientSession = None,
                  type=DeepfryTypes.RED) -> Image:
    """
    Deepfry an image.

    img: PIL.Image - Image to deepfry.
    [token]: str - Token to use for Microsoft facial recognition API. If this is not supplied, lens flares will not be added.
    [url_base]: str = 'westcentralus' - API base to use. Only needed if your key's region is not `westcentralus`.
    [session]: aiohttp.ClientSession - Optional session to use with API requests. If provided, may provide a bit more speed.

    Returns: PIL.Image - Deepfried image.
    """

    img = img.copy().convert('RGB')

    if type not in DeepfryTypes:
        raise ValueError(
            f'Unknown deepfry type "{type}", expected a value from deeppyer.DeepfryTypes'
        )

    if token:
        req_url = f'https://{url_base}.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceId=false&returnFaceLandmarks=true'  # WHY THE FUCK IS THIS SO LONG
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': token,
            'User-Agent': 'DeepPyer/1.0'
        }
        b = BytesIO()

        img.save(b, 'jpeg')
        b.seek(0)

        if session:
            async with session.post(req_url, headers=headers,
                                    data=b.read()) as r:
                face_data = await r.json()
        else:
            async with aiohttp.ClientSession() as s, s.post(
                    req_url, headers=headers, data=b.read()) as r:
                face_data = await r.json()

        if 'error' in face_data:
            err = face_data['error']
            code = err.get('code', err.get('statusCode'))
            msg = err['message']

            raise Exception(
                f'Error with Microsoft Face Recognition API\n{code}: {msg}')

        if face_data:
            landmarks = face_data[0]['faceLandmarks']

            # Get size and positions of eyes, and generate sizes for the flares
            eye_left_width = math.ceil(landmarks['eyeLeftInner']['x'] -
                                       landmarks['eyeLeftOuter']['x'])
            eye_left_height = math.ceil(landmarks['eyeLeftBottom']['y'] -
                                        landmarks['eyeLeftTop']['y'])
            eye_left_corner = (landmarks['eyeLeftOuter']['x'],
                               landmarks['eyeLeftTop']['y'])
            flare_left_size = eye_left_height if eye_left_height > eye_left_width else eye_left_width
            flare_left_size *= 4
            eye_left_corner = tuple(
                math.floor(x - flare_left_size / 2.5 + 5)
                for x in eye_left_corner)

            eye_right_width = math.ceil(landmarks['eyeRightOuter']['x'] -
                                        landmarks['eyeRightInner']['x'])
            eye_right_height = math.ceil(landmarks['eyeRightBottom']['y'] -
                                         landmarks['eyeRightTop']['y'])
            eye_right_corner = (landmarks['eyeRightInner']['x'],
                                landmarks['eyeRightTop']['y'])
            flare_right_size = eye_right_height if eye_right_height > eye_right_width else eye_right_width
            flare_right_size *= 4
            eye_right_corner = tuple(
                math.floor(x - flare_right_size / 2.5 + 5)
                for x in eye_right_corner)

    # Crush image to hell and back
    img = img.convert('RGB')
    width, height = img.width, img.height
    img = img.resize((int(width**.75), int(height**.75)),
                     resample=Image.LANCZOS)
    img = img.resize((int(width**.88), int(height**.88)),
                     resample=Image.BILINEAR)
    img = img.resize((int(width**.9), int(height**.9)), resample=Image.BICUBIC)
    img = img.resize((width, height), resample=Image.BICUBIC)
    img = ImageOps.posterize(img, 4)

    # Generate red and yellow overlay for classic deepfry effect
    r = img.split()[0]
    r = ImageEnhance.Contrast(r).enhance(2.0)
    r = ImageEnhance.Brightness(r).enhance(1.5)

    if type == DeepfryTypes.RED:
        r = ImageOps.colorize(r, Colours.RED, Colours.YELLOW)
    elif type == DeepfryTypes.BLUE:
        r = ImageOps.colorize(r, Colours.BLUE, Colours.WHITE)

    # Overlay red and yellow onto main image and sharpen the hell out of it
    img = Image.blend(img, r, 0.75)
    img = ImageEnhance.Sharpness(img).enhance(100.0)

    if token and face_data:
        # Copy and resize flares
        flare = Image.open('./deeppyer/flare.png')
        flare_left = flare.copy().resize((flare_left_size, ) * 2,
                                         resample=Image.BILINEAR)
        flare_right = flare.copy().resize((flare_right_size, ) * 2,
                                          resample=Image.BILINEAR)

        del flare

        img.paste(flare_left, eye_left_corner, flare_left)
        img.paste(flare_right, eye_right_corner, flare_right)

    return img


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Deepfry an image, optionally adding lens flares for eyes.'
    )
    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version='%(prog)s 1.0',
                        help='Display program version.')
    parser.add_argument('-t',
                        '--token',
                        help='Token to use for facial recognition API.')
    parser.add_argument('-o', '--output', help='Filename to output to.')
    parser.add_argument('file', metavar='FILE', help='File to deepfry.')
    args = parser.parse_args()

    token = args.token
    img = Image.open(args.file)
    out = args.output or './deepfried.jpg'

    loop = asyncio.get_event_loop()
    img = loop.run_until_complete(deepfry(img, token=token))

    img.save(out, 'jpeg')
