from Logic.BaseLogic import *


class PracticeLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def SignInPractice(self, ExamineeNo: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        if ExamineeNo == '':
            result.Memo = self._lang.WrongAccount
        else:
            # 获取考生数据
            ExamineeData: ExamineeEntity = self._examineeModel.FindExamineeNo(_dbsession, ExamineeNo)
            if ExamineeData is None:
                result.Memo = self._lang.ExamineeDataError
            else:
                _dbsession.begin_nested()

                # 生成Token数据
                ExamineeTokenData = ExamineeTokenEntity()
                ExamineeTokenData.ExamID = 0
                ExamineeTokenData.Token = self._common.GenerateToken()
                AddInfo: Result = self._examineeTokenModel.Insert(_dbsession, ExamineeTokenData)
                if AddInfo.State == False:
                    result.Memo = AddInfo.Memo
                    return result

                _dbsession.commit()

                result.State = True
                result.Data = ExamineeTokenData.Token
        return result

    def NewPractice(self, Token: str, QuestionType: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        ExamineeTokenID: int = self.PracticeValidation(_dbsession, Token)
        if ExamineeTokenID == 0:
            result.Memo = self._lang.WrongToken
        elif QuestionType <= 0:
            result.Memo = self._lang.WrongQuestionType
        else:
            # 获取所有当前类型的试题
            QuestionDataList: list = self._questionModel.FindQuestionType(_dbsession, QuestionType)
            if len(QuestionDataList) == 0:
                result.Memo = self._lang.NoData
                return result

            # 获取该考生现在已经做过的试题
            DoneTestQuestionDataList: list = self._practiceModel.FindExamineeTokenID(_dbsession, ExamineeTokenID)

            if len(QuestionDataList) == len(DoneTestQuestionDataList):
                result.Memo = self._lang.AllTestsCompleted
                return result

            # 去掉已经使用过的试题
            if len(DoneTestQuestionDataList) > 0:
                for i in QuestionDataList[:]:
                    QuestionData: QuestionEntity = i
                    for j in DoneTestQuestionDataList[:]:
                        PracticeData: PracticeEntity = j
                        if PracticeData.QuestionCode == QuestionData.QuestionCode:
                            QuestionDataList.remove(QuestionData)

            # 随机抽取一道题
            ChoiceData: QuestionEntity = self._common.RandomDrawChoice(QuestionDataList)

            _dbsession.begin_nested()

            # 写入刷题数据
            PracticeData = PracticeEntity()
            PracticeData.QuestionTitle = ChoiceData.QuestionTitle
            PracticeData.QuestionCode = ChoiceData.QuestionCode
            PracticeData.QuestionType = ChoiceData.QuestionType
            PracticeData.Marking = ChoiceData.Marking
            PracticeData.KnowledgeID = ChoiceData.KnowledgeID
            PracticeData.Description = ChoiceData.Description
            PracticeData.Attachment = ChoiceData.Attachment
            PracticeData.ExamineeTokenID = ExamineeTokenID
            AddInfo: Result = self._practiceModel.Insert(_dbsession, PracticeData)
            if AddInfo.State == False:
                result.Memo = AddInfo.Memo
                return result

            # 写入刷题选项数据
            QuestionSolutionDataList: list = self._questionSolutionModel.FindQuestionID(_dbsession, ChoiceData.ID)
            if len(QuestionSolutionDataList) == 0:
                result.Memo = self._lang.WrongData
                return result
            for k in QuestionSolutionDataList:
                QuestionSolutionData: QuestionSolutionEntity = k
                PracticeSolutionData = PracticeSolutionEntity()
                PracticeSolutionData.PracticeID = PracticeData.ID
                PracticeSolutionData.Option = QuestionSolutionData.Option
                PracticeSolutionData.OptionAttachment = QuestionSolutionData.OptionAttachment
                PracticeSolutionData.CorrectAnswer = QuestionSolutionData.CorrectAnswer
                PracticeSolutionData.CorrectItem = QuestionSolutionData.CorrectItem
                PracticeSolutionData.ScoreRatio = QuestionSolutionData.ScoreRatio
                PracticeSolutionData.Position = QuestionSolutionData.Position
                AddInfo: Result = self._practiceSolutionModel.Insert(_dbsession, PracticeSolutionData)
                if AddInfo.State == False:
                    result.Memo = AddInfo.Memo
                    return result

            _dbsession.commit()

            result.State = True
            result.Data = PracticeData.ID
        return result

    def PracticeInfo(self, Token: str, ID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        ExamineeTokenID: int = self.PracticeValidation(_dbsession, Token)
        if ExamineeTokenID == 0:
            result.Memo = self._lang.WrongToken
        elif ID <= 0:
            result.Memo = self._lang.WrongData
        else:
            PracticeData: PracticeEntity = self._practiceModel.Find(_dbsession, ID)
            if PracticeData is None:
                result.Memo = self._lang.WrongData
                return result
            PracticeSolutionDataList: list = self._practiceSolutionModel.FindPracticeID(_dbsession, PracticeData.ID)
            if len(PracticeSolutionDataList) == 0:
                result.Memo = self._lang.WrongData
                return result
            PracticeData.SolutionList = PracticeSolutionDataList

            result.Data = PracticeData
        return result
