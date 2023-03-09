# -*- coding:utf-8 -*-
from Logic.BaseLogic import *


class ManagerLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def ManagerSignIn(self, ClientHost: str, Account: str, Password: str):
        result = Result()
        _dbsession = DBsession()
        if Account == '':
            result.Memo = self._lang.WrongAccount
        elif Password == '':
            result.Memo = self._lang.WrongPassword
        else:
            ManagerData: ManagerEntity = self._managerModel.FindAccount(_dbsession, Account)
            if ManagerData is None:
                result.Memo = self._lang.ManagerDataDoesNotExist
            else:
                if ManagerData.State != 1:
                    result.Memo = self._lang.ManagerIsDisabled
                elif ManagerData.Password != self._common.UserPWD(Password):
                    result.Memo = self._lang.WrongPassword
                else:
                    _dbsession.begin_nested()

                    try:
                        ManagerData.Token = self._common.GenerateToken()
                        _dbsession.commit()
                    except Exception as e:
                        result.Memo = str(e)
                        _dbsession.rollback()
                        return result

                    Desc = 'manager login account:' + Account
                    if self.LogSysAction(_dbsession, 2, 0, Desc, ClientHost) == False:
                        result.Memo = self._lang.LoggingFailed
                        return result

                    _dbsession.commit()
                    result.State = True
                    result.Data = ManagerData.Token
        _dbsession.close()
        return result

    def ManagerSignOut(self, ClientHost: str, Token: str):
        result = Result()
        _dbsession = DBsession()
        if Token == '':
            result.Memo = self._lang.WrongToken
        else:
            ManagerData: ManagerEntity = self._managerModel.FindToken(_dbsession, Token)
            if ManagerData is None:
                result.Memo = self._lang.ManagerDataDoesNotExist
            else:
                _dbsession.begin_nested()

                try:
                    ManagerData.Token = ''
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                Desc = 'manager logout account:' + ManagerData.Account
                if self.LogSysAction(_dbsession, 2, 0, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result

    def NewManager(self, ClientHost: str, Token: str, Account: str, Password: str, Name: str):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif Account == '':
            result.Memo = self._lang.WrongAccount
        elif len(Account) < 6:
            result.Memo = self._lang.AccountLengthIsNotEnough
        elif self._common.MatchAll(Account) == False:
            result.Memo = self._lang.AccountFormatError
        elif Password == '':
            result.Memo = self._lang.WrongPassword
        elif len(Password) < 6:
            result.Memo = self._lang.PasswordLengthIsNotEnough
        elif Name == '':
            result.Memo = self._lang.WrongName
        elif self._managerModel.FindAccount(_dbsession, Account) is not None:
            result.Memo = self._lang.ManagerDataAlreadyExists
        else:
            _dbsession.begin_nested()

            ManagerData = ManagerEntity()
            ManagerData.Account = Account
            ManagerData.Password = Password
            ManagerData.Name = Name
            ManagerData.State = 1
            ManagerData.Permission = 9
            AddInfo: Result = self._managerModel.Insert(_dbsession, ManagerData)
            if AddInfo.State == False:
                result.Memo = AddInfo.Memo
                return result

            Desc = 'new manager account:' + Account
            if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                result.Memo = self._lang.LoggingFailed
                return result

            _dbsession.commit()
            result.State = True
        _dbsession.close()
        return result

    def ManagerDisabled(self, ClientHost: str, Token: str, ID: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif ID <= 0:
            result.Memo = self._lang.WrongID
        elif ID == 1:
            result.Memo = self._lang.OperationFailed
        else:
            ManagerData: ManagerEntity = self._managerModel.Find(_dbsession, ID)
            if ManagerData is None:
                result.Memo = self._lang.ManagerDataError
            else:
                _dbsession.begin_nested()

                try:
                    if ManagerData.State == 2:
                        ManagerData.State = 1
                    else:
                        ManagerData.State = 2
                    ManagerData.UpdateTime = self._common.Time()
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                if ManagerData.State == 1:
                    Desc = 'enable manager ID:' + str(ID)
                if ManagerData.State == 2:
                    Desc = 'disable manager ID:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result

    def ManagerChangePassword(self, ClientHost: str, Token: str, NewPassword: str, ID: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif NewPassword == '':
            result.Memo = self._lang.WrongNewPassword
        elif len(NewPassword) < 6:
            result.Memo = self._lang.PasswordLengthIsNotEnough
        else:
            if ID == 0:
                ManagerData: ManagerEntity = self._managerModel.FindToken(_dbsession, Token)
            else:
                ManagerData: ManagerEntity = self._managerModel.Find(_dbsession, ID)
            if ManagerData is None:
                result.Memo = self._lang.ManagerDataError
            else:
                _dbsession.begin_nested()

                ChangeInfo: Result = self._managerModel.ChangePassword(_dbsession, ManagerData, NewPassword)
                if ChangeInfo.State == False:
                    result.Memo = self._lang.FailToEdit
                    return result

                Desc = 'manager change password account:' + ManagerData.Account
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result

    def UpdateManagerInfo(self, ClientHost: str, Token: str, Name: str, Permission: int, ID: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif Name == '':
            result.Memo = self._lang.WrongName
        elif Permission <= 0:
            result.Memo = self._lang.WrongPermission
        else:
            if ID == 0:
                ManagerData: ManagerEntity = self._managerModel.FindToken(_dbsession, Token)
            else:
                ManagerData: ManagerEntity = self._managerModel.Find(_dbsession, ID)
            if ManagerData is None:
                result.Memo = self._lang.ManagerDataError
            else:
                _dbsession.begin_nested()

                try:
                    ManagerData.Name = Name
                    ManagerData.Permission = Permission
                    ManagerData.UpdateTime = self._common.Time()
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                Desc = 'update manager ID:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result

    def ManagerList(self, Token: str, Page: int, PageSize: int, Stext: str, State: int, Permission: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: ResultList = self._managerModel.List(_dbsession, Page, PageSize, Stext, State, Permission)
        _dbsession.close()
        return result

    def ManagerInfo(self, Token: str, ID: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        # elif ID <= 0:
        #     result.Memo = self._lang.WrongID
        else:
            if ID <= 0:
                ID = AdminID
            ManagerData: ManagerEntity = self._managerModel.Find(_dbsession, ID)
            if ManagerData is None:
                result.Memo = self._lang.ManagerDataError
            else:
                result.State = True
                result.Data = ManagerData
        _dbsession.close()
        return result

    def Managers(self, Token: str):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: Result = self._managerModel.Managers(_dbsession)
        _dbsession.close()
        return result