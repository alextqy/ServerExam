from Entity.BaseEntity import *


# 知识点
class KnowledgeEntity(BaseEntity, BaseORM):
    __tablename__ = 'Knowledge'

    KnowledgeName: str = Column(String(128), comment='知识点名称')
    KnowledgeCode: str = Column(String(128), index=True, comment='知识点编码')
    SubjectID: int = Column(INTEGER, index=True, comment='科目ID')
    SubjectState: int = Column(INTEGER, comment='知识点状态 1正常 2禁用')
    UpdateTime: int = Column(INTEGER, comment='更新时间', default=int(time()))

    def __init__(self):
        super().__init__()

    def SetKnowledgeName(self, Value: str):
        if isinstance(Value, str):
            self.KnowledgeName = Value.strip()

    def SetKnowledgeCode(self, Value: str):
        if isinstance(Value, str):
            self.KnowledgeCode = Value.strip()

    def SetSubjectID(self, Value: int):
        if isinstance(Value, int):
            self.SubjectID = Value

    def SetSubjectState(self, Value: int):
        if isinstance(Value, int):
            self.SubjectState = Value

    def SetUpdateTime(self, Value: int):
        if isinstance(Value, int):
            self.UpdateTime = Value