# -*- coding:utf-8 -*-
from Logic.BaseLogic import *


class TeacherClassLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewTeacherClass(self, ClientHost: str, Token: str, TeacherID: int, ClassID: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif TeacherID <= 0:
            result.Memo = self._lang.WrongTeacherID
        elif ClassID <= 0:
            result.Memo = self._lang.WrongClassID
        elif self._teacherModel.Find(_dbsession, TeacherID) is None:
            result.Memo = self._lang.TeacherDataError
        elif self._classModel.Find(_dbsession, ClassID) is None:
            result.Memo = self._lang.ClassDataError
        elif self._teacherClassModel.CheckData(_dbsession, TeacherID, ClassID) is not None:
            result.Memo = self._lang.TeackerClassDataAlreadyExists
        else:
            _dbsession.begin_nested()

            TeacherClassData = TeacherClassEntity()
            TeacherClassData.TeacherID = TeacherID
            TeacherClassData.ClassID = ClassID
            AddInfo: Result = self._teacherClassModel.Insert(_dbsession, TeacherClassData)
            if AddInfo.State == False:
                result.Memo = AddInfo.Memo
                return result

            Desc = 'new teacher-class data ID:' + str(AddInfo.Data)
            if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                result.Memo = self._lang.LoggingFailed
                return result

            _dbsession.commit()
            result.State = True
        _dbsession.close()
        return result

    def DeleteTeacherClass(self, ClientHost: str, Token: str, ID: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif ID <= 0:
            result.Memo = self._lang.WrongID
        elif self._teacherClassModel.Find(_dbsession, ID) is None:
            result.Memo = self._lang.NoData
        else:
            _dbsession.begin_nested()

            DelInfo: Result = self._teacherClassModel.Delete(_dbsession, ID)
            if DelInfo.State == False:
                result.Memo = DelInfo.Memo
                return result

            Desc = 'delete teacher-class data ID:' + str(ID)
            if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                result.Memo = self._lang.LoggingFailed
                return result

            _dbsession.commit()
            result.State = True
        _dbsession.close()
        return result

    def TeacherClassList(self, Token: str, Page: int, PageSize: int, TeacherID: int, ClassID: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: ResultList = self._teacherClassModel.List(_dbsession, Page, PageSize, TeacherID, ClassID)
        _dbsession.close()
        return result

    def Teachers(self, Token: str, ClassID: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            TempResult: Result = self._teacherClassModel.Teachers(_dbsession, ClassID)
            DataList = []
            for obj in TempResult.Data:
                TeacherData: ClassModel = self._teacherModel.Find(_dbsession, obj.TeacherID)
                DataList.append(TeacherData)
            result.State = True
            result.Memo = ''
            result.Data = DataList
        _dbsession.close()
        return result

    def Classes(self, Token: str, TeacherID: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            TempResult: Result = self._teacherClassModel.Classes(_dbsession, TeacherID)
            DataList = []
            for obj in TempResult.Data:
                ClassData: ClassModel = self._classModel.Find(_dbsession, obj.ClassID)
                DataList.append(ClassData)
            result.State = True
            result.Memo = ''
            result.Data = DataList
        _dbsession.close()
        return result