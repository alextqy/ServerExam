from Entity.BaseEntity import *


# 班级
class ClassEntity(BaseEntity, BaseORM):
    __tablename__ = 'Class'

    ClassName: str = Column(String(128), comment='班级名称')
    ClassCode: str = Column(String(128), index=True, comment='班级编号')
    Description: str = Column(String(65535), comment='描述信息')

    def __init__(self):
        super().__init__()

    def SetClassName(self, Value: str):
        if isinstance(Value, str):
            self.ClassName = Value.strip()

    def SetClassCode(self, Value: str):
        if isinstance(Value, str):
            self.ClassCode = Value.strip()

    def SetDescription(self, Value: str):
        if isinstance(Value, str):
            self.Description = Value.strip()