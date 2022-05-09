from Logic.BaseLogic import *


class HeadlineLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewHeadline(self, ClientHost: str, Token: str, Content: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif Content == '':
            result.Memo = 'wrong content'
        elif self._headlineModel.FindContentCode(_dbsession, Content) is not None:
            result.Memo = 'data already exists'
        else:
            Desc = 'new headline:' + Content
            if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                result.Memo = 'logging failed'
                return result
            HeadlineData = HeadlineEntity()
            HeadlineData.Content = Content
            result: Result = self._headlineModel.Insert(_dbsession, HeadlineData)
        return result

    def UpdateHeadlineInfo(self, ClientHost: str, Token: str, ID: int, Content: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif ID <= 0:
            result.Memo = 'wrong id'
        elif Content == '':
            result.Memo = 'wrong content'
        else:
            HeadlineData: HeadlineEntity = self._headlineModel.Find(_dbsession, ID)
            if HeadlineData is None:
                result.Memo = 'data error'
            elif HeadlineData.Content == Content:
                result.Status = True
                return result
            elif self._headlineModel.FindContentCode(_dbsession, Content) is not None:
                result.Memo = 'data already exists'
            else:
                Desc = 'update headline id:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result
                try:
                    HeadlineData.Content = Content
                    HeadlineData.UpdateTime = self._common.Time()
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result
                result.Status = True
        return result

    def HeadlineList(self, Token: str, Page: int, PageSize: int, Stext: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        else:
            result: ResultList = self._headlineModel.List(_dbsession, Page, PageSize, Stext)
        return result

    def HeadlineInfo(self, Token: str, ID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif ID <= 0:
            result.Memo = 'wrong id'
        else:
            HeadlineData: HeadlineEntity = self._headlineModel.Find(_dbsession, ID)
            if HeadlineData is None:
                result.Memo = 'data error'
            else:
                result.Status = True
                result.Data = HeadlineData
        return result