from Entity.BaseEntity import *


# 考生
class ExamineeEntity(BaseEntity, BaseORM):
    __tablename__ = 'Examinee'

    Name: str = Column(String(128), comment='考生姓名')
    ExamineeNo: str = Column(String(128), index=True, comment='考生编号')
    Contact: str = Column(String(128), comment='联系方式')
    ClassID: int = Column(INTEGER, comment='班级ID')

    def __init__(self):
        super().__init__()

    def SetName(self, Value: str):
        if isinstance(Value, str):
            self.Name = Value.strip()

    def SetExamineeNo(self, Value: str):
        if isinstance(Value, str):
            self.ExamineeNo = Value.strip()

    def SetContact(self, Value: str):
        if isinstance(Value, str):
            self.Contact = Value.strip()

    def SetClassID(self, Value: int):
        if isinstance(Value, int):
            self.ClassID = Value