# -*- coding:utf-8 -*-
from Entity.BaseEntity import *


# 科目
class SubjectEntity(BaseEntity, BaseORM):
    __tablename__ = 'Subject'

    SubjectName: str = Column(String(128), comment='科目名称', default='none')
    SubjectCode: str = Column(String(128), index=True, comment='科目代码', default='none')
    SubjectState: int = Column(INTEGER, comment='科目状态 1正常 2禁用', default=0)
    UpdateTime: int = Column(INTEGER, comment='更新时间', default=int(time()))

    def __init__(self):
        super().__init__()