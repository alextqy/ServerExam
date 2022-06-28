from Entity.BaseEntity import *


# 知识点
class KnowledgeEntity(BaseEntity, BaseORM):
    __tablename__ = 'Knowledge'

    KnowledgeName: str = Column(String(128), comment='知识点名称', default='none')
    KnowledgeCode: str = Column(String(128), index=True, comment='知识点编码', default='none')
    SubjectID: int = Column(INTEGER, index=True, comment='科目ID', default=0)
    KnowledgeState: int = Column(INTEGER, comment='知识点状态 1正常 2禁用', default=0)
    UpdateTime: int = Column(INTEGER, comment='更新时间', default=int(time()))

    def __init__(self):
        super().__init__()