from .utils.extdl import install_pip

try:
    import randomstuff
except ModuleNotFoundError:
    install_pip("randomstuff.py")
    import randomstuff

from ..Config import Config

rs_client = randomstuff.AsyncClient(api_key=Config.RANDOM_STUFF_API_KEY, version="4")
