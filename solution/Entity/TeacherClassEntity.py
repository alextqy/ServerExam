# -*- coding:utf-8 -*-
from Entity.BaseEntity import *


# 教师 班级 对应表
class TeacherClassEntity(BaseEntity, BaseORM):
    __tablename__ = 'TeacherClass'

    TeacherID: int = Column(INTEGER, comment='教师ID', default=0)
    ClassID: int = Column(INTEGER, comment='班级ID', default=0)

    def __init__(self):
        super().__init__()