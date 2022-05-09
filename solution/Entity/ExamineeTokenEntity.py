from Entity.BaseEntity import *


# 考生Token
class ExamineeTokenEntity(BaseEntity, BaseORM):
    __tablename__ = 'ExamineeToken'

    Token: str = Column(String(128), index=True, comment='Token')
    ExamID: int = Column(INTEGER, index=True, comment='报名ID')

    def __init__(self):
        super().__init__()