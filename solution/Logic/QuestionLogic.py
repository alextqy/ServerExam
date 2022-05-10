from Logic.BaseLogic import *


class QuestionLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewQuestion(self, ClientHost: str, Token: str, QuestionTitle: str, QuestionType: int, KnowledgeID: int, Description: str):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif QuestionTitle == '':
            result.Memo = 'wrong question title'
        elif QuestionType <= 0:
            result.Memo = 'wrong question type'
        elif KnowledgeID <= 0:
            result.Memo = 'wrong knowledge id'
        else:
            KnowledgeData: KnowledgeEntity = self._knowledgeModel.Find(_dbsession, KnowledgeID)
            if KnowledgeData is None:
                result.Memo = 'knowledge data error'
            elif KnowledgeData.KnowledgeState != 1:
                result.Memo = 'knowledge data error'
            else:
                Desc = 'new question:' + QuestionTitle
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result
                QuestionData: QuestionEntity = QuestionEntity()
                QuestionData.QuestionTitle = QuestionTitle
                QuestionData.QuestionType = QuestionType
                QuestionData.KnowledgeID = KnowledgeID
                QuestionData.Description = Description
                result: Result = self._questionModel.Insert(_dbsession, QuestionData)
        return result