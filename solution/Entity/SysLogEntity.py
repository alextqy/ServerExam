from Entity.BaseEntity import *


# 系统日志
class SysLogEntity(BaseEntity):
    __tablename__ = 'SysLog'

    Type = Column(INTEGER, comment='日志类型 1操作 2登录')
    ManagerID = Column(INTEGER, comment='管理员ID')
    Describe = Column(String(65535), comment='描述信息')
    IP = Column(String(128), comment='IP地址')