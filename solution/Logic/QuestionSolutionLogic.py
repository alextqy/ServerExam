from Logic.BaseLogic import *


class QuestionSolutionLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewQuestionSolution(self, ClientHost: str, Token: str, QuestionID: int, Option: str, CorrectAnswer: int, CorrectItem: str, ScoreRatio: float, Position: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif QuestionID <= 0:
            result.Memo = 'wrong question id'
        # elif Option == '':
        #     result.Memo = 'wrong option'
        elif CorrectAnswer <= 0:
            result.Memo = 'wrong correct answer'
        # elif CorrectItem == '':
        #     result.Memo = 'wrong correct item'
        elif ScoreRatio <= 0:
            result.Memo = 'wrong score ratio'
        elif Position <= 0:
            result.Memo = 'wrong position'
        else:
            QuestionData: QuestionEntity = self._questionModel.Find(QuestionID)
            if QuestionData is None:
                result.Memo = 'question data error'
            else:
                if QuestionData.QuestionType == 1:
                    pass
                if QuestionData.QuestionType == 2:
                    pass
                if QuestionData.QuestionType == 3:
                    pass
                if QuestionData.QuestionType == 4:
                    pass
                if QuestionData.QuestionType == 5:
                    pass
                if QuestionData.QuestionType == 6:
                    pass
                if QuestionData.QuestionType == 7:
                    pass
                if QuestionData.QuestionType == 8:
                    pass

                # _dbsession.begin_nested()

                # QuestionData = QuestionSolutionEntity()
                # QuestionData.QuestionID = QuestionID
                # QuestionData.Option = Option
                # QuestionData.CorrectAnswer = CorrectAnswer
                # QuestionData.ScoreRatio = ScoreRatio
                # QuestionData.Position = Position
                # AddInfo: Result = self._questionSolutionModel.Insert(_dbsession, QuestionData)
                # if AddInfo.State == False:
                #     result.Memo = AddInfo.Memo
                #     return result

                # Desc = 'new question solution:' + Option
                # if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                #     result.Memo = 'logging failed'
                #     return result

                # _dbsession.commit()
                # result.State = True
        return result