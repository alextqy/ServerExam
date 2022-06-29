# -*- coding:utf-8 -*-
from Entity.BaseEntity import *


# 答题卡
class ScantronEntity(BaseEntity, BaseORM):
    __tablename__ = 'Scantron'

    QuestionTitle: str = Column(String(65535), comment='标题', default='none')
    QuestionCode: str = Column(String(128), comment='试题编码', default='none')
    QuestionType: int = Column(INTEGER, comment='试题类型 1单选 2判断 3多选 4填空 5问答 6代码实训 7拖拽题 8连线题', default=0)
    Marking: int = Column(INTEGER, comment='人工阅卷 1否 2是', default=0)
    KnowledgeID: int = Column(INTEGER, comment='知识点ID', default=0)
    Description: str = Column(String(65535), comment='试题描述', default='none')
    Attachment: str = Column(String(65535), comment='试题附件', default='none')
    UpdateTime: int = Column(INTEGER, comment='更新时间', default=int(time()))
    Score: float = Column(DECIMAL(10, 2), comment='额定分数', default=0.00)
    ExamID: int = Column(INTEGER, comment='报名ID', default=0)
    HeadlineContent: str = Column(String(65535), comment='大标题内容', default='none')

    def __init__(self):
        super().__init__()