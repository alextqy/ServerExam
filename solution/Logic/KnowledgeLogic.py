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
            result.Memo = 'wrong subject ID'
        elif self._knowledgeModel.FindKnowledgeCode(_dbsession, KnowledgeName) is not None:
            result.Memo = 'knowledge data already exists'
        else:
            SubjectData: SubjectEntity = self._subjectModel.Find(_dbsession, SubjectID)
            if SubjectData is None:
                result.Memo = 'subject data error'
            else:
                _dbsession.begin_nested()

                KnowledgeData = KnowledgeEntity()
                KnowledgeData.KnowledgeName = KnowledgeName
                KnowledgeData.SubjectID = SubjectID
                AddInfo: Result = self._knowledgeModel.Insert(_dbsession, KnowledgeData)
                if AddInfo.State == False:
                    result.Memo = AddInfo.Memo
                    return result

                Desc = 'new knowledge:' + KnowledgeName
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result

                _dbsession.commit()
                result.State = True
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
                result.Memo = 'knowledge data error'
            else:
                _dbsession.begin_nested()

                try:
                    if KnowledgeData.KnowledgeState == 2:
                        KnowledgeData.KnowledgeState = 1
                    else:
                        KnowledgeData.KnowledgeState = 2
                    KnowledgeData.UpdateTime = self._common.Time()
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                if KnowledgeData.KnowledgeState == 1:
                    Desc = 'enable knowledge ID:' + str(ID)
                if KnowledgeData.KnowledgeState == 2:
                    Desc = 'disable knowledge ID:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result

                _dbsession.commit()
                result.State = True
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
            result.Memo = 'wrong ID'
        elif KnowledgeName == '':
            result.Memo = 'wrong knowledge name'
        else:
            KnowledgeData: KnowledgeEntity = self._knowledgeModel.Find(_dbsession, ID)
            if KnowledgeData is None:
                result.Memo = 'knowledge data error'
            elif KnowledgeData.KnowledgeName == KnowledgeName:
                result.State = True
                return result
            else:
                if KnowledgeData.KnowledgeName != KnowledgeName:
                    KnowledgeData.KnowledgeCode = self._common.StrMD5(KnowledgeName)

                _dbsession.begin_nested()

                try:
                    KnowledgeData.KnowledgeName = KnowledgeName
                    KnowledgeData.UpdateTime = self._common.Time()
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                Desc = 'update knowledge ID:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result

                _dbsession.commit()
                result.State = True
        return result

    def KnowledgeList(self, Token: str, Page: int, PageSize: int, Stext: str, SubjectID: int, KnowledgeState: int) -> ResultList:
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
            result.Memo = 'wrong ID'
        else:
            KnowledgeData: KnowledgeEntity = self._knowledgeModel.Find(_dbsession, ID)
            if KnowledgeData is None:
                result.Memo = 'knowledge data error'
            else:
                result.State = True
                result.Data = KnowledgeData
        return result