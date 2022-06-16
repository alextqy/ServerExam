from Logic.BaseLogic import *


class ScantronSolutionLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def ScantronSolutionList(self, Token: str, Page: int, PageSize: int, ScantronID: int, Position: int) -> ResultList:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: ResultList = self._scantronSolutionModel.List(_dbsession, Page, PageSize, ScantronID, Position)
        return result

    def ScantronSolutionInfo(self, Token: str, ID: int) -> Result:
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
            ExamInfoData: ExamInfoEntity = self._scantronSolutionModel.Find(_dbsession, ID)
            if ExamInfoData is None:
                result.Memo = self._lang.ScantronSolutionDataError
            else:
                result.State = True
                result.Data = ExamInfoData
        return result