from Entity.BaseEntity import *


# 系统配置
class SysConfEntity(BaseEntity, BaseORM):
    __tablename__ = 'SysConf'

    Type: int = Column(INTEGER, comment='配置类型')
    Key: str = Column(String(128), comment='配置KEY')
    Value: str = Column(String(128), comment='配置Value')
    Description: str = Column(String(128), comment='配置描述')

    def __init__(self):
        super().__init__()

    def SetType(self, Value: int):
        if isinstance(Value, int):
            self.Type = Value

    def SetKey(self, Value: str):
        if isinstance(Value, str):
            self.Key = Value.strip()

    def SetValue(self, Value: str):
        if isinstance(Value, str):
            self.Value = Value.strip()

    def SetDescription(self, Value: str):
        if isinstance(Value, str):
            self.Description = Value.strip()