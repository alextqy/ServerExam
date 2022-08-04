# -*- coding:utf-8 -*-
from Logic.BaseLogic import *


class SysConfLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def ConfigInfo(self, Token: str, Key: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif Key == '':
            result.Memo = self._lang.WrongData
        else:
            result.Data = self._sysConfModel.FindKey(_dbsession, Key)
            result.State = True
        _dbsession.close()
        return result