# -*- coding:utf-8 -*-
from Logic.BaseLogic import *


class KnowledgeLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewKnowledge(self, ClientHost: str, Token: str, KnowledgeName: str, SubjectID: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif KnowledgeName == '':
            result.Memo = self._lang.WrongKnowledgeName
        elif SubjectID <= 0:
            result.Memo = self._lang.WrongSubjectID
        elif self._knowledgeModel.FindKnowledgeCode(_dbsession, KnowledgeName) is not None:
            result.Memo = self._lang.KnowledgeDataAlreadyExists
        else:
            SubjectData: SubjectEntity = self._subjectModel.Find(_dbsession, SubjectID)
            if SubjectData is None:
                result.Memo = self._lang.SubjectDataError
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
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result

    def KnowledgeDisabled(self, ClientHost: str, Token: str, ID: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            KnowledgeData: KnowledgeEntity = self._knowledgeModel.Find(_dbsession, ID)
            if KnowledgeData is None:
                result.Memo = self._lang.KnowledgeDataError
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
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result

    def UpdateKnowledgeInfo(self, ClientHost: str, Token: str, ID: int, KnowledgeName: str):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif ID <= 0:
            result.Memo = self._lang.WrongID
        elif KnowledgeName == '':
            result.Memo = self._lang.WrongKnowledgeName
        else:
            KnowledgeData: KnowledgeEntity = self._knowledgeModel.Find(_dbsession, ID)
            if KnowledgeData is None:
                result.Memo = self._lang.KnowledgeDataError
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
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result

    def KnowledgeList(self, Token: str, Page: int, PageSize: int, Stext: str, SubjectID: int, KnowledgeState: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: ResultList = self._knowledgeModel.List(_dbsession, Page, PageSize, Stext, SubjectID, KnowledgeState)
        _dbsession.close()
        return result

    def KnowledgeInfo(self, Token: str, ID: int):
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
            KnowledgeData: KnowledgeEntity = self._knowledgeModel.Find(_dbsession, ID)
            if KnowledgeData is None:
                result.Memo = self._lang.KnowledgeDataError
            else:
                result.State = True
                result.Data = KnowledgeData
        _dbsession.close()
        return result

    def Knowledge(self, Token: str, SubjectID: int = 0):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: Result = self._knowledgeModel.Knowledge(_dbsession, SubjectID)
        _dbsession.close()
        return result