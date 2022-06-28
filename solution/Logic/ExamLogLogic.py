from Logic.BaseLogic import *


class ExamLogLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def ExamLogList(self, Token: str, Page: int, PageSize: int, Stext: str, Type: int) -> ResultList:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: ResultList = self._examLogModel.List(_dbsession, Page, PageSize, Stext, Type)
        return result

    def ExamLogInfo(self, Token: str, ID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif ID <= 0:
            result.Memo = self._lang.WrongID
        else:
            ExamLogData: ExamLogEntity = self._examLogModel.Find(_dbsession, ID)
            if ExamLogData is None:
                result.Memo = self._lang.ExamLogDataError
            else:
                result.State = True
                result.Data = ExamLogData
        return result