from Entity.BaseEntity import *


# 试卷规则
class PaperRuleEntity(BaseEntity, BaseORM):
    __tablename__ = 'PaperRule'

    HeadlineID: int = Column(INTEGER(10), comment='大标题ID')
    QuestionType: int = Column(INTEGER(1), comment='试题类型 1单选 2判断 3多选 4填空 5问答')
    QuestionNum: int = Column(INTEGER(10), comment='抽题数量')
    SingleScore: float = Column(DECIMAL(10, 2), comment='单题分数')
    PaperID: int = Column(INTEGER(10), comment='试卷ID')
    PaperRuleState: int = Column(INTEGER(1), comment='试卷规则状态 1正常 2禁用')
    UpdateTime: int = Column(INTEGER(10), comment='更新时间', default=int(time()))

    def __init__(self):
        super().__init__()