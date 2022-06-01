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

            Desc = 'new manager account:' + Account
            if self.LogSysAction(_dbsession, 1, 0, Desc, ClientHost) == False:
                result.Memo = 'logging failed'
                return result

            _dbsession.commit()
            result.State = True
        return result