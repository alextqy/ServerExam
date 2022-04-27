from Logic.BaseLogic import *


class ExamineeLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewExaminee(self, Name: str, ExamineeNo: str, Contact: str) -> Result:
        _dbsession = DBsession()
        _dbsession.begin_nested()
        Result = self._examineemodel.Insert(_dbsession, Name, ExamineeNo, Contact)
        _dbsession.commit()
        return Result

    def DeleteExaminee(self, ID: int) -> Result:
        _dbsession = DBsession()
        _dbsession.begin_nested()
        Result = self._examineemodel.Delete(_dbsession, ID)
        _dbsession.commit()
        return Result

    def UpdateExaminee(self, ID: int, Name: str, ExamineeNo: str, Contact: str) -> Result:
        _dbsession = DBsession()
        _dbsession.begin_nested()
        Result = self._examineemodel.Update(_dbsession, ID, Name, ExamineeNo, Contact)
        _dbsession.commit()
        return Result

    def FindExaminee(self, ID: int) -> Result:
        _dbsession = DBsession()
        Result = self._examineemodel.Find(_dbsession, ID)
        return Result

    def ListExaminee(self, Page: int, PageSize: int, Stext: str) -> Result:
        _dbsession = DBsession()
        Result = self._examineemodel.List(_dbsession, Page, PageSize, Stext)
        return Result