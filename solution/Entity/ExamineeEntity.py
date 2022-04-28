from Entity.BaseEntity import *


# 考生
class ExamineeEntity(BaseEntity, BaseORM):
    __tablename__ = 'Examinee'

    Name: str = Column(String(128), comment='考生姓名')
    ExamineeNo: str = Column(String(128), index=True, comment='考生编号')
    Contact: str = Column(String(128), comment='联系方式')

    def __init__(self):
        super().__init__()