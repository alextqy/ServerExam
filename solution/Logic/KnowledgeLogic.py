from Logic.BaseLogic import *


class KnowledgeLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewKnowledge(self, ClientHost: str, Token: str, KnowledgeName: str, SubjectID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif KnowledgeName == '':
            result.Memo = 'wrong knowledge name'
        elif SubjectID <= 0:
            result.Memo = 'wrong subject id'
        elif self._knowledgeModel.FindKnowledgeCode(_dbsession, KnowledgeName) is not None:
            result.Memo = 'data already exists'
        else:
            SubjectData: SubjectEntity = self._subjectModel.Find(_dbsession, SubjectID)
            if SubjectData is None:
                result.Memo = 'subject data error'
            elif SubjectData.SubjectState != 1:
                result.Memo = 'subject data error'
            else:
                Desc = 'new knowledge:' + KnowledgeName
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result
                KnowledgeData = KnowledgeEntity()
                KnowledgeData.KnowledgeName = KnowledgeName
                KnowledgeData.SubjectID = SubjectID
                result: Result = self._knowledgeModel.Insert(_dbsession, KnowledgeData)
        return result

    def KnowledgeDisabled(self, ClientHost: str, Token: str, ID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        else:
            KnowledgeData: KnowledgeEntity = self._knowledgeModel.Find(_dbsession, ID)
            if KnowledgeData is None:
                result.Memo = 'data error'
            else:
                Desc = 'disable/enable knowledge id:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result
                try:
                    if KnowledgeData.KnowledgeState == 2:
                        KnowledgeData.KnowledgeState = 1
                    else:
                        KnowledgeData.KnowledgeState = 2
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result
                result.Status = True
        return result

    def UpdateKnowledgeInfo(self, ClientHost: str, Token: str, ID: int, KnowledgeName: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif ID <= 0:
            result.Memo = 'wrong id'
        elif KnowledgeName == '':
            result.Memo = 'wrong knowledge name'
        else:
            KnowledgeData: KnowledgeEntity = self._knowledgeModel.Find(_dbsession, ID)
            if KnowledgeData is None:
                result.Memo = 'data error'
            elif KnowledgeData.KnowledgeName == KnowledgeName:
                result.Status = True
                return result
            else:
                Desc = 'update knowledge id:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result
                try:
                    KnowledgeData.KnowledgeName = KnowledgeName
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result
                result.Status = True
        return result

    def KnowledgeList(self, Token: str, Page: int, PageSize: int, Stext: str, SubjectID: int, KnowledgeState: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        else:
            result: ResultList = self._knowledgeModel.List(_dbsession, Page, PageSize, Stext, SubjectID, KnowledgeState)
        return result

    def KnowledgeInfo(self, Token: str, ID: int) -> Result:
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
            KnowledgeData: KnowledgeEntity = self._knowledgeModel.Find(_dbsession, ID)
            if KnowledgeData is None:
                result.Memo = 'data error'
            else:
                result.Status = True
                result.Data = KnowledgeData
        return result