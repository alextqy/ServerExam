from Entity.BaseEntity import *


# 考生Token
class ExamineeTokenEntity(BaseEntity, BaseORM):
    __tablename__ = 'ExamineeToken'

    Token: str = Column(String(128), index=True, comment='Token', default='none')
    ExamID: int = Column(INTEGER, index=True, comment='报名ID', default=0)

    def __init__(self):
        super().__init__()