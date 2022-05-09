from Logic.BaseLogic import *


class ManagerLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def ManagerSignIn(self, ClientHost: str, Account: str, Password: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        if Account == '':
            result.Memo = 'wrong account'
        elif Password == '':
            result.Memo = 'wrong password'
        else:
            ManagerData: ManagerEntity = self._managerModel.FindAccount(_dbsession, Account)
            if ManagerData is None:
                result.Memo = 'data does not exist'
            else:
                if ManagerData.PWD != self._common.UserPWD(Password):
                    result.Memo = 'wrong password'
                else:
                    Desc = 'manager login account:' + Account
                    if self.LogSysAction(_dbsession, 2, 0, Desc, ClientHost) == False:
                        result.Memo = 'logging failed'
                        return result
                    try:
                        ManagerData.Token = self._common.GenerateToken()
                        _dbsession.commit()
                    except Exception as e:
                        result.Memo = str(e)
                        _dbsession.rollback()
                        return result
                    result.Status = True
                    result.Data = ManagerData.Token
        return result

    def ManagerSignOut(self, ClientHost: str, Token: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        if Token == '':
            result.Memo = 'wrong token'
        else:
            ManagerData: ManagerEntity = self._managerModel.FindToken(_dbsession, Token)
            if ManagerData is None:
                result.Memo = 'data does not exist'
            else:
                Desc = 'manager logout account:' + ManagerData.Account
                if self.LogSysAction(_dbsession, 2, 0, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result
                try:
                    ManagerData.Token = ''
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result
                result.Status = True
        return result

    def NewManager(self, ClientHost: str, Token: str, Account: str, Password: str, Name: str) -> Result:
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
        elif self._managerModel.FindAccount(_dbsession, Account) is not None:
            result.Memo = 'data already exists'
        else:
            Desc = 'new manager account:' + Account
            if self.LogSysAction(_dbsession, 1, 0, Desc, ClientHost) == False:
                result.Memo = 'logging failed'
                return result
            ManagerData = ManagerEntity()
            ManagerData.Account = Account
            ManagerData.PWD = Password
            ManagerData.Name = Name
            ManagerData.State = 1
            ManagerData.Permission = 9
            result: Result = self._managerModel.Insert(_dbsession, ManagerData)
        return result

    def ManagerDisabled(self, ClientHost: str, Token: str, ID: int) -> Result:
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
            ManagerData: ManagerEntity = self._managerModel.Find(_dbsession, ID)
            if ManagerData is None:
                result.Memo = 'data error'
            else:
                Desc = 'disable/enable manager id:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result
                try:
                    if ManagerData.State == 2:
                        ManagerData.State = 1
                    else:
                        ManagerData.State = 2
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result
                result.Status = True
        return result

    def ManagerChangePassword(self, ClientHost: str, Token: str, NewPassword: str, ID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif NewPassword == '':
            result.Memo = 'wrong new password'
        elif len(NewPassword) < 6:
            result.Memo = 'password length is not enough'
        else:
            if ID == 0:
                ManagerData: ManagerEntity = self._managerModel.FindToken(_dbsession, Token)
            else:
                ManagerData: ManagerEntity = self._managerModel.Find(_dbsession, ID)
            if ManagerData is None:
                result.Memo = 'data error'
            else:
                Desc = 'manager change password account:' + ManagerData.Account
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result
                result: Result = self._managerModel.ChangePassword(_dbsession, ManagerData, NewPassword)
        return result

    def UpdateManagerInfo(self, ClientHost: str, Token: str, Name: str, Permission: int, ID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif Name == '':
            result.Memo = 'wrong name'
        elif Permission <= 0:
            result.Memo = 'wrong permission'
        else:
            if ID == 0:
                ManagerData: ManagerEntity = self._managerModel.FindToken(_dbsession, Token)
            else:
                ManagerData: ManagerEntity = self._managerModel.Find(_dbsession, ID)
            if ManagerData is None:
                result.Memo = 'data error'
            else:
                Desc = 'update manager id:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result
                try:
                    Data: ManagerEntity = ManagerData
                    Data.Name = Name
                    Data.Permission = Permission
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result
                result.Status = True
        return result

    def ManagerList(self, Token: str, Page: int, PageSize: int, Stext: str, State: int, Permission: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        else:
            result: ResultList = self._managerModel.List(_dbsession, Page, PageSize, Stext, State, Permission)
        return result

    def ManagerInfo(self, Token: str, ID: int):
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
            ManagerData: ManagerEntity = self._managerModel.Find(_dbsession, ID)
            if ManagerData is None:
                result.Memo = 'data error'
            else:
                result.Status = True
                result.Data = ManagerData
        return result