from Entity.BaseEntity import *


# 科目
class SubjectEntity(BaseEntity):
    __tablename__ = 'Subject'

    SubjectName = Column(String(128), comment='科目名称')
    SubjectCode = Column(String(128), index=True, comment='科目编码')
    SubjectState = Column(INTEGER, comment='科目状态 1正常 2禁用')
    UpdateTime = Column(INTEGER, comment='更新时间')