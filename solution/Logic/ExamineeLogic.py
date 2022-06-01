from Logic.BaseLogic import *


class ExamineeLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewExaminee(self, ClientHost: str, Token: str, ExamineeNo: str, Name: str, ClassID: int, Contact: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif ExamineeNo == '':
            result.Memo = 'wrong examinee No.'
        elif Name == '':
            result.Memo = 'wrong name'
        elif ClassID <= 0:
            result.Memo = 'wrong class id'
        elif self._examineeModel.FindExamineeNo(_dbsession, ExamineeNo) is not None:
            result.Memo = 'examinee No. data already exists'
        elif self._classModel.Find(_dbsession, ClassID) is None:
            result.Memo = 'class data does not exist'
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
            if self.LogSysAction(_dbsession, 1, 0, Desc, ClientHost) == False:
                result.Memo = 'logging failed'
                return result

            _dbsession.commit()
            result.State = True
        return result

    def UpdateExaminee(self, ClientHost: str, Token: str, ID: int, Name: str, Contact: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif ID <= 0:
            result.Memo = 'wrong id'
        elif Name == '':
            result.Memo = 'wrong name'
        else:
            if Contact == '':
                Contact = 'none'

            ExamineeData: ExamineeEntity = self._examineeModel.Find(_dbsession, ID)
            if ExamineeData is None:
                result.Memo = 'examinee data error'
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

            Desc = 'update examinee id:' + str(ID)
            if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                result.Memo = 'logging failed'
                return result

            _dbsession.commit()
            result.State = True
        return result

    def ExamineeList(self, Token: str, Page: int, PageSize: int, Stext: str, ClassID: int) -> ResultList:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        else:
            result: ResultList = self._examineeModel.List(_dbsession, Page, PageSize, Stext, ClassID)
        return result

    def ExamineeInfo(self, Token: str, ID: int) -> Result:
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
            ExamineeData: ExamineeEntity = self._examineeModel.Find(_dbsession, ID)
            if ExamineeData is None:
                result.Memo = 'examinee data error'
            else:
                result.State = True
                result.Data = ExamineeData
        return result