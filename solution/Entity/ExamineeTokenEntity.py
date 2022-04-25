from Entity.BaseEntity import *


# 考生Token
class ExamineeTokenEntity(BaseEntity):
    __tablename__ = 'ExamineeToken'

    Token = Column(String(128), index=True, comment='Token')
    ExamID = Column(INTEGER, index=True, comment='报名ID')