from Entity.BaseEntity import *


# 考生日志
class ExamLogEntity(BaseEntity, BaseORM):
    __tablename__ = 'ExamLog'

    Type: int = Column(INTEGER, comment='日志类型 1操作 2登录', default=0)
    ExamNo: str = Column(String(128), comment='准考证号', default='none')
    Description: str = Column(String(65535), comment='描述信息', default='none')
    IP: str = Column(String(128), comment='IP地址', default='none')

    def __init__(self):
        super().__init__()