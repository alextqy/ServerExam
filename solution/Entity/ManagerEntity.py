from Entity.BaseEntity import *


# 管理员
class ManagerEntity(BaseEntity, BaseORM):
    __tablename__ = 'Manager'

    Account = Column(String(128), comment='账号')
    PWD = Column(String(128), comment='密码')
    Name = Column(String(128), comment='名称')
    State = Column(INTEGER, comment='状态 1正常 2禁用')
    Permission = Column(INTEGER, comment='权限 9 ~ 1 从高到低')
    UpdateTime = Column(INTEGER, comment='更新时间', default=int(time()))
    Token = Column(String(128), comment='Token')

    def __init__(self):
        super().__init__()