# -*- coding:utf-8 -*-
from Logic.BaseLogic import *


class ExamineeLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewExaminee(self, ClientHost: str, Token: str, ExamineeNo: str, Name: str, ClassID: int, Contact: str):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
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
                return result

            Desc = 'new examinee No.:' + ExamineeNo
            if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                result.Memo = self._lang.LoggingFailed
                return result

            _dbsession.commit()
            result.State = True
        _dbsession.close()
        return result

    def UpdateExaminee(self, ClientHost: str, Token: str, ID: int, Name: str, Contact: str):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif ID <= 0:
            result.Memo = self._lang.WrongID
        elif Name == '':
            result.Memo = self._lang.WrongName
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
                _dbsession.commit()
            except Exception as e:
                result.Memo = str(e)
                _dbsession.rollback()
                return result

            Desc = 'update examinee ID:' + str(ID)
            if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                result.Memo = self._lang.LoggingFailed
                return result

            _dbsession.commit()
            result.State = True
        _dbsession.close()
        return result

    def ExamineeList(self, Token: str, Page: int, PageSize: int, Stext: str, ClassID: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: ResultList = self._examineeModel.List(_dbsession, Page, PageSize, Stext, ClassID)
        _dbsession.close()
        return result

    def ExamineeInfo(self, Token: str, ID: int):
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
            ExamineeData: ExamineeEntity = self._examineeModel.Find(_dbsession, ID)
            if ExamineeData is None:
                result.Memo = self._lang.ExamineeDataError
            else:
                result.State = True
                result.Data = ExamineeData
        _dbsession.close()
        return result

    def Examinees(self, Token: str):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: Result = self._examineeModel.Examinees(_dbsession)
        _dbsession.close()
        return result