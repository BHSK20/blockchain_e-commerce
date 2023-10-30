from redis.asyncio import Redis
from redis.asyncio.cluster import RedisCluster
from typing import Dict, Any, Union
import json
import traceback

class Cache:

    def __init__(self, redis: Union[Redis, RedisCluster, None] = None) -> None:
        self.redis = redis

    def get_key(self, filter: Dict) -> str:
        _keys = list(filter.keys())
        _keys.sort()
        _key_items = [f'{k}.{filter[k]}' for k in _keys]
        return ':'.join(_key_items)

    async def set(self, filter: Dict, data: Any, ttl: float = -1) -> None:
        _key = self.get_key(filter)
        if isinstance(data, dict):
            data = json.dumps(data)
        if ttl == -1:
            await self.redis.set(_key, data)
        else:
            await self.redis.set(_key, data, ex=ttl)

    async def get(self, filter: Dict) -> Any:
        if not self.redis:
            raise Exception()
        _key = self.get_key(filter)
        data: bytes = await self.redis.get(_key)
        return data.decode()

    async def hset(self, filter: Dict, hset_key: Any, data: Any) -> None:
        _key = self.get_key(filter)
        _hset_val = filter.get(hset_key)
        if isinstance(data, dict) or isinstance(data, list):
            data = json.dumps(data)
        await self.redis.hset(_key, str(_hset_val), data)

    async def hget(self, filter: Dict, hset_val: str):
        _key = self.get_key(filter)
        return await self.redis.hget(_key, hset_val)

    async def hget_all(self, filter: Dict):
        _key = self.get_key(filter)
        try:
            return await self.redis.hgetall(_key)
        except:
            traceback.print_exc()
            return None
