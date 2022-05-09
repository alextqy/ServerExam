from Logic.BaseLogic import *


class SubjectLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewSubject(self, ClientHost: str, Token: str, SubjectName: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif SubjectName == '':
            result.Memo = 'wrong subject name'
        elif self._subjectModel.FindSubjectCode(_dbsession, SubjectName) is not None:
            result.Memo = 'data already exists'
        else:
            Desc = 'new subject:' + SubjectName
            if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                result.Memo = 'logging failed'
                return result
            SubjectData = SubjectEntity()
            SubjectData.SubjectName = SubjectName
            result: Result = self._subjectModel.Insert(_dbsession, SubjectData)
        return result

    def SubjectDisabled(self, ClientHost: str, Token: str, ID: int) -> Result:
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
            SubjectData: SubjectEntity = self._subjectModel.Find(_dbsession, ID)
            if SubjectData is None:
                result.Memo = 'data error'
            else:
                Desc = 'disable/enable subject id:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result
                try:
                    if SubjectData.SubjectState == 2:
                        SubjectData.SubjectState = 1
                    else:
                        SubjectData.SubjectState = 2
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result
                result.Status = True
        return result

    def UpdateSubjectInfo(self, ClientHost: str, Token: str, ID: int, SubjectName: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif ID <= 0:
            result.Memo = 'wrong id'
        elif SubjectName == '':
            result.Memo = 'wrong subject name'
        else:
            SubjectData: SubjectEntity = self._subjectModel.Find(_dbsession, ID)
            if SubjectData is None:
                result.Memo = 'data error'
            elif SubjectData.SubjectName == SubjectName:
                result.Status = True
                return result
            elif self._subjectModel.FindSubjectCode(_dbsession, SubjectName) is not None:
                result.Memo = 'data already exists'
            else:
                Desc = 'update subject id:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result
                SubjectData.SubjectName = SubjectName
                result: Result = self._subjectModel.Update(_dbsession, ID, SubjectData)
        return result

    def SubjectList(self, Token: str, Page: int, PageSize: int, Stext: str, SubjectState: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        else:
            result: ResultList = self._subjectModel.List(_dbsession, Page, PageSize, Stext, SubjectState)
        return result

    def SubjectInfo(self, Token: str, ID: int) -> Result:
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
            SubjectData: SubjectEntity = self._subjectModel.Find(_dbsession, ID)
            if SubjectData is None:
                result.Memo = 'data error'
            else:
                result.Status = True
                result.Data = SubjectData
        return result