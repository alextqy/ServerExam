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
        elif self._subjectModel.FindSubjectName(_dbsession, SubjectName) is not None:
            result.Memo = 'subject data already exists'
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
                result.Memo = 'logging failed'
                return result

            _dbsession.commit()
            result.State = True
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
            result.Memo = 'wrong ID'
        else:
            SubjectData: SubjectEntity = self._subjectModel.Find(_dbsession, ID)
            if SubjectData is None:
                result.Memo = 'subject data error'
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
                    result.Memo = 'logging failed'
                    return result

                _dbsession.commit()
                result.State = True
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
            result.Memo = 'wrong ID'
        elif SubjectName == '':
            result.Memo = 'wrong subject name'
        else:
            SubjectData: SubjectEntity = self._subjectModel.Find(_dbsession, ID)
            if SubjectData is None:
                result.Memo = 'subject data error'
            elif SubjectData.SubjectName == SubjectName:
                result.State = True
                return result
            elif self._subjectModel.FindSubjectName(_dbsession, SubjectName) is not None:
                result.Memo = 'subject data already exists'
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
                    result.Memo = 'logging failed'
                    return result

                _dbsession.commit()
                result.State = True
        return result

    def SubjectList(self, Token: str, Page: int, PageSize: int, Stext: str, SubjectState: int) -> ResultList:
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
            result.Memo = 'wrong ID'
        else:
            SubjectData: SubjectEntity = self._subjectModel.Find(_dbsession, ID)
            if SubjectData is None:
                result.Memo = 'subject data error'
            else:
                result.State = True
                result.Data = SubjectData
        return result