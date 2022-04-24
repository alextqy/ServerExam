from Entity.BaseEntity import *


# 答题卡
class ScantronEntity(BaseEntity):
    QuestionTitle = ''  # 标题
    QuestionCode = ''  # 试题编码
    QuestionType = 0  # 试题类型 1单选 2判断 3多选 4填空 5问答
    Marking = 0  # 人工阅卷 1否 2是
    KnowledgeID = 0  # 知识点ID
    Describe = ''  # 试题描述
    Attachment = ''  # 试题附件
    UpdateTime = 0  # 更新时间
    Score = 0.00  # 额定分数
    ExamID = 0  # 报名ID
    HeadlineContent = ''  # 大标题内容
