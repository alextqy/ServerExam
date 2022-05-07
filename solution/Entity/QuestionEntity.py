from Entity.BaseEntity import *


# 试题
class QuestionEntity(BaseEntity, BaseORM):
    __tablename__ = 'Question'

    QuestionTitle: str = Column(String(65535), comment='题目')
    QuestionCode: str = Column(String(128), index=True, comment='试题编码')
    QuestionType: int = Column(INTEGER, comment='试题类型 1单选 2判断 3多选 4填空 5问答 6代码实训 7拖拽题 8连线题')
    QuestionState: int = Column(INTEGER, comment='试题状态 1正常 2禁用')
    Marking: int = Column(INTEGER, comment='人工阅卷 1否 2是')
    KnowledgeID: int = Column(INTEGER, comment='知识点ID')
    Description: str = Column(String(65535), comment='试题描述')
    Attachment: str = Column(String(65535), comment='试题附件')
    UpdateTime: int = Column(INTEGER, comment='更新时间', default=int(time()))

    def __init__(self):
        super().__init__()

    def SetQuestionTitle(self, Value: str):
        if isinstance(Value, str):
            self.QuestionTitle = Value.strip()

    def SetQuestionCode(self, Value: str):
        if isinstance(Value, str):
            self.QuestionCode = Value.strip()

    def SetQuestionType(self, Value: int):
        if isinstance(Value, int):
            self.QuestionType = Value

    def SetQuestionState(self, Value: int):
        if isinstance(Value, int):
            self.QuestionState = Value

    def SetMarking(self, Value: int):
        if isinstance(Value, int):
            self.Marking = Value

    def SetKnowledgeID(self, Value: int):
        if isinstance(Value, int):
            self.KnowledgeID = Value

    def SetDescription(self, Value: str):
        if isinstance(Value, str):
            self.Description = Value.strip()

    def SetAttachment(self, Value: str):
        if isinstance(Value, str):
            self.Attachment = Value.strip()

    def SetUpdateTime(self, Value: int):
        if isinstance(Value, int):
            self.UpdateTime = Value