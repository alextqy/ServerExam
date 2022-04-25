from Entity.BaseEntity import *


class ScantronSolutionEntity(BaseEntity):
    __tablename__ = 'ScantronSolution'

    ScantronID = Column(INTEGER, comment='试题ID')
    Option = Column(String(128), comment='试题选项')
    OptionAttachment = Column(String(65535), comment='试题附件')
    CorrectAnswer = Column(String(128), comment='正确答案')
    CandidateAnswer = Column(String(128), comment='考生答案')
    ScoreRatio = Column(DECIMAL(10, 2), comment='得分比例')
    UpdateTime = Column(INTEGER, comment='更新时间')