# -*- coding:utf-8 -*-
from Entity.BaseEntity import *


# 考生
class ExamineeEntity(BaseEntity, BaseORM):
    __tablename__ = 'Examinee'

    ExamineeNo: str = Column(String(128), index=True, comment='考生编号', default='none')
    Name: str = Column(String(128), comment='考生姓名', default='none')
    ClassID: int = Column(INTEGER, comment='班级ID', default=0)
    Contact: str = Column(String(128), comment='联系方式', default='none')

    def __init__(self):
        super().__init__()