from Entity.BaseEntity import BaseEntity


# 考生日志
class ExamLogEntity(BaseEntity):
    Type = 0  # 日志类型 1操作 2登录
    ExamNo = ''  # 准考证号
    Describe = ''  # 描述信息
    IP = ''  # IP地址
