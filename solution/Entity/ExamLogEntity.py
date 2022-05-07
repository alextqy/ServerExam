from Entity.BaseEntity import *


# 考生日志
class ExamLogEntity(BaseEntity, BaseORM):
    __tablename__ = 'ExamLog'

    Type: int = Column(INTEGER, comment='日志类型 1操作 2登录')
    ExamNo: str = Column(String(128), comment='准考证号')
    Description: str = Column(String(65535), comment='描述信息')
    IP: str = Column(String(128), comment='IP地址')

    def __init__(self):
        super().__init__()

    def SetType(self, Value: int):
        if isinstance(Value, int):
            self.Type = Value

    def SetExamNo(self, Value: str):
        if isinstance(Value, str):
            self.ExamNo = Value.strip()

    def SetDescription(self, Value: str):
        if isinstance(Value, str):
            self.Description = Value.strip()

    def SetIP(self, Value: str):
        if isinstance(Value, str):
            self.IP = Value.strip()