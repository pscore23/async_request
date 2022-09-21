import asyncio
import json
from typing import Any, Coroutine

import aiohttp
from aiohttp import ClientSession

import _exceptions


class _BaseAsyncRequester:
    def __init__(self, url: str, repeat: int, method: str, data: Any, headers: dict) -> None:
        self.url: str = url
        self.repeat: int = repeat
        self.method: str = method
        self.data: Any = data
        self.headers: dict = headers
    
    async def _get_data(self, url: str, __session: ClientSession) -> Coroutine[Any, Any, Any]:
        async with __session.get(url) as response:
            return await response.json()
    
    async def _post_data(self, url: str, data: Any, __session: ClientSession) -> Coroutine[Any, Any, Any]:
        async with __session.post(url, data=json.dumps(data)) as response:
            return await response.json()
    
    async def _base_request(self) -> Any:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            tasks: list[Any] = []
            
            for i in range(self.repeat):
                if self.method == "GET":
                    tasks.append(asyncio.ensure_future(self._get_data(self.url, session)))
                
                elif self.method == "POST":
                    tasks.append(asyncio.ensure_future(self._post_data(self.url, self.data, session)))
                
                else:
                    raise _exceptions.InputError("指定されたメソッドが見つかりません")
            
            original_data: Any = await asyncio.gather(*tasks)
            
            return original_data


class AsyncRequester(_BaseAsyncRequester):
    def __init__(self, url: str, repeat: int, method: str = "GET", data: Any = {}, headers: dict = {}) -> None:
        super().__init__(url, repeat, method, data, headers)
    
    def request(self) -> Any:
        return asyncio.run(self._base_request())
