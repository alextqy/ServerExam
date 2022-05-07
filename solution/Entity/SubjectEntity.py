from Entity.BaseEntity import *


# 科目
class SubjectEntity(BaseEntity, BaseORM):
    __tablename__ = 'Subject'

    SubjectName: str = Column(String(128), comment='科目名称')
    SubjectCode: str = Column(String(128), index=True, comment='科目编码')
    SubjectState: int = Column(INTEGER, comment='科目状态 1正常 2禁用')
    UpdateTime: int = Column(INTEGER, comment='更新时间', default=int(time()))

    def __init__(self):
        super().__init__()

    def SetSubjectName(self, Value: str):
        if isinstance(Value, str):
            self.SubjectName = Value.strip()

    def SetSubjectCode(self, Value: str):
        if isinstance(Value, str):
            self.SubjectCode = Value.strip()

    def SetSubjectState(self, Value: int):
        if isinstance(Value, int):
            self.SubjectState = Value

    def SetUpdateTime(self, Value: int):
        if isinstance(Value, int):
            self.UpdateTime = Value