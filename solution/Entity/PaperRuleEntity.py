from Entity.BaseEntity import *


# 试卷规则
class PaperRuleEntity(BaseEntity, BaseORM):
    __tablename__ = 'PaperRule'

    HeadlineID = Column(INTEGER, comment='大标题ID')
    QuestionType = Column(INTEGER, comment='试题类型 1单选 2判断 3多选 4填空 5问答')
    QuestionNum = Column(INTEGER, comment='抽题数量')
    SingleScore = Column(DECIMAL(10, 2), comment='单题分数')
    PaperID = Column(INTEGER, comment='试卷ID')
    PaperRuleState = Column(INTEGER, comment='试卷规则状态 1正常 2禁用')
    UpdateTime = Column(INTEGER, comment='更新时间')

    def __init__(self):
        super().__init__()