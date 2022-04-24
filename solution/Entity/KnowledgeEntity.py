from Entity.BaseEntity import *


# 知识点
class KnowledgeEntity(BaseEntity):
    __tablename__ = 'Knowledge'

    KnowledgeName = Column(String(128), comment='知识点名称')
    SubjectID = Column(INTEGER, comment='科目ID')
    SubjectState = Column(INTEGER, comment='知识点状态 1正常 2禁用')
    UpdateTime = Column(INTEGER, comment='更新时间')