from Entity.BaseEntity import *


# 知识点
class KnowledgeEntity(BaseEntity):
    KnowledgeName = ''  # 知识点名称
    SubjectID = 0  # 科目ID
    SubjectState = 0  # 知识点状态 1正常 2禁用
    UpdateTime = 0  # 更新时间