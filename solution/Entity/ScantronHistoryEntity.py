from Entity.BaseEntity import *


# 历史答题卡
class ScantronHistoryEntity(BaseEntity, BaseORM):
    __tablename__ = 'ScantronHistory'

    QuestionTitle = Column(String(65535), comment='标题')
    QuestionCode = Column(String(128), comment='试题编码')
    QuestionType = Column(INTEGER, comment='试题类型 1单选 2判断 3多选 4填空 5问答')
    Marking = Column(INTEGER, comment='人工阅卷 1否 2是')
    KnowledgeID = Column(INTEGER, comment='知识点ID')
    Describe = Column(String(65535), comment='试题描述')
    Attachment = Column(String(65535), comment='试题附件')
    UpdateTime = Column(INTEGER, comment='更新时间', default=int(time()))
    Score = Column(DECIMAL(10, 2), comment='额定分数')
    ExamID = Column(INTEGER, comment='报名ID')
    HeadlineContent = Column(String(65535), comment='大标题内容')

    def __init__(self):
        super().__init__()