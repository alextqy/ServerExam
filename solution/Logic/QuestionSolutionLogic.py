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
        # elif CorrectAnswer <= 0:
        #     result.Memo = 'wrong correct answer'
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
                if QuestionData.QuestionType == 1:  # 单选
                    if Option == '':
                        result.Memo = 'wrong option'
                        return result
                    if CorrectAnswer <= 0:
                        result.Memo = 'wrong correct answer'
                        return result
                    ScoreRatio = 1.00
                if QuestionData.QuestionType == 2:  # 判断
                    if Option == '':
                        result.Memo = 'wrong option'
                        return result
                    if CorrectAnswer <= 0:
                        result.Memo = 'wrong correct answer'
                        return result
                    ScoreRatio = 1.00
                    # 判断题只能有两个选项
                    QuestionSolutionList: ResultList = self._questionSolutionModel.List(QuestionData.ID)
                    if len(QuestionSolutionList.Data) > 2:
                        result.Memo = 'too many options'
                        return result
                if QuestionData.QuestionType == 3:  # 多选 必须全对才给分
                    if Option == '':
                        result.Memo = 'wrong option'
                        return result
                    if CorrectAnswer <= 0:
                        result.Memo = 'wrong correct answer'
                        return result
                    ScoreRatio = 1.00
                if QuestionData.QuestionType == 4:  # 填空
                    if CorrectItem == '':
                        result.Memo = 'wrong correct item'
                        return result
                    if ScoreRatio <= 0:
                        result.Memo = 'wrong score ratio'
                        return result
                    QuestionSolutionList: ResultList = self._questionSolutionModel.List(QuestionData.ID)
                    if len(QuestionSolutionList.Data) > 0:
                        SolutionDataList = QuestionSolutionList.Data
                        # 答案数量是否超过填空数
                        if len(SolutionDataList) >= self._common.CountStr(QuestionData.QuestionTitle, "<->"):
                            result.Memo = 'too many answers'
                            return result
                        CountScoreRatio = 0
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            CountScoreRatio += SolutionData.ScoreRatio
                        # 所有选项得分比例总和为1
                        if CountScoreRatio > 1:
                            result.Memo = 'wrong score ratio'
                            return result
                    CorrectAnswer = 1
                if QuestionData.QuestionType == 5:  # 问答
                    if CorrectItem == '':
                        result.Memo = 'wrong correct item'
                        return result
                    if ScoreRatio <= 0:
                        result.Memo = 'wrong score ratio'
                        return result
                    CountScoreRatio = 0
                    for i in SolutionDataList:
                        SolutionData: QuestionSolutionEntity = i
                        CountScoreRatio += SolutionData.ScoreRatio
                    # 所有选项得分比例总和为1
                    if CountScoreRatio > 1:
                        result.Memo = 'wrong score ratio'
                        return result
                    CorrectAnswer = 1
                if QuestionData.QuestionType == 6:  # 代码实训
                    if CorrectItem == '':
                        result.Memo = 'wrong correct item'
                        return result
                    ScoreRatio = 1.00
                if QuestionData.QuestionType == 7:  # 拖拽题
                    QuestionSolutionList: ResultList = self._questionSolutionModel.List(QuestionData.ID)
                    ScoreRatio = 1.00
                if QuestionData.QuestionType == 8:  # 连线题
                    QuestionSolutionList: ResultList = self._questionSolutionModel.List(QuestionData.ID)
                    ScoreRatio = 1.00

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