from Entity.BaseEntity import *


# 试卷
class PaperEntity(BaseEntity):
    PaperName = ''  # 试卷名称
    SubjectID = 0  # 科目ID
    TotalScore = 0.00  # 总分
    PassLine = 0.00  # 及格分数
    ExamDuration = 0  # 考试时长
    PaperState = 0  # 试卷状态 1正常 2禁用
    UpdateTime = 0  # 更新时间