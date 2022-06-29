# -*- coding:utf-8 -*-
from Entity.BaseEntity import *


# 系统日志
class SysLogEntity(BaseEntity, BaseORM):
    __tablename__ = 'SysLog'

    Type: int = Column(INTEGER, comment='日志类型 1操作 2登录', default=0)
    ManagerID: int = Column(INTEGER, comment='管理员ID', default=0)
    Description: str = Column(String(65535), comment='描述信息', default='none')
    IP: str = Column(String(128), comment='IP地址', default='none')

    def __init__(self):
        super().__init__()