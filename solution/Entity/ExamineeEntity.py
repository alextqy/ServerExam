from Entity.BaseEntity import *


# 考生
class ExamineeEntity(BaseEntity, BaseORM):
    __tablename__ = 'Examinee'

    Name = Column(String(128), comment='考生姓名')
    ExamineeNo = Column(String(128), index=True, comment='考生编号')
    Contact = Column(String(128), comment='联系方式')

    def __init__(self):
        super().__init__()