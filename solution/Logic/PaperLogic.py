from Logic.BaseLogic import *


class PaperLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewPaper(self, ClientHost: str, Token: str, PaperName: str, SubjectID: int, TotalScore: float, PassLine: float, ExamDuration: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif PaperName == '':
            result.Memo = 'wrong paper name'
        elif SubjectID <= 0:
            result.Memo = 'wrong subject id'
        elif TotalScore <= 0:
            result.Memo = 'wrong total score'
        elif PassLine <= 0:
            result.Memo = 'wrong pass line'
        elif PassLine > TotalScore:
            result.Memo = 'wrong pass line'
        elif ExamDuration <= 0:
            result.Memo = 'wrong exam duration'
        elif self._paperModel.FindPaperCode(_dbsession, PaperName) is not None:
            result.Memo = 'data already exists'
        else:
            SubjectData: SubjectEntity = self._subjectModel.Find(_dbsession, SubjectID)
            if SubjectData is None:
                result.Memo = 'subject data error'
            elif SubjectData.SubjectState != 1:
                result.Memo = 'subject data error'
            else:
                _dbsession.begin_nested()

                PaperData = PaperEntity()
                PaperData.PaperName = PaperName
                PaperData.SubjectID = SubjectID
                PaperData.TotalScore = TotalScore
                PaperData.PassLine = PassLine
                PaperData.ExamDuration = ExamDuration
                AddInfo: Result = self._paperModel.Insert(_dbsession, PaperData)
                if AddInfo.Status == False:
                    result.Memo - AddInfo.Memo
                    return result

                Desc = 'new paper:' + PaperName
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result

                _dbsession.commit()
                result.Status = True
        return result

    def PaperDisabled(self, ClientHost: str, Token: str, ID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        else:
            PaperData: PaperEntity = self._paperModel.Find(_dbsession, ID)
            if PaperData is None:
                result.Memo = 'data error'
            else:
                _dbsession.begin_nested()

                try:
                    if PaperData.PaperState == 2:
                        PaperData.PaperState = 1
                    else:
                        PaperData.PaperState = 2
                    PaperData.UpdateTime = self._common.Time()
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                if PaperData.PaperState == 1:
                    Desc = 'enable paper id:' + str(ID)
                if PaperData.PaperState == 2:
                    Desc = 'disable paper id:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result

                _dbsession.commit()
                result.Status = True
        return result

    def UpdatePaperInfo(self, ClientHost: str, Token: str, ID: int, PaperName: str, TotalScore: float, PassLine: float, ExamDuration: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif ID <= 0:
            result.Memo = 'wrong id'
        elif PaperName == '':
            result.Memo = 'wrong paper name'
        elif TotalScore <= 0:
            result.Memo = 'wrong total score'
        elif PassLine <= 0:
            result.Memo = 'wrong pass line'
        elif ExamDuration <= 0:
            result.Memo = 'wrong exam duration'
        else:
            PaperData: PaperEntity = self._paperModel.Find(_dbsession, ID)
            if PaperData is None:
                result.Memo = 'data error'
            else:
                _dbsession.begin_nested()

                try:
                    PaperData.PaperName = PaperName
                    PaperData.TotalScore = TotalScore
                    PaperData.PassLine = PassLine
                    PaperData.ExamDuration = ExamDuration * 60
                    PaperData.UpdateTime = self._common.Time()
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                Desc = 'update paper id:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result

                _dbsession.commit()
                result.Status = True
        return result

    def PaperList(self, Token: str, Page: int, PageSize: int, Stext: str, SubjectID: int, PaperState: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        else:
            result: ResultList = self._paperModel.List(_dbsession, Page, PageSize, Stext, SubjectID, PaperState)
        return result

    def PaperInfo(self, Token: str, ID: int) -> Result:
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
            PaperData: PaperEntity = self._paperModel.Find(_dbsession, ID)
            if PaperData is None:
                result.Memo = 'data error'
            else:
                result.Status = True
                result.Data = PaperData
        return result