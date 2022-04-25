from Entity.BaseEntity import *


# 试卷
class PaperEntity(BaseEntity):
    __tablename__ = 'Paper'

    PaperName = Column(String(128), comment='试卷名称')
    PaperCode = Column(String(128), index=True, comment='试卷编码')
    SubjectID = Column(INTEGER, comment='科目ID')
    TotalScore = Column(DECIMAL(10, 2), comment='总分')
    PassLine = Column(DECIMAL(10, 2), comment='及格分数')
    ExamDuration = Column(INTEGER, comment='考试时长')
    PaperState = Column(INTEGER, comment='试卷状态 1正常 2禁用')
    UpdateTime = Column(INTEGER, comment='更新时间')