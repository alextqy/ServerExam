from Entity.BaseEntity import BaseEntity


class ScantronSolutionEntity(BaseEntity):
    ScantronID = 0  # 试题ID
    Option = ''  # 试题选项
    OptionAttachment = ''  # 试题附件
    CorrectAnswer = ''  # 正确答案
    CandidateAnswer = ''  # 考生答案
    ScoreRatio = 0.00  # 得分比例
    UpdateTime = 0  # 更新时间