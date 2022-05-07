from Entity.BaseEntity import *


# 系统日志
class SysLogEntity(BaseEntity, BaseORM):
    __tablename__ = 'SysLog'

    Type: int = Column(INTEGER, comment='日志类型 1操作 2登录')
    ManagerID: int = Column(INTEGER, comment='管理员ID')
    Description: str = Column(String(65535), comment='描述信息')
    IP: str = Column(String(128), comment='IP地址')

    def __init__(self):
        super().__init__()

    def SetType(self, Value: int):
        if isinstance(Value, int):
            self.Type = Value

    def SetManagerID(self, Value: int):
        if isinstance(Value, int):
            self.ManagerID = Value

    def SetDescription(self, Value: str):
        if isinstance(Value, str):
            self.Description = Value.strip()

    def SetIP(self, Value: str):
        if isinstance(Value, str):
            self.IP = Value.strip()