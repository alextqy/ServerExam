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