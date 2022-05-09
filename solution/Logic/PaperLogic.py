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
                Desc = 'new paper:' + PaperName
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result
                PaperData = PaperEntity()
                PaperData.PaperName = PaperName
                PaperData.SubjectID = SubjectID
                PaperData.TotalScore = TotalScore
                PaperData.PassLine = PassLine
                PaperData.ExamDuration = ExamDuration
                result: Result = self._paperModel.Insert(_dbsession, PaperData)
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
                Desc = 'disable/enable paper id:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result
                try:
                    if PaperData.PaperState == 2:
                        PaperData.PaperState = 1
                    else:
                        PaperData.PaperState = 2
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result
                result.Status = True
                result: Result = self._paperModel.Update(_dbsession, ID, PaperData)
        return result