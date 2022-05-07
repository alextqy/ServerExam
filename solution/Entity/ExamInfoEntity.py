from Entity.BaseEntity import *


# 报名
class ExamInfoEntity(BaseEntity, BaseORM):
    __tablename__ = 'ExamInfo'

    SubjectName: str = Column(String(128), comment='科目名称')
    ExamNo: str = Column(String(128), index=True, comment='准考证号')
    TotalScore: float = Column(DECIMAL(10, 2), comment='总分')
    PassLine: float = Column(DECIMAL(10, 2), comment='及格线')
    ActualScore: float = Column(DECIMAL(10, 2), comment='真实得分')
    ExamDuration: int = Column(INTEGER, comment='额定考试时长')
    StartTime: int = Column(INTEGER, comment='实际考试开始时间')
    EndTime: int = Column(INTEGER, comment='实际考试结束时间')
    ActualDuration: int = Column(INTEGER, comment='实际考试时长')
    Pass: int = Column(INTEGER, comment='是否通过 1否 2是')
    UpdateTime: int = Column(INTEGER, comment='更新时间', default=int(time()))
    ExamineeID: int = Column(INTEGER, comment='考生ID')

    def __init__(self):
        super().__init__()

    def SetSubjectName(self, Value: str):
        if isinstance(Value, str):
            self.SubjectName = Value.strip()

    def SetExamNo(self, Value: str):
        if isinstance(Value, str):
            self.ExamNo = Value.strip()

    def SetTotalScore(self, Value: float):
        if isinstance(Value, float):
            self.TotalScore = Value

    def SetPassLine(self, Value: float):
        if isinstance(Value, float):
            self.PassLine = Value

    def SetActualScore(self, Value: float):
        if isinstance(Value, float):
            self.ActualScore = Value

    def SetExamDuration(self, Value: int):
        if isinstance(Value, int):
            self.ExamDuration = Value

    def SetStartTime(self, Value: int):
        if isinstance(Value, int):
            self.StartTime = Value

    def SetEndTime(self, Value: int):
        if isinstance(Value, int):
            self.EndTime = Value

    def SetActualDuration(self, Value: int):
        if isinstance(Value, int):
            self.ActualDuration = Value

    def SetPass(self, Value: int):
        if isinstance(Value, int):
            self.Pass = Value

    def SetUpdateTime(self, Value: int):
        if isinstance(Value, int):
            self.UpdateTime = Value

    def SetExamineeID(self, Value: int):
        if isinstance(Value, int):
            self.ExamineeID = Value