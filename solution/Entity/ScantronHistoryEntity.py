from Entity.BaseEntity import *


# 历史答题卡
class ScantronHistoryEntity(BaseEntity, BaseORM):
    __tablename__ = 'ScantronHistory'

    QuestionTitle: str = Column(String(65535), comment='标题')
    QuestionCode: str = Column(String(128), comment='试题编码')
    QuestionType: int = Column(INTEGER, comment='试题类型 1单选 2判断 3多选 4填空 5问答 6代码实训 7拖拽题 8连线题')
    Marking: int = Column(INTEGER, comment='人工阅卷 1否 2是')
    KnowledgeID: int = Column(INTEGER, comment='知识点ID')
    Description: str = Column(String(65535), comment='试题描述')
    Attachment: str = Column(String(65535), comment='试题附件')
    UpdateTime: int = Column(INTEGER, comment='更新时间', default=int(time()))
    Score: float = Column(DECIMAL(10, 2), comment='额定分数')
    ExamID: int = Column(INTEGER, comment='报名ID')
    HeadlineContent: str = Column(String(65535), comment='大标题内容')

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

    def SetScore(self, Value: float):
        if isinstance(Value, float):
            self.Score = Value

    def SetExamID(self, Value: int):
        if isinstance(Value, int):
            self.ExamID = Value

    def SetHeadlineContent(self, Value: str):
        if isinstance(Value, str):
            self.HeadlineContent = Value.strip()