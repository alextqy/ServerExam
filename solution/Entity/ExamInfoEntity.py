from decimal import Decimal
from Entity.BaseEntity import *


# 报名
class ExamInfoEntity(BaseEntity):
    __tablename__ = 'ExamineeToken'

    SubjectName = Column(String(128), comment='科目名称')
    ExamNo = Column(String(128), index=True, comment='准考证号')
    TotalScore = Column(DECIMAL(10, 2), comment='总分')
    PassLine = Column(DECIMAL(10, 2), comment='及格线')
    ActualScore = Column(DECIMAL(10, 2), comment='真实得分')
    ExamDuration = Column(INTEGER, comment='额定考试时长')
    StartTime = Column(INTEGER, comment='实际考试开始时间')
    EndTime = Column(INTEGER, comment='实际考试结束时间')
    ActualDuration = Column(INTEGER, comment='实际考试时长')
    Pass = Column(INTEGER, comment='是否通过 1否 2是')
    UpdateTime = Column(INTEGER, comment='更新时间')
    ExamineeID = Column(INTEGER, comment='考生ID')
