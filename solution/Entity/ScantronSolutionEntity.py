from Entity.BaseEntity import *


# 答题卡选项
class ScantronSolutionEntity(BaseEntity, BaseORM):
    __tablename__ = 'ScantronSolution'

    ScantronID: int = Column(INTEGER, comment='试题ID')
    Option: str = Column(String(128), comment='试题选项')
    OptionAttachment: str = Column(String(65535), comment='试题附件')
    CorrectAnswer: str = Column(String(128), comment='正确答案')
    CandidateAnswer: str = Column(String(128), comment='考生答案')
    ScoreRatio: float = Column(DECIMAL(10, 2), comment='得分比例')
    Position: int = Column(INTEGER, comment='拖拽题/连线题 展示位置 1左 2右')
    UpdateTime: int = Column(INTEGER, comment='更新时间', default=int(time()))

    def __init__(self):
        super().__init__()

    def SetScantronID(self, Value: int):
        if isinstance(Value, int):
            self.ScantronID = Value

    def SetOption(self, Value: str):
        if isinstance(Value, str):
            self.Option = Value.strip()

    def SetOptionAttachment(self, Value: str):
        if isinstance(Value, str):
            self.OptionAttachment = Value.strip()

    def SetCorrectAnswer(self, Value: str):
        if isinstance(Value, str):
            self.CorrectAnswer = Value.strip()

    def SetCandidateAnswer(self, Value: str):
        if isinstance(Value, str):
            self.CandidateAnswer = Value.strip()

    def SetScoreRatio(self, Value: float):
        if isinstance(Value, float):
            self.ScoreRatio = Value

    def SetPosition(self, Value: int):
        if isinstance(Value, int):
            self.Position = Value

    def SetUpdateTime(self, Value: int):
        if isinstance(Value, int):
            self.UpdateTime = Value