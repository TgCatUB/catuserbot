# deeppyer
![banner image](./banner.jpg)

deeppyer is an image deepfryer written in Python using [Pillow](https://python-pillow.org/
) and using the [Microsoft Facial Recognition API](https://azure.microsoft.com/services/cognitive-services/face/).

NOTE: This *requires* at least Python v3.6 in order to run.

## How to use
You can either use deeppyer as a module, or straight from the command line.

### Command line usage
```
$ python deeppyer.py -h

usage: deeppyer.py [-h] [-v] [-t TOKEN] [-o OUTPUT] FILE

Deepfry an image, optionally adding lens flares for eyes.

positional arguments:
  FILE                  File to deepfry.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Display program version.
  -t TOKEN, --token TOKEN
                        Token to use for facial recognition API.
  -o OUTPUT, --output OUTPUT
                        Filename to output to.
```

When a token is supplied, the script will automatically try to add lens flares for the eyes, otherwise it won't.

### Program usage
```py
from PIL import Image
import deeppyer, asyncio

async def main():
    img = Image.open('./foo.jpg')
    img = await deeppyer.deepfry(img, token='optional token')
    img.save('./bar.jpg')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## API Documentation
#### `async deeppyer.deepfry(img: PIL.Image, *, token: str=None, url_base: str='westcentralus', session: aiohttp.ClientSession=None)`
Deepfry a given image.

**Arguments**
 - *img* (PIL.Image) - Image to apply the deepfry effect on.
 - *[token]* (str) - Token to use for the facial recognition API. Defining this will add lens flares to the eyes of a face in the image.
 - *[url_base]* (str='westcentralus') - URL base to use for the facial recognition API. Can either be `westus`, `eastus2`, `westcentralus`, `westeurope` or `southeastasia`.
 - *[session]* (aiohttp.ClientSession) - Optional session to use when making the request to the API. May make it a tad faster if you already have a created session, and allows you to give it your own options.

Returns:
  `PIL.Image` - Deepfried image.

## Why?
¯\\\_(ツ)_/¯ Why not

## Contributing
If you wish to contribute something to this, go ahead! Just please try to keep your code similar-ish to mine, and make sure that it works with the tests.

## Testing
Create a file in [tests](./tests) called `token.json` with the following format:
```json
{
    "token": "",
    "url_base": ""
}
```
`token` is your token for the facial recognition API.
`url_base` is optional, and is for if your token is from a different region.

After that, simply run `test.py` and make sure that all the images output as you want.