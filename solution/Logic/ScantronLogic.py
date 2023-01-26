# -*- coding:utf-8 -*-
from Logic.BaseLogic import *


class ScantronLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def ScantronList(self, Token: str, Page: int, PageSize: int, ExamID: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: ResultList = self._scantronModel.List(_dbsession, Page, PageSize, ExamID)
        _dbsession.close()
        return result

    def ScantronInfo(self, Token: str, ID: int):
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
            ExamInfoData: ExamInfoEntity = self._scantronModel.Find(_dbsession, ID)
            if ExamInfoData is None:
                result.Memo = self._lang.ScantronDataError
            else:
                result.State = True
                result.Data = ExamInfoData
        _dbsession.close()
        return result