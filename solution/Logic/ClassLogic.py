# -*- coding:utf-8 -*-
from Logic.BaseLogic import *


class ClassLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewClass(self, ClientHost: str, Token: str, ClassName: str, Description: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif ClassName == '':
            result.Memo = self._lang.WrongClassName
        elif self._classModel.FindClassCode(_dbsession, ClassName) is not None:
            result.Memo = self._lang.ClassDataAlreadyExists
        else:
            _dbsession.begin_nested()

            ClassData = ClassEntity()
            ClassData.ClassName = ClassName
            ClassData.Description = Description

            AddInfo: Result = self._classModel.Insert(_dbsession, ClassData)
            if AddInfo.State == False:
                result.Memo = AddInfo.Memo
                return result

            Desc = 'new class name:' + ClassName
            if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                result.Memo = self._lang.LoggingFailed
                return result

            _dbsession.commit()
            _dbsession.close()
            result.State = True

        return result

    def UpdateClassInfo(self, ClientHost: str, Token: str, ID: int, ClassName: str, Description: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif ID <= 0:
            result.Memo = self._lang.WrongID
        elif ClassName == '':
            result.Memo = self._lang.WrongClassName
        else:
            CheckData: ClassEntity = self._classModel.FindClassCode(_dbsession, ClassName)
            if CheckData is not None and CheckData.ID != ID:
                result.Memo = self._lang.ClassDataAlreadyExists
                return result
            ClassData: ClassEntity = self._classModel.Find(_dbsession, ID)
            if ClassData is None:
                result.Memo = self._lang.ClassDataError
                return result

            if ClassData.ClassName != ClassName:
                ClassData.ClassCode = self._common.StrMD5(ClassName)

            if Description == '':
                Description = 'none'

            _dbsession.begin_nested()

            try:
                ClassData.ClassName = ClassName
                ClassData.Description = Description
                _dbsession.commit()
            except Exception as e:
                result.Memo = str(e)
                _dbsession.rollback()
                return result

            Desc = 'update class ID:' + str(ID)
            if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                result.Memo = self._lang.LoggingFailed
                return result

            _dbsession.commit()
            _dbsession.close()
            result.State = True
        return result

    def ClassList(self, Token: str, Page: int, PageSize: int, Stext: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: ResultList = self._classModel.List(_dbsession, Page, PageSize, Stext)
        _dbsession.close()
        return result

    def ClassInfo(self, Token: str, ID: int) -> Result:
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
            ClassData: ClassEntity = self._classModel.Find(_dbsession, ID)
            if ClassData is None:
                result.Memo = self._lang.ClassDataError
            else:
                result.State = True
                result.Data = ClassData
        _dbsession.close()
        return result

    def Classes(self, Token: str) -> ResultList:
        result = ResultList()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: ResultList = self._classModel.Classes(_dbsession)
        _dbsession.close()
        return result