import asyncio
import typing

import aiohttp


class AsyncRequester:
    def __init__(self, url: str, repeat: int) -> None:
        self.url: str = url
        self.repeat: int = repeat
    
    async def _get_data(self, url: str, __session: aiohttp.ClientSession) -> typing.Coroutine[typing.Any, typing.Any, typing.Any]:
        async with __session.get(url) as response:
            return await response.json()
    
    async def request(self) -> typing.Any:
        async with aiohttp.ClientSession() as session:
            tasks: list[typing.Any] = []
            
            for i in range(self.repeat):
                tasks.append(asyncio.ensure_future(self._get_data(self.url, session)))
            
            original_data: typing.Any = await asyncio.gather(*tasks)
            
            return original_data
