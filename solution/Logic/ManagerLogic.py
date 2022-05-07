from Logic.BaseLogic import *


class ManagerLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def ManagerSignIn(self, Account: str, Password: str) -> Result:
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

    def ManagerSignOut(self, Token: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        if Token == '':
            result.Memo = 'wrong token'
        else:
            ManagerData: ManagerEntity = self._managerModel.FindToken(_dbsession, Token)
            if ManagerData is None:
                result.Memo = 'data does not exist'
            else:
                try:
                    ManagerData.Token = ''
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result
                result.Status = True
        return result

    def NewManager(self, Token: str, Account: str, Password: str, Name: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        if Token == '':
            result.Memo = 'wrong token'
        elif self.PermissionValidation(_dbsession, Token) == False:
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
            ManagerData = ManagerEntity()
            ManagerData.Account = Account
            ManagerData.PWD = Password
            ManagerData.Name = Name
            ManagerData.State = 1
            ManagerData.Permission = 9
            result: Result = self._managerModel.Insert(_dbsession, ManagerData)
        return result

    def ManagerDisabled(self, Token: str, ID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        if Token == '':
            result.Memo = 'wrong token'
        elif self.PermissionValidation(_dbsession, Token) == False:
            result.Memo = 'permission denied'
        elif ID <= 0:
            result.Memo = 'wrong id'
        else:
            ManagerData: ManagerEntity = self._managerModel.Find(_dbsession, ID)
            if ManagerData is None:
                result.Memo = "data error"
            else:
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

    def ManagerChangePassword(self, Token: str, NewPassword: str, ID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        if Token == '':
            result.Memo = 'wrong token'
        elif self.PermissionValidation(_dbsession, Token) == False:
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
                if self._managerModel.ChangePassword(_dbsession, ManagerData, NewPassword) == True:
                    result.Status = True
        return result

    def UpdateManagerInfo(self, Token: str, Name: str, Permission: int, ID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        if Token == '':
            result.Memo = 'wrong token'
        elif self.PermissionValidation(_dbsession, Token) == False:
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
                try:
                    Data: ManagerEntity = ManagerData
                    Data.SetName(Name)
                    Data.SetPermission(Permission)
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
        if Token == '':
            result.Memo = 'wrong token'
        elif self.PermissionValidation(_dbsession, Token) == False:
            result.Memo = 'permission denied'
        else:
            result: ResultList = self._managerModel.List(_dbsession, Page, PageSize, Stext, State, Permission)
        return result

    def ManagerInfo(self, Token: str, ID: int):
        result = Result()
        _dbsession = DBsession()
        if Token == '':
            result.Memo = 'wrong token'
        elif self.PermissionValidation(_dbsession, Token) == False:
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