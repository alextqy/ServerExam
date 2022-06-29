# -*- coding:utf-8 -*-
from Entity.BaseEntity import *


# 班级
class ClassEntity(BaseEntity, BaseORM):
    __tablename__ = 'Class'

    ClassName: str = Column(String(128), comment='班级名称', default='none')
    ClassCode: str = Column(String(128), index=True, comment='班级编号', default='none')
    Description: str = Column(String(65535), comment='描述信息', default='none')

    def __init__(self):
        super().__init__()