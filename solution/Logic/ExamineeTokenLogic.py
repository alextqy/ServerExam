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
            else:
                result = self.PostLoginOperation(ClientHost, ExamInfoData.ID)
        return result

    def PostLoginOperation(self, ClientHost: str, ExamInfoID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        if ExamInfoID <= 0:
            result.Memo = self._lang.RegistrationDataError
        else:
            # 获取报名数据
            ExamInfoData: ExamInfoEntity = self._examInfoModel.Find(_dbsession, ExamInfoID)
            if ExamInfoData is None:
                result.Memo = self._lang.ExamDataDoesNotExist
            elif ExamInfoData.ExamState != 2:
                result.Memo = self._lang.RegistrationDataError
            else:
                _dbsession.begin_nested()

                # 删除相同报名Token
                CheckToken: ExamineeTokenEntity = self._examineeTokenModel.FindExamID(_dbsession, ExamInfoData.ID)
                if CheckToken is not None:
                    DelInfo: Result = self._examineeTokenModel.Delete(_dbsession, CheckToken.ID)
                    if DelInfo.State == False:
                        return result

                # 生成考生Token
                ExamineeTokenData = ExamineeTokenEntity()
                ExamineeTokenData.CreateTime = self._common.Time()
                ExamineeTokenData.ExamID = ExamInfoData.ID
                ExamineeTokenData.Token = self._common.StrMD5(ExamInfoData.ExamNo + str(self._common.TimeMS()))
                AddInfo: Result = self._examineeTokenModel.Insert(_dbsession, ExamineeTokenData)
                if AddInfo.State == False:
                    result.Memo = AddInfo.Memo
                    return result

                # 记录日志
                Desc = 'examinee login exam No.:' + ExamInfoData.ExamNo
                if self.LogExamAction(_dbsession, 2, ExamInfoData.ExamNo, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.Data = ExamineeTokenData.Token
                result.State = True
        return result