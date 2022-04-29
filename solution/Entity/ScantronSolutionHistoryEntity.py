from Entity.BaseEntity import *


class ScantronSolutionHistoryEntity(BaseEntity, BaseORM):
    __tablename__ = 'ScantronSolutionHistory'

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