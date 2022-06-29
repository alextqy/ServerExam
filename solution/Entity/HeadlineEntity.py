# -*- coding:utf-8 -*-
from Entity.BaseEntity import *


# 大标题
class HeadlineEntity(BaseEntity, BaseORM):
    __tablename__ = 'Headline'

    Content: str = Column(String(65535), comment='内容', default='none')
    ContentCode: str = Column(String(128), comment='内容编码', default='none')
    UpdateTime: int = Column(INTEGER, comment='更新时间', default=int(time()))

    def __init__(self):
        super().__init__()