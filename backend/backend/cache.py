import json
import os
from typing import Optional, Any
from datetime import timedelta

# 尝试导入Redis，如果失败则使用模拟实现
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None
    print("Redis not available, using mock cache")

class CacheManager:
    def __init__(self):
        if REDIS_AVAILABLE and redis:
            # 从环境变量获取Redis配置
            self.redis_host = os.getenv("REDIS_HOST", "localhost")
            self.redis_port = int(os.getenv("REDIS_PORT", 6379))
            self.redis_db = int(os.getenv("REDIS_DB", 0))
            self.redis_password = os.getenv("REDIS_PASSWORD", None)
            
            # 创建Redis连接
            self.redis_client = redis.Redis(
                host=self.redis_host,
                port=self.redis_port,
                db=self.redis_db,
                password=self.redis_password,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True
            )
        else:
            # 模拟缓存实现
            self.cache = {}
    
    def set(self, key: str, value: Any, expire: Optional[timedelta] = None) -> bool:
        """
        设置缓存值
        :param key: 缓存键
        :param value: 缓存值
        :param expire: 过期时间
        :return: 是否设置成功
        """
        try:
            if REDIS_AVAILABLE and redis:
                # 将值转换为JSON字符串
                serialized_value = json.dumps(value, default=str)
                
                # 设置缓存
                if expire:
                    result = self.redis_client.setex(key, int(expire.total_seconds()), serialized_value)
                else:
                    result = self.redis_client.set(key, serialized_value)
                
                return result
            else:
                # 模拟实现
                self.cache[key] = {
                    'value': value,
                    'expire': None  # 简化实现，不处理过期时间
                }
                return True
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存值
        :param key: 缓存键
        :return: 缓存值或None
        """
        try:
            if REDIS_AVAILABLE and redis:
                value = self.redis_client.get(key)
                if value is None:
                    return None
                
                # 将JSON字符串转换回Python对象
                return json.loads(value)
            else:
                # 模拟实现
                if key in self.cache:
                    return self.cache[key]['value']
                return None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """
        删除缓存值
        :param key: 缓存键
        :return: 是否删除成功
        """
        try:
            if REDIS_AVAILABLE and redis:
                result = self.redis_client.delete(key)
                return result > 0
            else:
                # 模拟实现
                if key in self.cache:
                    del self.cache[key]
                    return True
                return False
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """
        检查缓存键是否存在
        :param key: 缓存键
        :return: 是否存在
        """
        try:
            if REDIS_AVAILABLE and redis:
                return self.redis_client.exists(key) > 0
            else:
                # 模拟实现
                return key in self.cache
        except Exception as e:
            print(f"Cache exists error: {e}")
            return False
    
    def flush(self) -> bool:
        """
        清空所有缓存
        :return: 是否清空成功
        """
        try:
            if REDIS_AVAILABLE and redis:
                self.redis_client.flushdb()
                return True
            else:
                # 模拟实现
                self.cache.clear()
                return True
        except Exception as e:
            print(f"Cache flush error: {e}")
            return False

# 创建全局缓存管理器实例
cache_manager = CacheManager()