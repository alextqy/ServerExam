# -*- coding:utf-8 -*-
from Entity.BaseEntity import *


# 教师
class TeacherEntity(BaseEntity, BaseORM):
    __tablename__ = 'Teacher'

    Account: str = Column(String(128), comment='账号', default='none')
    Password: str = Column(String(128), comment='密码', default='none')
    Name: str = Column(String(128), comment='姓名', default='none')
    State: int = Column(INTEGER, comment='状态 1正常 2禁用', default=0)
    ClassID: int = Column(INTEGER, comment='班级ID', default=0)
    UpdateTime: int = Column(INTEGER, comment='更新时间', default=int(time()))
    Token: str = Column(String(128), comment='Token', default='none')

    def __init__(self):
        super().__init__()