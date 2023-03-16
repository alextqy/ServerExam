# -*- coding:utf-8 -*-
from Logic.BaseLogic import *


class HeadlineLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewHeadline(self, ClientHost: str, Token: str, Content: str):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif Content == '':
            result.Memo = self._lang.WrongContent
        elif self._headlineModel.FindContentCode(_dbsession, Content) is not None:
            result.Memo = self._lang.HeadlineDataAlreadyExists
        else:
            _dbsession.begin_nested()

            HeadlineData = HeadlineEntity()
            HeadlineData.Content = Content
            AddInfo: Result = self._headlineModel.Insert(_dbsession, HeadlineData)
            if AddInfo.State == False:
                result.Memo = AddInfo.Memo
                _dbsession.rollback()
                return result

            Desc = 'new headline:' + Content
            if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                result.Memo = self._lang.LoggingFailed
                _dbsession.rollback()
                return result

            _dbsession.commit()
            result.State = True
        _dbsession.close()
        return result

    def UpdateHeadlineInfo(self, ClientHost: str, Token: str, ID: int, Content: str):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif ID <= 0:
            result.Memo = self._lang.WrongID
        elif Content == '':
            result.Memo = self._lang.WrongContent
        else:
            HeadlineData: HeadlineEntity = self._headlineModel.Find(_dbsession, ID)
            if HeadlineData is None:
                result.Memo = self._lang.HeadlineDataError
            elif HeadlineData.Content == Content:
                result.State = True
                return result
            elif self._headlineModel.FindContentCode(_dbsession, Content) is not None:
                result.Memo = self._lang.HeadlineDataAlreadyExists
            else:
                if HeadlineData.Content != Content:
                    HeadlineData.ContentCode = self._common.StrMD5(Content)

                _dbsession.begin_nested()

                try:
                    HeadlineData.Content = Content
                    HeadlineData.UpdateTime = self._common.Time()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                Desc = 'update headline ID:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    _dbsession.rollback()
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result

    def HeadlineList(self, Token: str, Page: int, PageSize: int, Stext: str):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: ResultList = self._headlineModel.List(_dbsession, Page, PageSize, Stext)
        _dbsession.close()
        return result

    def HeadlineInfo(self, Token: str, ID: int):
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
            HeadlineData: HeadlineEntity = self._headlineModel.Find(_dbsession, ID)
            if HeadlineData is None:
                result.Memo = self._lang.HeadlineDataError
            else:
                result.State = True
                result.Data = HeadlineData
        _dbsession.close()
        return result

    def Headlines(self, Token: str):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: Result = self._headlineModel.Headlines(_dbsession)
        _dbsession.close()
        return result