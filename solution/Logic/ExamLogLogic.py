from Logic.BaseLogic import *


class ExamLogLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def ExamLogList(self, Token: str, Page: int, PageSize: int, Stext: str, Type: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        else:
            result: ResultList = self._examLogModel.List(_dbsession, Page, PageSize, Stext, Type)
        return result

    def ExamLogInfo(self, Token: str, ID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif ID <= 0:
            result.Memo = 'wrong ID'
        else:
            ExamLogData: ExamLogEntity = self._examLogModel.Find(_dbsession, ID)
            if ExamLogData is None:
                result.Memo = 'exam log data error'
            else:
                result.State = True
                result.Data = ExamLogData
        return result