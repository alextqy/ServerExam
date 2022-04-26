from Entity.BaseEntity import *


# 知识点
class KnowledgeEntity(BaseEntity, BaseORM):
    __tablename__ = 'Knowledge'

    KnowledgeName = Column(String(128), comment='知识点名称')
    KnowledgeCode = Column(String(128), index=True, comment='知识点编码')
    SubjectID = Column(INTEGER, index=True, comment='科目ID')
    SubjectState = Column(INTEGER, comment='知识点状态 1正常 2禁用')
    UpdateTime = Column(INTEGER, comment='更新时间')

    def __init__(self):
        super().__init__()