from Entity.BaseEntity import *


# 试卷规则
class PaperRuleEntity(BaseEntity, BaseORM):
    __tablename__ = 'PaperRule'

    HeadlineID: int = Column(INTEGER, comment='大标题ID', default=0)
    QuestionType: int = Column(INTEGER, comment='试题类型 1单选 2判断 3多选 4填空 5问答', default=0)
    QuestionNum: int = Column(INTEGER, comment='抽题数量', default=0)
    SingleScore: float = Column(DECIMAL(10, 2), comment='单题分数', default=0.00)
    PaperID: int = Column(INTEGER, comment='试卷ID', default=0)
    PaperRuleState: int = Column(INTEGER, comment='试卷规则状态 1正常 2禁用', default=0)
    UpdateTime: int = Column(INTEGER, comment='更新时间', default=int(time()))

    def __init__(self):
        super().__init__()