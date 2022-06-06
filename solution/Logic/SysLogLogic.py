from Logic.BaseLogic import *


class SysLogLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def SysLogList(self, Token: str, Page: int, PageSize: int, Stext: str, Type: int, ManagerID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        else:
            result: ResultList = self._sysLogModel.List(_dbsession, Page, PageSize, Stext, Type, ManagerID)
        return result

    def SysLogInfo(self, Token: str, ID: int) -> Result:
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
            SysLogData: SysLogEntity = self._sysLogModel.Find(_dbsession, ID)
            if SysLogData is None:
                result.Memo = 'sys log data error'
            else:
                result.State = True
                result.Data = SysLogData
        return result