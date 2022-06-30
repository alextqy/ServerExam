# -*- coding:utf-8 -*-
from Entity.BaseEntity import *


# 试题
class QuestionEntity(BaseEntity, BaseORM):
    __tablename__ = 'Question'

    QuestionTitle: str = Column(String(65535), comment='题目', default='none')
    QuestionCode: str = Column(String(128), index=True, comment='试题代码', default='none')
    QuestionType: int = Column(INTEGER, comment='试题类型 1单选 2判断 3多选 4填空 5问答 6代码实训 7拖拽 8连线', default=0)
    QuestionState: int = Column(INTEGER, comment='试题状态 1正常 2禁用', default=0)
    Marking: int = Column(INTEGER, comment='人工阅卷 1否 2是', default=0)
    KnowledgeID: int = Column(INTEGER, comment='知识点ID', default=0)
    Description: str = Column(String(65535), comment='试题描述', default='none')
    Attachment: str = Column(String(65535), comment='试题附件', default='none')
    Language: str = Column(String(128), comment='计算机语言', default='none')
    LanguageVersion: str = Column(String(128), comment='计算机语言版本', default='none')
    UpdateTime: int = Column(INTEGER, comment='更新时间', default=int(time()))

    def __init__(self):
        super().__init__()