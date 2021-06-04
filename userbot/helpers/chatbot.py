import randomstuff

from ..Config import Config

rs_client = randomstuff.AsyncClient(api_key=Config.RANDOM_STUFF_API_KEY, version="4")
