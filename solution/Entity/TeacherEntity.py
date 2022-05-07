from Entity.BaseEntity import *


# 教师
class TeacherEntity(BaseEntity, BaseORM):
    __tablename__ = 'Teacher'

    Account: str = Column(String(128), comment='账号')
    PWD: str = Column(String(128), comment='密码')
    Name: str = Column(String(128), comment='姓名')
    State: int = Column(INTEGER, comment='状态 1正常 2禁用')
    ClassID: int = Column(INTEGER, comment='班级ID')
    UpdateTime: int = Column(INTEGER, comment='更新时间', default=int(time()))
    Token: str = Column(String(128), comment='Token')

    def __init__(self):
        super().__init__()

    def SetAccount(self, Value: str):
        if isinstance(Value, str):
            self.Account = Value.strip()

    def SetPWD(self, Value: str):
        if isinstance(Value, str):
            self.PWD = Value.strip()

    def SetName(self, Value: str):
        if isinstance(Value, str):
            self.Name = Value.strip()

    def SetState(self, Value: int):
        if isinstance(Value, int):
            self.State = Value

    def SetClassID(self, Value: int):
        if isinstance(Value, int):
            self.ClassID = Value

    def SetUpdateTime(self, Value: int):
        if isinstance(Value, int):
            self.UpdateTime = Value

    def SetToken(self, Value: str):
        if isinstance(Value, str):
            self.Token = Value.strip()