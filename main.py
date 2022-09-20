import asyncio
from typing import Any, Coroutine

import aiohttp
from aiohttp import ClientSession


class _BaseAsyncRequester:
    def __init__(self, url: str, repeat: int) -> None:
        self.url: str = url
        self.repeat: int = repeat
    
    async def _get_data(self, url: str, __session: ClientSession) -> Coroutine[Any, Any, Any]:
        async with __session.get(url) as response:
            return await response.json()
    
    async def _base_request(self) -> Any:
        async with aiohttp.ClientSession() as session:
            tasks: list[Any] = []
            
            for i in range(self.repeat):
                tasks.append(asyncio.ensure_future(self._get_data(self.url, session)))
            
            original_data: Any = await asyncio.gather(*tasks)
            
            return original_data


class AsyncRequester(_BaseAsyncRequester):
    def __init__(self, url: str, repeat: int) -> None:
        super().__init__(url, repeat)
    
    def request(self) -> Any:
        return asyncio.run(self._base_request())
