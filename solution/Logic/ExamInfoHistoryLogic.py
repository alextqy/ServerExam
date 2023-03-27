# -*- coding:utf-8 -*-
from Logic.BaseLogic import *


class ExamInfoHistoryLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def ExamInfoHistoryList(self, Token: str, Page: int, PageSize: int, Stext: str, ExamState: int, ExamType: int, Pass: int, ExamineeID: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: ResultList = self._examInfoHistoryModel.List(_dbsession, Page, PageSize, Stext, ExamState, ExamType, Pass, ExamineeID)
        _dbsession.close()
        return result

    def ExamInfoHistory(self, Token: str, ID: int):
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
            ExamInfoData: ExamInfoEntity = self._examInfoHistoryModel.Find(_dbsession, ID)
            if ExamInfoData is None:
                result.Memo = self._lang.ExamDataError
            else:
                result.State = True
                result.Data = ExamInfoData
        _dbsession.close()
        return result