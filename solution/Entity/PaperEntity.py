from Entity.BaseEntity import *


# 试卷
class PaperEntity(BaseEntity, BaseORM):
    __tablename__ = 'Paper'

    PaperName: str = Column(String(128), comment='试卷名称')
    PaperCode: str = Column(String(128), index=True, comment='试卷编码')
    SubjectID: int = Column(INTEGER, comment='科目ID')
    TotalScore: float = Column(DECIMAL(10, 2), comment='总分')
    PassLine: float = Column(DECIMAL(10, 2), comment='及格分数')
    ExamDuration: int = Column(INTEGER, comment='考试时长')
    PaperState: int = Column(INTEGER, comment='试卷状态 1正常 2禁用')
    UpdateTime: int = Column(INTEGER, comment='更新时间', default=int(time()))

    def __init__(self):
        super().__init__()

    def SetPaperName(self, Value: str):
        if isinstance(Value, str):
            self.PaperName = Value.strip()

    def SetPaperCode(self, Value: str):
        if isinstance(Value, str):
            self.PaperCode = Value.strip()

    def SetSubjectID(self, Value: int):
        if isinstance(Value, int):
            self.SubjectID = Value

    def SetTotalScore(self, Value: float):
        if isinstance(Value, float):
            self.TotalScore = Value

    def SetPassLine(self, Value: float):
        if isinstance(Value, float):
            self.PassLine = Value

    def SetExamDuration(self, Value: int):
        if isinstance(Value, int):
            self.ExamDuration = Value

    def SetPaperState(self, Value: int):
        if isinstance(Value, int):
            self.PaperState = Value

    def SetUpdateTime(self, Value: int):
        if isinstance(Value, int):
            self.UpdateTime = Value