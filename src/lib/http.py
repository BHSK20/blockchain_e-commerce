from urllib.parse import urljoin

import httpx

class AsyncHttpClient:

    def __init__(self, base_url: str) -> None:
        self.client = httpx.AsyncClient()
        if base_url.endswith('/'):
            base_url = base_url[:-1]
        self.base_url = base_url

    async def get(self, url, params={}, headers={}) -> httpx.Response:
        _response = await self.client.get(urljoin(self.base_url, url), params=params, headers=headers)
        return _response

    async def post(self, url, data={}, headers={}) -> httpx.Response:
        _response = await self.client.post(urljoin(self.base_url, url), json=data, headers=headers)
        return _response

    async def put(self, url, data={}, headers={}) -> httpx.Response:
        _response = await self.client.put(urljoin(self.base_url, url), json=data, headers=headers)
        return _response

    async def delete(self, url, data={}, headers={}) -> httpx.Response:
        _response = await self.client.delete(urljoin(self.base_url, url), json=data, headers=headers)
        return _response
