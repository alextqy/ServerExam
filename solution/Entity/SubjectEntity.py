from Entity.BaseEntity import *


# 科目
class SubjectEntity(BaseEntity):
    SubjectName = ''  # 科目名称
    SubjectCode = ''  # 科目编码
    SubjectState = 0  # 科目状态 1正常 2禁用
    UpdateTime = 0  # 更新时间