from Entity.BaseEntity import *


# 教师
class TeacherEntity(BaseEntity, BaseORM):
    __tablename__ = 'Teacher'

    Account: str = Column(String(128), comment='账号')
    PWD: str = Column(String(128), comment='密码')
    Name: str = Column(String(128), comment='姓名')
    State: int = Column(INTEGER, commont='状态 1正常 2禁用')
    ClassID: int = Column(INTEGER, comment='班级ID')
    UpdateTime: int = Column(INTEGER, comment='更新时间', default=int(time()))
    Token: str = Column(String(128), comment='Token')

    def __init__(self):
        super().__init__()