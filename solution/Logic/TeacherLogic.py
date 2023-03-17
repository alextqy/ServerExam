# -*- coding:utf-8 -*-
from Logic.BaseLogic import *


class TeacherLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewTeacher(self, ClientHost: str, Token: str, Account: str, Password: str, Name: str):
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
        elif self._teacherModel.FindAccount(_dbsession, Account) is not None:
            result.Memo = self._lang.TeacherDataAlreadyExists
        else:
            _dbsession.begin_nested()

            TeacherData = TeacherEntity()
            TeacherData.Account = Account
            TeacherData.Password = Password
            TeacherData.Name = Name
            TeacherData.State = 1
            AddInfo: Result = self._teacherModel.Insert(_dbsession, TeacherData)
            if AddInfo.State == False:
                result.Memo = AddInfo.Memo
                _dbsession.rollback()
                return result

            Desc = 'new teacher account:' + Account
            if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                result.Memo = self._lang.LoggingFailed
                _dbsession.rollback()
                return result

            _dbsession.commit()
            result.State = True
        _dbsession.close()
        return result

    def TeacherDisabled(self, ClientHost: str, Token: str, ID: int):
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
            TeacherData: TeacherEntity = self._teacherModel.Find(_dbsession, ID)
            if TeacherData is None:
                result.Memo = self._lang.TeacherDataError
            else:
                _dbsession.begin_nested()

                try:
                    if TeacherData.State == 2:
                        TeacherData.State = 1
                    else:
                        TeacherData.State = 2
                    TeacherData.UpdateTime = self._common.Time()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                if TeacherData.State == 1:
                    Desc = 'enable Teacher ID:' + str(ID)
                if TeacherData.State == 2:
                    Desc = 'disable Teacher ID:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    _dbsession.rollback()
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result

    def UpdateTeacherInfo(self, ClientHost: str, Token: str, Password: str, Name: str, ID: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif Name == '':
            result.Memo = self._lang.WrongName
        else:
            _dbsession.begin_nested()

            TeacherData: TeacherEntity = self._teacherModel.Find(_dbsession, ID)
            if TeacherData is None:
                result.Memo = self._lang.TeacherDataError
                _dbsession.rollback()
                return result

            if Password != '':
                if len(Password) < 6:
                    result.Memo = self._lang.PasswordLengthIsNotEnough
                    _dbsession.rollback()
                    return result
                else:
                    TeacherData.Password = self._common.UserPWD(Password.strip())

            TeacherData.Name = Name

            Desc = 'update teacker info ID:' + str(ID)
            if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                result.Memo = self._lang.LoggingFailed
                _dbsession.rollback()
                return result

            _dbsession.commit()
            result.State = True
        _dbsession.close()
        return result

    def TeacherList(self, Token: str, Page: int, PageSize: int, Stext: str, State: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: ResultList = self._teacherModel.List(_dbsession, Page, PageSize, Stext, State)
        _dbsession.close()
        return result

    def TeacherInfo(self, Token: str, ID: int):
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
            TeacherData: TeacherEntity = self._teacherModel.Find(_dbsession, ID)
            if TeacherData is None:
                result.Memo = self._lang.TeacherDataError
            else:
                result.State = True
                result.Data = TeacherData
        _dbsession.close()
        return result

    def Teachers(self, Token: str):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: ResultList = self._teacherModel.Teachers(_dbsession)
        _dbsession.close()
        return result


# ========================================================================= teacher side =========================================================================

    def TeacherSignIn(self, ClientHost: str, Account: str, Password: str):
        result = Result()
        _dbsession = DBsession()
        if Account == '':
            result.Memo = self._lang.WrongAccount
        elif Password == '':
            result.Memo = self._lang.WrongPassword
        else:
            TeacherData: TeacherEntity = self._teacherModel.FindAccount(_dbsession, Account)
            if TeacherData is None:
                result.Memo = self._lang.TeacherDataDoesNotExist
            else:
                if TeacherData.State != 1:
                    result.Memo = self._lang.TeacherIsDisabled
                elif TeacherData.Password != self._common.UserPWD(Password):
                    result.Memo = self._lang.WrongPassword
                else:
                    _dbsession.begin_nested()

                    try:
                        TeacherData.Token = self._common.GenerateToken()
                    except Exception as e:
                        result.Memo = str(e)
                        _dbsession.rollback()
                        return result

                    Desc = 'teacher login account:' + Account
                    if self.LogSysAction(_dbsession, 2, 0, Desc, ClientHost) == False:
                        result.Memo = self._lang.LoggingFailed
                        _dbsession.rollback()
                        return result

                    _dbsession.commit()
                    result.State = True
                    result.Data = TeacherData.Token
        _dbsession.close()
        return result

    def TeacherSignOut(self, ClientHost: str, Token: str):
        result = Result()
        _dbsession = DBsession()
        if Token == '':
            result.Memo = self._lang.WrongToken
        else:
            TeacherData: TeacherEntity = self._teacherModel.FindToken(_dbsession, Token)
            if TeacherData is None:
                result.Memo = self._lang.TeacherDataDoesNotExist
            else:
                _dbsession.begin_nested()

                try:
                    TeacherData.Token = ''
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                Desc = 'teacher logout account:' + TeacherData.Account
                if self.LogSysAction(_dbsession, 2, 0, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    _dbsession.rollback()
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result

    def CheckTeacherInfo(self, Token: str):
        result = Result()
        _dbsession = DBsession()
        TeacherID = self.TeacherPermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif TeacherID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            TeacherData: TeacherEntity = self._teacherModel.Find(_dbsession, TeacherID)
            if TeacherData is None:
                result.Memo = self._lang.TeacherDataError
            else:
                result.State = True
                result.Data = TeacherData
        _dbsession.close()
        return result

    def TeacherUpdate(self, ClientHost: str, Token: str, Name: str):
        result = Result()
        _dbsession = DBsession()
        TeacherID = self.TeacherPermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif TeacherID == 0:
            result.Memo = self._lang.PermissionDenied
        elif Name == '':
            result.Memo = self._lang.WrongName
        else:
            _dbsession.begin_nested()

            TeacherData: TeacherEntity = self._teacherModel.Find(_dbsession, TeacherID)
            if TeacherData is None:
                result.Memo = self._lang.TeacherDataError
                _dbsession.rollback()
                return result

            TeacherData.Name = Name

            _dbsession.commit()
            result.State = True
        _dbsession.close()
        return result

    def TeacherChangePassword(self, ClientHost: str, Token: str, NewPassword: str):
        result = Result()
        _dbsession = DBsession()
        TeacherID = self.TeacherPermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif TeacherID == 0:
            result.Memo = self._lang.PermissionDenied
        elif NewPassword == '':
            result.Memo = self._lang.WrongNewPassword
        elif len(NewPassword) < 6:
            result.Memo = self._lang.PasswordLengthIsNotEnough
        else:
            TeacherData: TeacherEntity = self._teacherModel.Find(_dbsession, TeacherID)
            if TeacherData is None:
                result.Memo = self._lang.TeacherDataError
            else:
                _dbsession.begin_nested()

                ChangeInfo: Result = self._teacherModel.ChangePassword(_dbsession, TeacherData, NewPassword)
                if ChangeInfo.State == False:
                    result.Memo = self._lang.FailToEdit
                    _dbsession.rollback()
                    return result

                Desc = 'teacher change password account:' + TeacherData.Account
                if self.LogSysAction(_dbsession, 1, TeacherID, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    _dbsession.rollback()
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result

    def TheTeacherClass(self, Token: str):
        result = Result()
        _dbsession = DBsession()
        TeacherID = self.TeacherPermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif TeacherID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            TempResult: Result = self._teacherClassModel.Classes(_dbsession, TeacherID)
            ClassIDList = []
            ClassList = []
            if TempResult.Data != '':
                for i in TempResult.Data:
                    Data: TeacherClassEntity = i
                    ClassIDList.append(Data.ClassID)
            if len(ClassIDList) > 0:
                for i in ClassIDList:
                    Data: Result = self._classModel.Find(_dbsession, i)
                    ClassList.append(Data)
            result.Data = ClassList
            result.State = True
        _dbsession.close()
        return result

    def TeacherExamineeList(self, Token: str, Page: int, PageSize: int, Stext: str, ClassID: int):
        result = Result()
        _dbsession = DBsession()
        TeacherID = self.TeacherPermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif TeacherID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            if ClassID > 0:
                result: ResultList = self._examineeModel.List(_dbsession, Page, PageSize, Stext, ClassID)
        _dbsession.close()
        return result

    def TeacherNewExaminee(self, ClientHost: str, Token: str, ExamineeNo: str, Name: str, ClassID: int, Contact: str):
        result = Result()
        _dbsession = DBsession()
        TeacherID = self.TeacherPermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif TeacherID == 0:
            result.Memo = self._lang.PermissionDenied
        elif ExamineeNo == '':
            result.Memo = self._lang.WrongExamineeNo
        elif Name == '':
            result.Memo = self._lang.WrongName
        elif ClassID <= 0:
            result.Memo = self._lang.WrongClassID
        elif self._examineeModel.FindExamineeNo(_dbsession, ExamineeNo) is not None:
            result.Memo = self._lang.ExamineeNoDataAlreadyExists
        elif self._classModel.Find(_dbsession, ClassID) is None:
            result.Memo = self._lang.ClassDataDoesNotExist
        else:
            if Contact == '':
                Contact = 'none'

            _dbsession.begin_nested()

            ExamineeData = ExamineeEntity()
            ExamineeData.ExamineeNo = ExamineeNo
            ExamineeData.Name = Name
            ExamineeData.ClassID = ClassID
            ExamineeData.Contact = Contact
            AddInfo: Result = self._examineeModel.Insert(_dbsession, ExamineeData)
            if AddInfo.State == False:
                result.Memo = AddInfo.Memo
                _dbsession.rollback()
                return result

            _dbsession.commit()
            result.State = True
        _dbsession.close()
        return result

    def TeacherUpdateExaminee(self, ClientHost: str, Token: str, ID: int, Name: str, Contact: str, ClassID: int):
        result = Result()
        _dbsession = DBsession()
        TeacherID = self.TeacherPermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif TeacherID == 0:
            result.Memo = self._lang.PermissionDenied
        elif ID <= 0:
            result.Memo = self._lang.WrongID
        elif Name == '':
            result.Memo = self._lang.WrongName
        elif ClassID <= 0:
            result.Memo = self._lang.WrongClassID
        else:
            if Contact == '':
                Contact = 'none'

            ExamineeData: ExamineeEntity = self._examineeModel.Find(_dbsession, ID)
            if ExamineeData is None:
                result.Memo = self._lang.ExamineeDataError
                return result

            _dbsession.begin_nested()

            try:
                ExamineeData.Name = Name
                ExamineeData.Contact = Contact
                ExamineeData.ClassID = ClassID
            except Exception as e:
                result.Memo = str(e)
                _dbsession.rollback()
                return result

            _dbsession.commit()
            result.State = True
        _dbsession.close()
        return result

    # type 1 当前 2 历史
    def TeacherExamInfoList(self, Token: str, Type: int, Page: int, PageSize: int, Stext: str, ExamState: int, ExamType: int, Pass: int, StartState: int, SuspendedState: int, ExamineeID: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.TeacherPermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            if Type == 1:
                result: ResultList = self._examInfoModel.List(_dbsession, Page, PageSize, Stext, ExamState, ExamType, Pass, StartState, SuspendedState, ExamineeID)
            if Type == 2:
                result: ResultList = self._examInfoHistoryModel.List(_dbsession, Page, PageSize, Stext, ExamState, ExamType, Pass, ExamineeID)
        _dbsession.close()
        return result

    # type 1 当前 2 历史
    def TeacherScantronList(self, Token: str, Type: int, Page: int, PageSize: int, ExamID: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.TeacherPermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            if Type == 1:
                result: ResultList = self._scantronModel.List(_dbsession, Page, PageSize, ExamID)
            if Type == 2:
                result: ResultList = self._scantronHistoryModel.List(_dbsession, Page, PageSize, ExamID)
        _dbsession.close()
        return result

    def TeacherScantronViewAttachments(self, Token: str, FilePath: str):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            import struct
            if FilePath != '' and FilePath != 'none':
                with open(FilePath, 'rb') as f:
                    BtFile = f.read()
                content = struct.unpack('B' * len(BtFile), BtFile)
                result.State = True
                result.Memo = self._file.CheckFileType(FilePath)
                result.Data = content
        _dbsession.close()
        return result

    # type 1 当前 2 历史
    def TeacherScantronSolutionList(self, Token: str, Type: int, Page: int, PageSize: int, ScantronID: int, Position: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.TeacherPermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            if Type == 1:
                result: ResultList = self._scantronSolutionModel.List(_dbsession, Page, PageSize, ScantronID, Position)
            if Type == 2:
                result: ResultList = self._scantronSolutionHistoryModel.List(_dbsession, Page, PageSize, ScantronID, Position)
        _dbsession.close()
        return result

    def TeacherScantronSolutionViewAttachments(self, Token: str, OptionAttachment: str):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.TeacherPermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            import struct
            if OptionAttachment != '' and OptionAttachment != 'none':
                with open(OptionAttachment, 'rb') as f:
                    BtFile = f.read()
                content = struct.unpack('B' * len(BtFile), BtFile)
                result.State = True
                result.Memo = self._file.CheckFileType(OptionAttachment)
                result.Data = content
        _dbsession.close()
        return result