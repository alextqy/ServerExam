from Logic.BaseLogic import *


class ExamineeTokenLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def SignInStudentID(self, Account: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        if Account == '':
            result.Memo = self._lang.WrongAccount
        else:
            ExamineeData: ExamineeEntity = self._examineeModel.FindExamineeNo(_dbsession, Account)
            if ExamineeData is not None:
                result.Memo = self._lang.ExamineeDataDoesNotExist
            else:
                pass
        return result

    def SignInAdmissionTicket(self, Account: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        if Account == '':
            result.Memo = self._lang.WrongAccount
        else:
            ExamInfoData: ExamInfoEntity = self._examInfoModel.FindExamNo(_dbsession, Account)
            if ExamInfoData is not None:
                result.Memo = self._lang.ExamDataDoesNotExist
            else:
                pass
        return result