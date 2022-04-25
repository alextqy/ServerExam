from Entity.BaseEntity import *


# 试题
class QuestionEntity(BaseEntity):
    __tablename__ = 'Question'

    QuestionTitle = Column(String(65535), comment='题目')
    QuestionCode = Column(String(128), index=True, comment='试题编码')
    QuestionType = Column(INTEGER, comment='试题类型 1单选 2判断 3多选 4填空 5问答')
    QuestionState = Column(INTEGER, comment='试题状态 1正常 2禁用')
    Marking = Column(INTEGER, comment='人工阅卷 1否 2是')
    KnowledgeID = Column(INTEGER, comment='知识点ID')
    Describe = Column(String(65535), comment='试题描述')
    Attachment = Column(String(65535), comment='试题附件')
    UpdateTime = Column(INTEGER, comment='更新时间')