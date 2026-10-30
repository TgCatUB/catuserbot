import httpx


class AioHttp:
    @staticmethod
    async def get_json(link):
        async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
            return (await client.get(link)).json()

    @staticmethod
    async def get_text(link):
        async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
            return (await client.get(link)).text

    @staticmethod
    async def get_raw(link):
        async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
            return (await client.get(link)).content

    @staticmethod
    async def get_status(link):
        async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
            return (await client.get(link)).status_code
