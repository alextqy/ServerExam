# -*- coding:utf-8 -*-
from Entity.BaseEntity import *


# 系统配置
class SysConfEntity(BaseEntity, BaseORM):
    __tablename__ = 'SysConf'

    Type: int = Column(INTEGER, comment='配置类型', default=0)
    Key: str = Column(String(128), comment='配置KEY', default='none')
    Value: str = Column(String(128), comment='配置Value', default='none')
    Description: str = Column(String(128), comment='配置描述', default='none')

    def __init__(self):
        super().__init__()