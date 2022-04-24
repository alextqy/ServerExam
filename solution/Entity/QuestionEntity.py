from Entity.BaseEntity import BaseEntity


# 试题
class QuestionEntity(BaseEntity):
    QuestionTitle = ''  # 题目
    QuestionCode = ''  # 试题编码
    QuestionType = 0  # 试题类型 1单选 2判断 3多选 4填空 5问答
    QuestionState = 0  # 试题状态 1正常 2禁用
    Marking = 0  # 人工阅卷 1否 2是
    KnowledgeID = 0  # 知识点ID
    Describe = ''  # 试题描述
    Attachment = ''  # 试题附件
    UpdateTime = 0  # 更新时间