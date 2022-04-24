from Entity.BaseEntity import BaseEntity


# 试卷规则
class PaperRuleEntity(BaseEntity):
    HeadlineID = 0  # 大标题ID
    QuestionType = 0  # 试题类型 1单选 2判断 3多选 4填空 5问答
    QuestionNum = 0  # 抽题数量
    SingleScore = 0.00  # 单题分数
    PaperID = 0  # 试卷ID
    PaperRuleState = 0  # 试卷规则状态 1正常 2禁用
    UpdateTime = 0  # 更新时间
