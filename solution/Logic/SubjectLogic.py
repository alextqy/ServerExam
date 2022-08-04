# -*- coding:utf-8 -*-
from Logic.BaseLogic import *


class SubjectLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewSubject(self, ClientHost: str, Token: str, SubjectName: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif SubjectName == '':
            result.Memo = self._lang.WrongSubjectName
        elif self._subjectModel.FindSubjectCode(_dbsession, SubjectName) is not None:
            result.Memo = self._lang.SubjectDataAlreadyExists
        else:
            _dbsession.begin_nested()

            SubjectData = SubjectEntity()
            SubjectData.SubjectName = SubjectName
            AddInfo: Result = self._subjectModel.Insert(_dbsession, SubjectData)
            if AddInfo.State == False:
                result.Memo = AddInfo.Memo
                return result

            Desc = 'new subject:' + SubjectName
            if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                result.Memo = self._lang.LoggingFailed
                return result

            _dbsession.commit()
            result.State = True
        _dbsession.close()
        return result

    def SubjectDisabled(self, ClientHost: str, Token: str, ID: int) -> Result:
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
            SubjectData: SubjectEntity = self._subjectModel.Find(_dbsession, ID)
            if SubjectData is None:
                result.Memo = self._lang.SubjectDataError
            else:
                _dbsession.begin_nested()

                try:
                    if SubjectData.SubjectState == 2:
                        SubjectData.SubjectState = 1
                    else:
                        SubjectData.SubjectState = 2
                    SubjectData.UpdateTime = self._common.Time()
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                if SubjectData.SubjectState == 1:
                    Desc = 'enable subject ID:' + str(ID)
                if SubjectData.SubjectState == 2:
                    Desc = 'disable subject ID:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result

    def UpdateSubjectInfo(self, ClientHost: str, Token: str, ID: int, SubjectName: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif ID <= 0:
            result.Memo = self._lang.WrongID
        elif SubjectName == '':
            result.Memo = self._lang.WrongSubjectName
        else:
            SubjectData: SubjectEntity = self._subjectModel.Find(_dbsession, ID)
            if SubjectData is None:
                result.Memo = self._lang.SubjectDataError
            elif SubjectData.SubjectName == SubjectName:
                result.State = True
                return result
            elif self._subjectModel.FindSubjectCode(_dbsession, SubjectName) is not None:
                result.Memo = self._lang.SubjectDataAlreadyExists
            else:
                if SubjectData.SubjectName != SubjectName:
                    SubjectData.SubjectCode = self._common.StrMD5(SubjectName)

                _dbsession.begin_nested()

                try:
                    SubjectData.SubjectName = SubjectName
                    SubjectData.UpdateTime = self._common.Time()
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                Desc = 'update subject ID:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result

    def SubjectList(self, Token: str, Page: int, PageSize: int, Stext: str, SubjectState: int) -> ResultList:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: ResultList = self._subjectModel.List(_dbsession, Page, PageSize, Stext, SubjectState)
        _dbsession.close()
        return result

    def SubjectInfo(self, Token: str, ID: int) -> Result:
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
            SubjectData: SubjectEntity = self._subjectModel.Find(_dbsession, ID)
            if SubjectData is None:
                result.Memo = self._lang.SubjectDataError
            else:
                result.State = True
                result.Data = SubjectData
        _dbsession.close()
        return result

    def Subjects(self, Token: str) -> ResultList:
        result = ResultList()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: ResultList = self._subjectModel.Subjects(_dbsession)
        _dbsession.close()
        return result