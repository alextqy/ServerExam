# -*- coding:utf-8 -*-
from Logic.BaseLogic import *


class SysLogLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def SysLogList(self, Token: str, Page: int, PageSize: int, Stext: str, Type: int, ManagerID: int) -> ResultList:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: ResultList = self._sysLogModel.List(_dbsession, Page, PageSize, Stext, Type, ManagerID)
        return result

    def SysLogInfo(self, Token: str, ID: int) -> Result:
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
            SysLogData: SysLogEntity = self._sysLogModel.Find(_dbsession, ID)
            if SysLogData is None:
                result.Memo = self._lang.SysLogDataError
            else:
                result.State = True
                result.Data = SysLogData
        return result