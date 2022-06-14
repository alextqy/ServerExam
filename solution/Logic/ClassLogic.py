from Logic.BaseLogic import *


class ClassLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewClass(self, ClientHost: str, Token: str, ClassName: str, Description: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif ClassName == '':
            result.Memo = 'wrong class name'
        elif self._classModel.FindName(_dbsession, ClassName) is not None:
            result.Memo = 'class data already exists'
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
                result.Memo = 'logging failed'
                return result

            _dbsession.commit()
            result.State = True

        return result

    def UpdateClassInfo(self, ClientHost: str, Token: str, ID: int, ClassName: str, Description: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif ID <= 0:
            result.Memo = 'wrong ID'
        elif ClassName == '':
            result.Memo = 'wrong class name'
        else:
            CheckData: ClassEntity = self._classModel.FindName(_dbsession, ClassName)
            if CheckData is not None and CheckData.ID != ID:
                result.Memo = 'class data already exists'
                return result
            ClassData: ClassEntity = self._classModel.Find(_dbsession, ID)
            if ClassData is None:
                result.Memo = 'class data error'
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
                result.Memo = 'logging failed'
                return result

            _dbsession.commit()
            result.State = True
        return result

    def ClassList(self, Token: str, Page: int, PageSize: int, Stext: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        else:
            result: ResultList = self._classModel.List(_dbsession, Page, PageSize, Stext)
        return result

    def ClassInfo(self, Token: str, ID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif ID <= 0:
            result.Memo = 'wrong ID'
        else:
            ClassData: ClassEntity = self._classModel.Find(_dbsession, ID)
            if ClassData is None:
                result.Memo = 'class data error'
            else:
                result.State = True
                result.Data = ClassData
        return result