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
            ManagerData = self._managerModel.FindAccount(_dbsession, Account)
            if ManagerData is None:
                result.Memo = 'data does not exist'
            else:
                if ManagerData.PWD != self._common.UserPWD(Password):
                    result.Memo = 'wrong password'
                else:
                    ManagerData.Token = self._common.GenerateToken()
                    result = self._managerModel.Update(_dbsession, ManagerData.ID, ManagerData)
                    result.Data = ManagerData.Token
        return result

    def ManagerSignOut(self, Token: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        if Token == '':
            result.Memo = 'wrong token'
        else:
            ManagerData = self._managerModel.FindToken(_dbsession, Token)
            if ManagerData is None:
                result.Memo = 'data does not exist'
            else:
                ManagerData.Token = ''
                result = self._managerModel.Update(_dbsession, ManagerData.ID, ManagerData)
        return result

    def NewManager(self, Token: str, Account: str, Password: str, Name: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        if Token == '':
            result.Memo = 'wrong token'
        elif Account == '':
            result.Memo = 'wrong account'
        elif len(Account) < 6:
            result.Memo = 'account length is not enough'
        elif Password == '':
            result.Memo = 'wrong password'
        elif len(Password) < 6:
            result.Memo = 'password length is not enough'
        elif Name == '':
            result.Memo = 'wrong name'
        elif self.PermissionValidation(_dbsession, Token) == False:
            result.Memo = 'permission denied'
        elif self._managerModel.FindAccount(_dbsession, Account) is not None:
            result.Memo = 'data already exists'
        else:
            ManagerData = ManagerEntity()
            ManagerData.Account = Account
            ManagerData.PWD = Password
            ManagerData.Name = Name
            ManagerData.State = 1
            ManagerData.Permission = 9
            result = self._managerModel.Insert(_dbsession, ManagerData)
        return result

    def ManagerDisabled(self, Token: str, ID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        if Token == '':
            result.Memo = 'wrong token'
        elif ID <= 0:
            result.Memo = 'wrong id'
        elif self.PermissionValidation(_dbsession, Token) == False:
            result.Memo = 'permission denied'
        else:
            CheckData: Result = self._managerModel.Find(_dbsession, ID)
            if CheckData is None:
                result.Memo = 'wrong data'
            else:
                ManagerData: ManagerEntity = CheckData.Data
                if ManagerData.State == 2:
                    ManagerData.State = 1
                else:
                    ManagerData.State = 2
                result = self._managerModel.Update(_dbsession, ID, ManagerData)
        return result