from Entity.BaseEntity import *


# 报名
class ExamInfoHistoryEntity(BaseEntity, BaseORM):
    __tablename__ = 'ExamInfoHistory'

    SubjectName: str = Column(String(128), comment='科目名称', default='none')
    ExamNo: str = Column(String(128), index=True, comment='准考证号', default='none')
    TotalScore: float = Column(DECIMAL(10, 2), comment='总分', default=0.00)
    PassLine: float = Column(DECIMAL(10, 2), comment='及格线', default=0.00)
    ActualScore: float = Column(DECIMAL(10, 2), comment='真实得分', default=0.00)
    ExamDuration: int = Column(INTEGER, comment='额定考试时长', default=0)
    StartTime: int = Column(INTEGER, comment='实际考试开始时间', default=0)
    EndTime: int = Column(INTEGER, comment='实际考试结束时间', default=0)
    ActualDuration: int = Column(INTEGER, comment='实际考试时长', default=0)
    Pass: int = Column(INTEGER, comment='是否通过 1否 2是', default=0)
    UpdateTime: int = Column(INTEGER, comment='更新时间', default=int(time()))
    ExamineeID: int = Column(INTEGER, comment='考生ID', default=0)
    ExamState: int = Column(INTEGER, comment='考试状态 1未考试 2待考(已经生成答题卡) 3已考试 4作废', default=0)
    ExamType: int = Column(INTEGER, comment='考试类型 1正式考试 2练习')

    def __init__(self):
        super().__init__()