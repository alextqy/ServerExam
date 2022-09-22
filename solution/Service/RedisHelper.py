# -*- coding:utf-8 -*-
from Service.BaseService import *
from Service.Common import *


class RedisHelper(BaseService):

    def __init__(self):
        super().__init__()
        self.Common = Common()
        self.ConfigObj: dict = self.Common.ReadJsonFile(path[0] + '/config.json')
        self.RedisPool = redis.ConnectionPool(
            host=self.ConfigObj['RedisAddr'],
            port=self.ConfigObj['RedisPort'],
            password=self.ConfigObj['RedisPWD'],
            db=self.ConfigObj['RedisDB'],
        )
        self.RedisObject = redis.Redis(connection_pool=self.RedisPool)

    # 清空
    def Clean(self) -> bool:
        return self.RedisObject.flushall(False)

    # 新建数据
    def Set(self, Key, Value, Seconds: int = 60) -> bool:
        return self.RedisObject.set(Key, Value, Seconds)

    # 更新Key失效时间
    def SetTIme(self, Key: str, Time: int) -> bool:
        return self.RedisObject.expire(Key, Time)

    # 取值
    def Get(self, Key: str) -> any:
        return self.RedisObject.get(Key)

    # 更新Value并获取旧Value 更新后时间为永久
    def GetOldSet(self, Key: str, Value: any) -> any:
        return self.RedisObject.getset(Key, Value)

    # 剩余时间
    def GetTIme(self, Key: str) -> int:
        return self.RedisObject.ttl(Key)

    # 获取Value的类型
    def GetType(self, Key: str) -> any:
        return self.RedisObject.type(Key)

    # Key是否存在 0不存在 1存在
    def KeyExists(self, Key: str) -> int:
        return self.RedisObject.exists(Key)

    # 删除指定键值对 返回影响行数
    def Del(self, Key: str) -> int:
        return self.RedisObject.delete(Key)

    # ====================== hash操作 ======================

    # 设置hash数据 0失败 1成功
    def HSet(self, Key: str, SubKey: str, JsonValue: str) -> int:
        return self.RedisObject.hset(Key, SubKey, JsonValue)

    # 获取指定列表下的Key值
    def HGet(self, Key: str, SubKey: str) -> any:
        return self.RedisObject.hget(Key, SubKey)

    # 获取hash表下所有的键值对
    def HAll(self, Key: str) -> dict:
        return self.RedisObject.hgetall(Key)

    # 获取hash表下所有Key
    def HAllKey(self, Key: str) -> list:
        return self.RedisObject.hkeys(Key)

    # 获取hash表下所有值
    def HAllVals(self, Key: str) -> list:
        return self.RedisObject.hvals(Key)

    # hash表下是否存在指定Key
    def HKeyExists(self, Key: str, SubKey: str) -> bool:
        return self.RedisObject.hexists(Key, SubKey)

    # 删除hash表下指定键值对 返回影响行数
    def HDel(self, Key: str, SubKey: str) -> bool:
        return self.RedisObject.hdel(Key, SubKey)

    # 获取当前所有的Key
    def HKeys(self) -> list:
        return self.RedisObject.keys()

    # ====================== 队列 ======================

    # 左入 返回最后的ID
    def LPush(self, Key: str, Value: any) -> int:
        return self.RedisObject.lpush(Key, Value)

    # 从右侧头部取出
    def RPOP(self, Key: str) -> any:
        return self.RedisObject.rpop(Key)

    # 右入 返回最后的ID
    def RPush(self, Key: str, Value: any) -> int:
        return self.RedisObject.rpush(Key, Value)

    # 从左侧头部取出
    def LPOP(self, Key: str) -> any:
        return self.RedisObject.lpop(Key)

    # 队列长度
    def CountQueue(self, QueueName: str) -> int:
        return self.RedisObject.llen(QueueName)