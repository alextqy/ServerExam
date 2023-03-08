# -*- coding:utf-8 -*-
from Logic.BaseLogic import *


class PaperRuleLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewPaperRule(self, ClientHost: str, Token: str, HeadlineID: int, QuestionType: int, KnowledgeID: int, QuestionNum: int, SingleScore: float, PaperID: int, SerialNumber: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif PaperID <= 0:
            result.Memo = self._lang.WrongPaperID
        elif SerialNumber <= 0:
            result.Memo = self._lang.WrongSerialNumber
        elif HeadlineID > 0 and KnowledgeID > 0:
            result.Memo = self._lang.WrongData
        elif HeadlineID == 0 and KnowledgeID == 0:
            result.Memo = self._lang.WrongData
        else:
            PaperData: PaperEntity = self._paperModel.Find(_dbsession, PaperID)
            if PaperData is None:
                result.Memo = self._lang.PaperDataError
                return result
            if HeadlineID > 0:
                HeadlineData: HeadlineEntity = self._headlineModel.Find(_dbsession, HeadlineID)
                if HeadlineData is None:
                    result.Memo = self._lang.HeadlineDataError
                    return result
                KnowledgeID = 0
                QuestionType = 0
                QuestionNum = 0
                SingleScore = 0
            if KnowledgeID > 0:
                HeadlineID = 0
                if QuestionType <= 0:
                    result.Memo = self._lang.WrongQuestionType
                    return result
                if QuestionNum <= 0:
                    result.Memo = self._lang.WrongQuestionNum
                    return result
                if SingleScore <= 0:
                    result.Memo = self._lang.WrongSingleScore
                    return result
                SubjectData: SubjectEntity = self._subjectModel.Find(_dbsession, PaperData.SubjectID)
                if SubjectData is None:
                    result.Memo = self._lang.SubjectDataError
                    return result
                KnowledgeData: KnowledgeEntity = self._knowledgeModel.Find(_dbsession, KnowledgeID)
                if KnowledgeData is None:
                    result.Memo = self._lang.KnowledgeDataError
                    return result
                if KnowledgeData.SubjectID != SubjectData.ID:
                    result.Memo = self._lang.KnowledgeIDError
                    return result
                # 是否有相同类型的试题规则
                CheckPaperRule: PaperRuleEntity = self._paperRuleModel.CheckPaperRule(_dbsession, PaperID, KnowledgeData.ID, QuestionType)
                if CheckPaperRule is not None:
                    result.Memo = self._lang.PaperRuleDataAlreadyExists
                    return result
                # 当前题型下是否有足够的试题数量
                CountType: int = self._questionModel.CountType(_dbsession, KnowledgeData.ID, QuestionType)
                if CountType < QuestionNum:
                    result.Memo = self._lang.ThereAreNotEnoughQuestions
                    return result
                # 当前试题规则总分是否超过试卷总分
                CurrentTotalScore: float = SingleScore * QuestionNum
                PaperRuleDataList: list = self._paperRuleModel.FindPaperID(_dbsession, PaperID)
                if len(PaperRuleDataList) > 0:
                    for i in PaperRuleDataList:
                        Data: PaperRuleEntity = i
                        CurrentTotalScore += float(Data.SingleScore) * Data.QuestionNum
                    if CurrentTotalScore > PaperData.TotalScore:
                        result.Memo = self._lang.GreaterThanTheTotalScoreOfTheTestPaper
                        return result

            _dbsession.begin_nested()

            PaperRuleData = PaperRuleEntity()
            PaperRuleData.HeadlineID = HeadlineID
            PaperRuleData.KnowledgeID = KnowledgeID
            PaperRuleData.QuestionType = QuestionType
            PaperRuleData.QuestionNum = QuestionNum
            PaperRuleData.SingleScore = SingleScore
            PaperRuleData.PaperID = PaperID
            PaperRuleData.SerialNumber = SerialNumber
            AddInfo: Result = self._paperRuleModel.Insert(_dbsession, PaperRuleData)
            if AddInfo.State == False:
                result.Memo - AddInfo.Memo
                return result

            try:
                PaperData.PaperState = 2
                PaperRuleData.UpdateTime = self._common.Time()
                _dbsession.commit()
            except Exception as e:
                result.Memo = str(e)
                _dbsession.rollback()
                return result

            Desc = 'new paper rule'
            if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                result.Memo = self._lang.LoggingFailed
                return result

            _dbsession.commit()
            result.State = True
        _dbsession.close()
        return result

    def PaperRuleDisabled(self, ClientHost: str, Token: str, ID: int):
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
            PaperRuleData: PaperRuleEntity = self._paperRuleModel.Find(_dbsession, ID)
            if PaperRuleData is None:
                result.Memo = self._lang.PaperRuleDataError
                return result

            _dbsession.begin_nested()

            try:
                if PaperRuleData.PaperRuleState == 2:
                    PaperRuleData.PaperRuleState = 1
                else:
                    PaperRuleData.PaperRuleState = 2
                PaperRuleData.UpdateTime = self._common.Time()
                _dbsession.commit()
            except Exception as e:
                result.Memo = str(e)
                _dbsession.rollback()
                return result

            PaperData: PaperEntity = self._paperModel.Find(_dbsession, PaperRuleData.PaperID)
            if PaperData is not None:
                try:
                    PaperData.PaperState = 2
                    PaperRuleData.UpdateTime = self._common.Time()
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

            if PaperRuleData.PaperRuleState == 1:
                Desc = 'enable paper rule ID:' + str(ID)
            if PaperRuleData.PaperRuleState == 2:
                Desc = 'disable paper rule ID:' + str(ID)
            if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                result.Memo = self._lang.LoggingFailed
                return result

            _dbsession.commit()
            result.State = True
        _dbsession.close()
        return result

    def PaperRuleDelete(self, ClientHost: str, Token: str, ID: int):
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
            PaperRuleData: PaperRuleEntity = self._paperRuleModel.Find(_dbsession, ID)
            if PaperRuleData is None:
                result.Memo = self._lang.PaperRuleDataError
                return result

            _dbsession.begin_nested()

            DelInfo: Result = self._paperRuleModel.Delete(_dbsession, ID)
            if DelInfo.State == False:
                result.Memo - DelInfo.Memo
                return result

            PaperData: PaperEntity = self._paperModel.Find(_dbsession, PaperRuleData.PaperID)
            if PaperData is not None:
                try:
                    PaperData.PaperState = 2
                    PaperRuleData.UpdateTime = self._common.Time()
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

            Desc = 'delete paper rule ID:' + str(ID)
            if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                result.Memo = self._lang.LoggingFailed
                return result

            _dbsession.commit()
            result.State = True
        _dbsession.close()
        return result

    def PaperRuleList(self, Token: str, Page: int, PageSize: int, PaperID: int, PaperRuleState: int, OrderBySerialNumber: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif PaperID <= 0:
            result.Memo = self._lang.WrongPaperID
        else:
            result: ResultList = self._paperRuleModel.List(_dbsession, Page, PageSize, PaperID, PaperRuleState, OrderBySerialNumber)
        _dbsession.close()
        return result

    def PaperRuleInfo(self, Token: str, ID: int):
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
            PaperRuleData: PaperRuleEntity = self._paperRuleModel.Find(_dbsession, ID)
            if PaperRuleData is None:
                result.Memo = self._lang.PaperRuleDataError
            else:
                result.State = True
                result.Data = PaperRuleData
        _dbsession.close()
        return result

    def PaperRules(self, Token: str, PaperID: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif PaperID <= 0:
            result.Memo = self._lang.WrongPaperID
        else:
            result: Result = self._paperRuleModel.PaperRules(_dbsession, PaperID)
        _dbsession.close()
        return result

    def UpdatePaperRule(self, ClientHost: str, Token: str, ID: int, QuestionType: int, QuestionNum: int, SingleScore: float, SerialNumber: int):
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif ID <= 0:
            result.Memo = self._lang.WrongID
        elif QuestionType <= 0:
            result.Memo = self._lang.WrongQuestionType
        elif QuestionNum <= 0:
            result.Memo = self._lang.WrongQuestionNum
        elif SingleScore <= 0:
            result.Memo = self._lang.WrongSingleScore
        elif SerialNumber <= 0:
            result.Memo = self._lang.WrongSerialNumber
        else:
            PaperRuleData: PaperRuleEntity = self._paperRuleModel.Find(_dbsession, ID)
            if PaperRuleData is None:
                result.Memo = self._lang.PaperRuleDataError
            else:
                _dbsession.begin_nested()

                try:
                    PaperRuleData.QuestionType = QuestionType
                    PaperRuleData.QuestionNum = QuestionNum
                    PaperRuleData.SingleScore = SingleScore
                    PaperRuleData.SerialNumber = SerialNumber
                    PaperRuleData.UpdateTime = self._common.Time()
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                PaperData: PaperEntity = self._paperModel.Find(_dbsession, PaperRuleData.PaperID)
                if PaperData is not None:
                    try:
                        PaperData.PaperState = 2
                        PaperRuleData.UpdateTime = self._common.Time()
                        _dbsession.commit()
                    except Exception as e:
                        result.Memo = str(e)
                        _dbsession.rollback()
                        return result

                Desc = 'update paper rule ID:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result
