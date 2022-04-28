from Entity.BaseEntity import *


# 管理员
class ManagerEntity(BaseEntity, BaseORM):
    __tablename__ = 'Manager'

    Account: str = Column(String(128), comment='账号')
    PWD: str = Column(String(128), comment='密码')
    Name: str = Column(String(128), comment='名称')
    State: int = Column(INTEGER(1), comment='状态 1正常 2禁用')
    Permission: int = Column(INTEGER(1), comment='权限 9 ~ 1 从高到低')
    UpdateTime: int = Column(INTEGER(10), comment='更新时间', default=int(time()))
    Token: str = Column(String(128), comment='Token')

    def __init__(self):
        super().__init__()