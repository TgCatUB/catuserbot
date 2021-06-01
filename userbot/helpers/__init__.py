from . import fonts
from . import memeshelper as catmemes
from .aiohttp_helper import AioHttp
from .utils import *

flag = True
check = 0
while flag:
    try:
        from .chatbot import *
        from .functions import *
        from .memeifyhelpers import *
        from .progress import *
        from .qhelper import process
        from .tools import *
        from .utils import _cattools, _catutils, _format

        break
    except ModuleNotFoundError as e:
        install_pip(e.name)
        check += 1
        if check > 5:
            break
