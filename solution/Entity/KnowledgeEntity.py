from Entity.BaseEntity import *


# 知识点
class KnowledgeEntity(BaseEntity, BaseORM):
    __tablename__ = 'Knowledge'

    KnowledgeName: str = Column(String(128), comment='知识点名称')
    KnowledgeCode: str = Column(String(128), index=True, comment='知识点编码')
    SubjectID: int = Column(INTEGER(10), index=True, comment='科目ID')
    SubjectState: int = Column(INTEGER(1), comment='知识点状态 1正常 2禁用')
    UpdateTime: int = Column(INTEGER(10), comment='更新时间', default=int(time()))

    def __init__(self):
        super().__init__()