from Entity.BaseEntity import *


# 答题卡选项
class ScantronSolutionEntity(BaseEntity, BaseORM):
    __tablename__ = 'ScantronSolution'

    ScantronID: int = Column(INTEGER, comment='试题ID', default=0)
    Option: str = Column(String(128), comment='试题选项', default='none')
    OptionAttachment: str = Column(String(65535), comment='试题附件', default='none')
    CorrectAnswer: int = Column(INTEGER, comment='正确答案 1错误 2正确', default=0)
    CorrectItem: str = Column(String(65535), comment='答案项', default='none')
    ScoreRatio: float = Column(DECIMAL(10, 2), comment='得分比例', default=0.00)
    Position: int = Column(INTEGER, comment='拖拽题/连线题 展示位置 1左 2右', default=0)
    UpdateTime: int = Column(INTEGER, comment='更新时间', default=int(time()))
    CandidateAnswer: str = Column(String(128), comment='考生答案', default='')

    def __init__(self):
        super().__init__()