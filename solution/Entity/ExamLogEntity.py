from Entity.BaseEntity import *


# 考生日志
class ExamLogEntity(BaseEntity):
    __tablename__ = 'ExamLog'

    Type = Column(INTEGER, comment='日志类型 1操作 2登录')
    ExamNo = Column(String(128), comment='准考证号')
    Describe = Column(String(65535), comment='描述信息')
    IP = Column(String(128), comment='IP地址')
