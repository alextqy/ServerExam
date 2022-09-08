# -*- coding:utf-8 -*-
from Logic.BaseLogic import *


class PaperLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewPaper(self, ClientHost: str, Token: str, PaperName: str, SubjectID: int, TotalScore: float, PassLine: float, ExamDuration: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif PaperName == '':
            result.Memo = self._lang.WrongPaperName
        elif SubjectID <= 0:
            result.Memo = self._lang.WrongSubjectID
        elif TotalScore <= 0:
            result.Memo = self._lang.WrongTotalScore
        elif PassLine <= 0:
            result.Memo = self._lang.WrongPassLine
        elif PassLine > TotalScore:
            result.Memo = self._lang.WrongPassLine
        elif ExamDuration <= 0:
            result.Memo = self._lang.WrongExamDuration
        elif self._paperModel.FindPaperCode(_dbsession, PaperName) is not None:
            result.Memo = self._lang.PaperDataAlreadyExists
        else:
            SubjectData: SubjectEntity = self._subjectModel.Find(_dbsession, SubjectID)
            if SubjectData is None:
                result.Memo = self._lang.SubjectDataError
            else:
                _dbsession.begin_nested()

                PaperData = PaperEntity()
                PaperData.PaperName = PaperName
                PaperData.SubjectID = SubjectID
                PaperData.TotalScore = TotalScore
                PaperData.PassLine = PassLine
                PaperData.ExamDuration = ExamDuration
                AddInfo: Result = self._paperModel.Insert(_dbsession, PaperData)
                if AddInfo.State == False:
                    result.Memo - AddInfo.Memo
                    return result

                Desc = 'new paper:' + PaperName
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result

    def PaperDisabled(self, ClientHost: str, Token: str, ID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            PaperData: PaperEntity = self._paperModel.Find(_dbsession, ID)
            if PaperData is None:
                result.Memo = self._lang.PaperDataError
            else:
                _dbsession.begin_nested()

                try:
                    if PaperData.PaperState == 2:
                        # 当前试卷下是否有对应的试卷规则
                        PaperRuleList: list = self._paperRuleModel.FindPaperID(_dbsession, ID)
                        if len(PaperRuleList) == 0:
                            result.Memo = self._lang.PaperRuleDataDoesNotExist
                            _dbsession.rollback()
                            return result
                        # 当前试卷下的试卷规则是否和当前试卷总分相匹配
                        if len(PaperRuleList) > 0:
                            TotalScore: float = 0
                            for i in PaperRuleList:
                                PaperRuleData: PaperRuleEntity = i
                                TotalScore += float(PaperRuleData.SingleScore) * PaperRuleData.QuestionNum
                            if TotalScore != PaperData.TotalScore:
                                result.Memo = self._lang.ScoreIsSetIncorrectly
                                _dbsession.rollback()
                                return result
                        # 当前科目只能有一个试卷被启用
                        PaperList: list = self._paperModel.SubjectPaper(_dbsession, PaperData.SubjectID)
                        if len(PaperList) > 0:
                            for i in PaperList:
                                Data: PaperEntity = i
                                Data.PaperState = 2
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
                    Desc = 'enable paper ID:' + str(ID)
                if PaperData.PaperState == 2:
                    Desc = 'disable paper ID:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result

    def UpdatePaperInfo(self, ClientHost: str, Token: str, ID: int, PaperName: str, TotalScore: float, PassLine: float, ExamDuration: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif ID <= 0:
            result.Memo = self._lang.WrongID
        elif PaperName == '':
            result.Memo = self._lang.WrongPaperName
        elif TotalScore <= 0:
            result.Memo = self._lang.WrongTotalScore
        elif PassLine <= 0:
            result.Memo = self._lang.WrongPassLine
        elif ExamDuration <= 0:
            result.Memo = self._lang.WrongExamDuration
        else:
            PaperData: PaperEntity = self._paperModel.Find(_dbsession, ID)
            if PaperData is None:
                result.Memo = self._lang.PaperDataError
            else:
                if PaperData.PaperName != PaperName:
                    PaperData.PaperCode = self._common.StrMD5(PaperName)

                _dbsession.begin_nested()

                try:
                    PaperData.PaperName = PaperName
                    PaperData.TotalScore = TotalScore
                    PaperData.PassLine = PassLine
                    PaperData.ExamDuration = ExamDuration
                    PaperData.UpdateTime = self._common.Time()
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                Desc = 'update paper ID:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result

    def PaperList(self, Token: str, Page: int, PageSize: int, Stext: str, SubjectID: int, PaperState: int) -> ResultList:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: ResultList = self._paperModel.List(_dbsession, Page, PageSize, Stext, SubjectID, PaperState)
        _dbsession.close()
        return result

    def PaperInfo(self, Token: str, ID: int) -> Result:
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
            PaperData: PaperEntity = self._paperModel.Find(_dbsession, ID)
            if PaperData is None:
                result.Memo = self._lang.PaperDataError
            else:
                result.State = True
                result.Data = PaperData
        _dbsession.close()
        return result