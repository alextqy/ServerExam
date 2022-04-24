from Entity.BaseEntity import BaseEntity


# 报名
class ExamInfoEntity(BaseEntity):
    SubjectName = ''  # 科目名称
    ExamNo = ''  # 准考证号
    TotalScore = 0.00  # 总分
    PassLine = 0.00  # 及格分数
    ActualScore = 0.00  # 真实得分
    ExamDuration = 0  # 额定考试时长
    StartTime = 0  # 实际考试开始时间
    EndTime = 0  # 实际考试结束时间
    ActualDuration = 0  # 实际考试时长
    Pass = 0  # 是否通过 1否 2是
    UpdateTime = 0  # 更新时间
    ExamineeID = 0  # 考生ID
