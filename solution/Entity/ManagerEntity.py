from Entity.BaseEntity import *


# 管理员
class ManagerEntity(BaseEntity, BaseORM):
    __tablename__ = 'Manager'

    Account: str = Column(String(128), comment='账号', default='none')
    PWD: str = Column(String(128), comment='密码', default='none')
    Name: str = Column(String(128), comment='名称', default='none')
    State: int = Column(INTEGER, comment='状态 1正常 2禁用', default=0)
    Permission: int = Column(INTEGER, comment='权限 9 ~ 1 从高到低', default=0)
    UpdateTime: int = Column(INTEGER, comment='更新时间', default=int(time()))
    Token: str = Column(String(128), comment='Token', default='none')

    def __init__(self):
        super().__init__()