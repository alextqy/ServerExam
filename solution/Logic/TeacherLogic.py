from Logic.BaseLogic import *


class TeacherLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewTeacher(self, ClientHost: str, Token: str, Account: str, Password: str, Name: str, ClassID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif Account == '':
            result.Memo = 'wrong account'
        elif len(Account) < 6:
            result.Memo = 'account length is not enough'
        elif self._common.MatchAll(Account) == False:
            result.Memo = 'account format error'
        elif Password == '':
            result.Memo = 'wrong password'
        elif len(Password) < 6:
            result.Memo = 'password length is not enough'
        elif Name == '':
            result.Memo = 'wrong name'
        elif ClassID <= 0:
            result.Memo = 'wrong class id'
        elif self._teacherModel.FindAccount(_dbsession, Account) is not None:
            result.Memo = 'teacher data already exists'
        elif self._classModel.Find(_dbsession, ClassID) is None:
            result.Memo = 'class data does not exist'
        else:
            _dbsession.begin_nested()

            TeacherData = TeacherEntity()
            TeacherData.Account = Account
            TeacherData.Password = Password
            TeacherData.Name = Name
            TeacherData.ClassID = ClassID
            TeacherData.State = 1
            AddInfo: Result = self._teacherModel.Insert(_dbsession, TeacherData)
            if AddInfo.State == False:
                result.Memo = AddInfo.Memo
                return result

            Desc = 'new teacher account:' + Account
            if self.LogSysAction(_dbsession, 1, 0, Desc, ClientHost) == False:
                result.Memo = 'logging failed'
                return result

            _dbsession.commit()
            result.State = True
        return result

    def TeacherDisabled(self, ClientHost: str, Token: str, ID: int) -> Result:
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
            TeacherData: TeacherEntity = self._teacherModel.Find(_dbsession, ID)
            if TeacherData is None:
                result.Memo = 'teacher data error'
            else:
                _dbsession.begin_nested()

                try:
                    if TeacherData.State == 2:
                        TeacherData.State = 1
                    else:
                        TeacherData.State = 2
                    TeacherData.UpdateTime = self._common.Time()
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                if TeacherData.State == 1:
                    Desc = 'enable Teacher id:' + str(ID)
                if TeacherData.State == 2:
                    Desc = 'disable Teacher id:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result

                _dbsession.commit()
                result.State = True
        return result

    def UpdateTeacherInfo(self, ClientHost: str, Token: str, Password: str, Name: str, ClassID: int, ID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif Name == '':
            result.Memo = 'wrong name'
        else:
            _dbsession.begin_nested()

            TeacherData: TeacherEntity = self._teacherModel.Find(_dbsession, ID)
            if TeacherData is None:
                result.Memo = 'teacher data error'
                return result

            if Password != '':
                if len(Password) < 6:
                    result.Memo = 'password length is not enough'
                    return result
                else:
                    TeacherData.Password = self._common.UserPWD(Password.strip())

            if ClassID > 0:
                if self._classModel.Find(_dbsession, ClassID) is None:
                    result.Memo = 'class data error'
                    return result
                else:
                    TeacherData.ClassID = ClassID

            TeacherData.Name = Name

            Desc = 'update teacker info id:' + str(ID)
            if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                result.Memo = 'logging failed'
                return result

            _dbsession.commit()
            result.State = True
        return result

    def TeacherList(self, Token: str, Page: int, PageSize: int, Stext: str, State: int, ClassID: int) -> ResultList:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        else:
            result: ResultList = self._teacherModel.List(_dbsession, Page, PageSize, Stext, State, ClassID)
        return

    def TeacherInfo(self, Token: str, ID: int) -> Result:
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
            TeacherData: TeacherEntity = self._teacherModel.Find(_dbsession, ID)
            if TeacherData is None:
                result.Memo = 'teacher data error'
            else:
                result.State = True
                result.Data = TeacherData
        return result

    def TeacherSignIn(self, ClientHost: str, Account: str, Password: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        if Account == '':
            result.Memo = 'wrong account'
        elif Password == '':
            result.Memo = 'wrong password'
        else:
            TeacherData: TeacherEntity = self._teacherModel.FindAccount(_dbsession, Account)
            if TeacherData is None:
                result.Memo = 'teacher data does not exist'
            else:
                if TeacherData.State != 1:
                    result.Memo = 'teacher is disabled'
                elif TeacherData.Password != self._common.UserPWD(Password):
                    result.Memo = 'wrong password'
                else:
                    _dbsession.begin_nested()

                    try:
                        TeacherData.Token = self._common.GenerateToken()
                        _dbsession.commit()
                    except Exception as e:
                        result.Memo = str(e)
                        _dbsession.rollback()
                        return result

                    Desc = 'teacher login account:' + Account
                    if self.LogSysAction(_dbsession, 2, 0, Desc, ClientHost) == False:
                        result.Memo = 'logging failed'
                        return result

                    _dbsession.commit()
                    result.State = True
                    result.Data = TeacherData.Token
        return result

    def TeacherSignOut(self, ClientHost: str, Token: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        if Token == '':
            result.Memo = 'wrong token'
        else:
            TeacherData: TeacherEntity = self._teacherModel.FindToken(_dbsession, Token)
            if TeacherData is None:
                result.Memo = 'teacher data does not exist'
            else:
                _dbsession.begin_nested()

                try:
                    TeacherData.Token = ''
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                Desc = 'teacher logout account:' + TeacherData.Account
                if self.LogSysAction(_dbsession, 2, 0, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result

                _dbsession.commit()
                result.State = True
        return result

    def TeacherChangePassword(self, ClientHost: str, Token: str, NewPassword: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        TeacherID = self.TeacherPermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif TeacherID == 0:
            result.Memo = 'permission denied'
        elif NewPassword == '':
            result.Memo = 'wrong new password'
        elif len(NewPassword) < 6:
            result.Memo = 'password length is not enough'
        else:
            TeacherData: TeacherEntity = self._teacherModel.FindToken(_dbsession, Token)
            if TeacherData is None:
                result.Memo = 'teacher data error'
            else:
                _dbsession.begin_nested()

                ChangeInfo: Result = self._teacherModel.ChangePassword(_dbsession, TeacherData, NewPassword)
                if ChangeInfo.State == False:
                    result.Memo = 'fail to edit'
                    return result

                Desc = 'teacher change password account:' + TeacherData.Account
                if self.LogSysAction(_dbsession, 1, TeacherID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result

                _dbsession.commit()
                result.State = True
        return result