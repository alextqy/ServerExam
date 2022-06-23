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
                for i in QuestionDataList:
                    QuestionData: QuestionEntity = i
                    for j in DoneTestQuestionDataList:
                        PracticeData: PracticeEntity = j
                        if PracticeData.QuestionCode == QuestionData.QuestionCode:
                            QuestionDataList.remove(QuestionData)

            # 随机抽取一道题
            result.State = True
            result.Data = self._common.RandomDrawChoice(QuestionDataList)
        return result