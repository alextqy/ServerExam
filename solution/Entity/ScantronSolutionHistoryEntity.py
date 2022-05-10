from Entity.BaseEntity import *


# 历史答题卡选项
class ScantronSolutionHistoryEntity(BaseEntity, BaseORM):
    __tablename__ = 'ScantronSolutionHistory'

    ScantronID: int = Column(INTEGER, comment='试题ID', default=0)
    Option: str = Column(String(128), comment='试题选项', default='none')
    OptionAttachment: str = Column(String(65535), comment='试题附件', default='none')
    CorrectAnswer: str = Column(String(128), comment='正确答案', default='none')
    CandidateAnswer: str = Column(String(128), comment='考生答案', default='none')
    ScoreRatio: float = Column(DECIMAL(10, 2), comment='得分比例', default=0.00)
    Position: int = Column(INTEGER, comment='拖拽题/连线题 展示位置 1左 2右', default=0)
    UpdateTime: int = Column(INTEGER, comment='更新时间', default=int(time()))

    def __init__(self):
        super().__init__()