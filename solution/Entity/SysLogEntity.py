from Entity.BaseEntity import *


# 系统日志
class SysLogEntity(BaseEntity):
    Type = 0  # 日志类型 1操作 2登录
    ManagerID = 0  # 管理员ID
    Describe = ''  # 描述信息
    IP = ''  # IP地址