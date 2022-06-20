from Logic.BaseLogic import *


class ExamineeTokenLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    # 获取当前考生的报名列表
    def SignInStudentID(self, Account: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        if Account == '':
            result.Memo = self._lang.WrongAccount
        else:
            ExamineeData: ExamineeEntity = self._examineeModel.FindExamineeNo(_dbsession, Account)
            if ExamineeData is None:
                result.Memo = self._lang.ExamineeDataDoesNotExist
            else:
                ExamInfoList: list = self._examInfoModel.FindExamineeID(_dbsession, ExamineeData.ID)
                result.Data = ExamInfoList
                result.State = True
        return result

    def SignInAdmissionTicket(self, ClientHost: str, ExamNo: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        if ExamNo == '':
            result.Memo = self._lang.WrongExamNo
        else:
            ExamInfoData: ExamInfoEntity = self._examInfoModel.FindExamNo(_dbsession, ExamNo)
            if ExamInfoData is None:
                result.Memo = self._lang.ExamDataDoesNotExist
            elif self._common.Time() >= ExamInfoData.EndTime:
                result.Memo = self._lang.TimeOut
            else:
                result = self.PostLoginOperationAction(ClientHost, ExamInfoData.ID)
        return result

    def PostLoginOperationAction(self, ClientHost: str, ExamInfoID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        if ExamInfoID <= 0:
            result.Memo = self._lang.RegistrationDataError
        else:
            _dbsession.begin_nested()

            # 获取报名数据
            ExamInfoData: ExamInfoEntity = self._examInfoModel.Find(_dbsession, ExamInfoID)
            if ExamInfoData is None:
                result.Memo = self._lang.ExamDataDoesNotExist
            elif ExamInfoData.ExamState != 2:
                result.Memo = self._lang.RegistrationDataError
            elif ExamInfoData.StartTime > 0 and self._common.Time() >= ExamInfoData.EndTime:
                result.Memo = self._lang.TimeOut
            else:
                # 删除相同报名Token
                CheckToken: ExamineeTokenEntity = self._examineeTokenModel.FindExamID(_dbsession, ExamInfoData.ID)
                if CheckToken is not None:
                    DelInfo: Result = self._examineeTokenModel.Delete(_dbsession, CheckToken.ID)
                    if DelInfo.State == False:
                        return result

                SignInTime: str = self._common.Time()

                # 生成考生Token
                ExamineeTokenData = ExamineeTokenEntity()
                ExamineeTokenData.CreateTime = SignInTime
                ExamineeTokenData.ExamID = ExamInfoData.ID
                ExamineeTokenData.Token = self._common.StrMD5(ExamInfoData.ExamNo + str(SignInTime))
                AddInfo: Result = self._examineeTokenModel.Insert(_dbsession, ExamineeTokenData)
                if AddInfo.State == False:
                    result.Memo = AddInfo.Memo
                    return result

                # 修改报名考试起止时间
                ExamInfoData.StartTime = SignInTime
                ExamInfoData.EndTime = SignInTime + ExamInfoData.ExamDuration

                # 记录日志
                Desc = 'examinee login exam No.:' + ExamInfoData.ExamNo
                if self.LogExamAction(_dbsession, 2, ExamInfoData.ExamNo, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.Data = ExamineeTokenData.Token
                result.State = True
        return result

    def ExamScantronList(self, Token: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        ExamID: int = self.ExamineeTokenValidation(_dbsession, Token)
        if ExamID == 0:
            result.Memo = self._lang.WrongToken
        else:
            ScantronData: list = self._scantronModel.AllInExamID(_dbsession, ExamID)
            result.State = True
            result.Data = ScantronData
        return result

    def ExamScantronSolutionInfo(self, Token: str, ID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        ExamID: int = self.ExamineeTokenValidation(_dbsession, Token)
        if ExamID == 0:
            result.Memo = self._lang.WrongToken
        else:
            ScantronData: ScantronEntity = self._scantronModel.Find(_dbsession, ID)
            if ScantronData is None:
                result.Memo = self._lang.WrongData
            elif ScantronData.QuestionType >= 4 and ScantronData.QuestionType <= 6:
                result.State = True
                return result
            else:
                ScantronSolutionList: list = self._scantronSolutionModel.AllInScantronID(_dbsession, ScantronData.ID)
                if len(ScantronSolutionList) > 0:
                    for i in ScantronSolutionList:
                        ScantronSolutionData: ScantronSolutionEntity = i
                        ScantronSolutionData.CorrectAnswer = 0
                        ScantronSolutionData.CorrectItem = ''
                    ScantronData.ScantronSolutionList = ScantronSolutionList
                    result.Data = ScantronData
                result.State = True
        return result

    def ExamAnswer(self, Token: str, QuestionType: int, ID: int, Answer: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        ExamID: int = self.ExamineeTokenValidation(_dbsession, Token)
        if ExamID == 0:
            result.Memo = self._lang.WrongToken
        else:
            if QuestionType <= 0:
                result.State = True
            elif ID <= 0:
                result.State = True
            elif Answer == '':
                result.State = True
            else:
                ScantronSolutionData: ScantronSolutionEntity = self._scantronSolutionModel.Find(_dbsession, ID)
                if ScantronSolutionData is None:
                    result.Memo = self._lang.WrongData
                else:
                    if QuestionType >= 1 and QuestionType <= 3:
                        pass
                    if QuestionType >= 4 and QuestionType <= 6:
                        pass
                    if QuestionType >= 7 and QuestionType <= 8:
                        pass
        return result