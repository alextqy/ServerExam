# -*- coding:utf-8 -*-
from Logic.BaseLogic import *


class ExamInfoLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewExamInfo(self, ClientHost: str, Token: str, SubjectName: str, ExamNo: str, ExamineeID: int, ExamType: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif SubjectName == '':
            result.Memo = self._lang.WrongSubjectName
        elif ExamNo == '':
            result.Memo = self._lang.WrongExamNo
        elif ExamType <= 0:
            result.Memo = self._lang.WrongExamType
        else:
            SubjectData: SubjectEntity = self._subjectModel.FindSubjectCode(_dbsession, SubjectName)
            if SubjectData is None:
                result.Memo = self._lang.SubjectDataError
            elif SubjectData.SubjectState == 2:
                result.Memo = self._lang.SubjectDataIsDisabled
            else:
                if ExamineeID > 0:
                    # 考生信息是否存在
                    if self._examineeModel.Find(_dbsession, ExamineeID) is None:
                        result.Memo = self._lang.ExamineeDataDoesNotExist
                        return result
                    # 该考生是否有相同科目的报名且未考试
                    CheckData: ExamInfoEntity = self._examInfoModel.CheckExam(_dbsession, ExamineeID, SubjectName, ExamType)
                    if CheckData is not None:
                        if CheckData.ExamState < 3:
                            result.Memo = self._lang.AlreadyRegisteredForTheSameSubject
                            return result

                CheckExamNo: ExamInfoEntity = self._examInfoModel.FindExamNo(_dbsession, ExamNo)
                if CheckExamNo is not None and CheckExamNo.ExamState != 4:
                    result.Memo = self._lang.ExamNoDataAlreadyExists
                    return result

                _dbsession.begin_nested()

                ExamInfoData = ExamInfoEntity()
                ExamInfoData.SubjectName = SubjectName
                ExamInfoData.ExamNo = ExamNo
                ExamInfoData.ExamineeID = ExamineeID
                ExamInfoData.ExamType = ExamType
                AddInfo: Result = self._examInfoModel.Insert(_dbsession, ExamInfoData)
                if AddInfo.State == False:
                    result.Memo = AddInfo.Memo
                    return result

                Desc = 'new exam No.:' + ExamNo
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result

    def ExamInfoDisabled(self, ClientHost: str, Token: str, ID: int) -> Result:
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
            ExamInfoData: ExamInfoEntity = self._examInfoModel.Find(_dbsession, ID)
            if ExamInfoData is None:
                result.Memo = self._lang.ExamDataError
            elif ExamInfoData.ExamState == 4:
                result.State = True
            elif ExamInfoData.ExamState == 3:
                result.Memo = self._lang.ExamCompleted
            elif ExamInfoData.StartTime > 0:
                result.Memo = self._lang.DataCannotBeInvalidated
            else:
                _dbsession.begin_nested()

                # 待考状态的报名 作废时要删除对应的答题卡和答题卡选项
                if ExamInfoData.ExamState == 2:
                    ScantronDataList: list = self._scantronModel.FindExamID(_dbsession, ID)
                    if len(ScantronDataList) > 0:
                        for i in ScantronDataList:
                            ScantronData: ScantronEntity = i
                            # 删除答题卡选项
                            ScantronSolutionDataList: list = self._scantronSolutionModel.FindScantronID(_dbsession, ScantronData.ID)
                            if len(ScantronSolutionDataList) > 0:
                                for j in ScantronSolutionDataList:
                                    ScantronSolutionData: ScantronSolutionEntity = j
                                    SSDelInfo: Result = self._scantronSolutionModel.Delete(_dbsession, ScantronSolutionData.ID)
                                    if SSDelInfo.State == False:
                                        result.Memo = SSDelInfo.Memo
                                        _dbsession.rollback()
                                        return result
                            # 删除答题卡
                            SDelInfo: Result = self._scantronModel.Delete(_dbsession, ScantronData.ID)
                            if SDelInfo.State == False:
                                result.Memo = SDelInfo.Memo
                                return result
                try:
                    ExamInfoData.ExamState = 4
                    ExamInfoData.UpdateTime = self._common.Time()
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                Desc = 'disable exam No.:' + ExamInfoData.ExamNo
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result

    def ExamInfoList(self, Token: str, Page: int, PageSize: int, Stext: str, ExamState: int, ExamType: int, Pass: int) -> ResultList:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: ResultList = self._examInfoModel.List(_dbsession, Page, PageSize, Stext, ExamState, ExamType, Pass)
        _dbsession.close()
        return result

    def ExamInfo(self, Token: str, ID: int) -> Result:
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
            ExamInfoData: ExamInfoEntity = self._examInfoModel.Find(_dbsession, ID)
            if ExamInfoData is None:
                result.Memo = self._lang.ExamDataError
            else:
                result.State = True
                result.Data = ExamInfoData
        _dbsession.close()
        return result

    def GenerateTestPaper(self, ClientHost: str, Token: str, ID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result = self.GenerateTestPaperAction(ClientHost, ID, AdminID)
        _dbsession.close()
        return result

    def GenerateTestPaperAction(self, ClientHost: str, ID: int, AdminID: int = 0) -> Result:
        result = Result()
        _dbsession = DBsession()
        ExamInfoData: ExamInfoEntity = self._examInfoModel.Find(_dbsession, ID)
        if ID <= 0:
            result.Memo = self._lang.WrongID
        elif ExamInfoData is None:
            result.Memo = self._lang.ExamDataDoesNotExist
        elif ExamInfoData.ExamState == 2:  # 已有试题
            result.Memo = self._lang.QuestionDataAlreadyExists
        elif ExamInfoData.ExamState == 3:  # 考试已完成
            result.Memo = self._lang.ExamCompleted
        elif ExamInfoData.ExamState == 4:  # 报名已禁用
            result.Memo = self._lang.ExamDataDisabled
        elif ExamInfoData.ExamineeID > 0 and self._examineeModel.Find(_dbsession, ExamInfoData.ExamineeID) is None:  # 考生不存在
            result.Memo = self._lang.ExamineeDataDoesNotExist
        else:
            # 科目数据
            SubjectData: SubjectEntity = self._subjectModel.FindSubjectCode(_dbsession, ExamInfoData.SubjectName)
            if SubjectData is None:
                result.Memo = self._lang.SubjectDataDoesNotExist
            else:
                # 获取当前科目下的有效试卷
                PaperData: PaperEntity = self._paperModel.FindSubjectPaper(_dbsession, SubjectData.ID)
                if PaperData is None:
                    result.Memo = self._lang.PaperDataDoesNotExist
                else:
                    # 获取当前试卷下所有有效试卷规则
                    PaperRuleListData: list = self._paperRuleModel.FindPaperID(_dbsession, PaperData.ID)
                    if len(PaperRuleListData) == 0:
                        result.Memo = self._lang.PaperDataDoesNotExist
                    else:
                        _dbsession.begin_nested()

                        # 遍历试卷规则
                        for i in PaperRuleListData:
                            PaperRuleData: PaperRuleEntity = i

                            # 解析大标题数据 ===============================================================================
                            if PaperRuleData.HeadlineID > 0:
                                HeadlineData: HeadlineEntity = self._headlineModel.Find(_dbsession, PaperRuleData.HeadlineID)
                                if HeadlineData is None:
                                    result.Memo = self._lang.HeadlineDataError
                                    _dbsession.rollback()
                                    return result
                                if HeadlineData.Content == '':
                                    result.Memo = self._lang.HeadlineDataError
                                    _dbsession.rollback()
                                    return result
                                # 写入答题卡信息
                                ScantronData = ScantronEntity()
                                ScantronData.HeadlineContent = HeadlineData.Content
                                ScantronData.ExamID = ID
                                AddInfo: Result = self._scantronModel.Insert(_dbsession, ScantronData)
                                if AddInfo.State == False:
                                    result.Memo = AddInfo.Memo
                                    return result

                            # 解析试卷数据 ===============================================================================
                            if PaperRuleData.KnowledgeID > 0:
                                if PaperRuleData.QuestionType == 0 or PaperRuleData.QuestionNum == 0 or PaperRuleData.SingleScore == 0:
                                    result.Memo = self._lang.ExamPaperRulesError
                                    _dbsession.rollback()
                                    return result
                                # 获取该知识点下对应类型的试题数据
                                QuestionDataList: list = self._questionModel.PaperRuleQuestion(_dbsession, PaperRuleData.KnowledgeID, PaperRuleData.QuestionType)
                                if len(QuestionDataList) < PaperRuleData.QuestionNum:
                                    result.Memo = self._lang.NotEnoughQuestions
                                    _dbsession.rollback()
                                    return result
                                # 试题数量和抽题数量相同 则全部放入答题卡
                                if len(QuestionDataList) == PaperRuleData.QuestionNum:
                                    ScantronDataList: list = QuestionDataList
                                # 试题数量大于抽题数量相同 则随机放入答题卡
                                if len(QuestionDataList) > PaperRuleData.QuestionNum:
                                    ScantronDataList: list = self._common.RandomDrawSample(QuestionDataList, PaperRuleData.QuestionNum)
                                # 遍历写入答题卡数据
                                for j in ScantronDataList:
                                    QuestionData: QuestionEntity = j
                                    ScantronData = ScantronEntity()
                                    ScantronData.QuestionTitle = QuestionData.QuestionTitle
                                    ScantronData.QuestionCode = QuestionData.QuestionCode
                                    ScantronData.QuestionType = QuestionData.QuestionType
                                    ScantronData.KnowledgeID = QuestionData.KnowledgeID
                                    ScantronData.Score = PaperRuleData.SingleScore
                                    ScantronData.Marking = QuestionData.Marking
                                    ScantronData.Description = QuestionData.Description
                                    ScantronData.Attachment = QuestionData.Attachment
                                    ScantronData.ExamID = ID
                                    AddInfo: Result = self._scantronModel.Insert(_dbsession, ScantronData)
                                    if AddInfo.State == False:
                                        result.Memo = AddInfo.Memo
                                        return result
                                    # 遍历写入答题卡选项数据
                                    QuestionSolutionDataList: list = self._questionSolutionModel.FindQuestionID(_dbsession, QuestionData.ID)
                                    if len(QuestionSolutionDataList) == 0:
                                        result.Memo = self._lang.WrongQuestionOptions
                                        _dbsession.rollback()
                                        return result
                                    for k in QuestionSolutionDataList:
                                        QuestionSolutionData: QuestionSolutionEntity = k
                                        ScantronSolutionData = ScantronSolutionEntity()
                                        ScantronSolutionData.ScantronID = ScantronData.ID
                                        ScantronSolutionData.Option = QuestionSolutionData.Option
                                        ScantronSolutionData.OptionAttachment = QuestionSolutionData.OptionAttachment
                                        ScantronSolutionData.CorrectAnswer = QuestionSolutionData.CorrectAnswer
                                        ScantronSolutionData.CorrectItem = QuestionSolutionData.CorrectItem
                                        ScantronSolutionData.ScoreRatio = QuestionSolutionData.ScoreRatio
                                        ScantronSolutionData.Position = QuestionSolutionData.Position
                                        AddInfo: Result = self._scantronSolutionModel.Insert(_dbsession, ScantronSolutionData)
                                        if AddInfo.State == False:
                                            result.Memo = AddInfo.Memo
                                            return result

                        ExamInfoData.TotalScore = PaperData.TotalScore
                        ExamInfoData.PassLine = PaperData.PassLine
                        ExamInfoData.ExamDuration = PaperData.ExamDuration
                        ExamInfoData.ExamState = 2  # 报名状态改为待考

                        Desc = 'generate test paper exam No.:' + str(ExamInfoData.ID)
                        if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                            result.Memo = self._lang.LoggingFailed
                            return result

                        _dbsession.commit()
                        result.State = True
        _dbsession.close()
        return result

    def ResetExamQuestionData(self, ClientHost: str, Token: str, ID: int) -> Result:
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
            # 获取报名数据
            ExamInfoData: ExamInfoEntity = self._examInfoModel.Find(_dbsession, ID)
            if ExamInfoData is None:
                result.Memo = self._lang.ExamDataError
            elif ExamInfoData.StartTime > 0:
                result.Memo = self._lang.ExamHasStarted
            elif ExamInfoData.ExamState == 3:
                result.Memo = self._lang.ExamCompleted
            elif ExamInfoData.ExamState == 4:
                result.Memo = self._lang.ExamDataDisabled
            else:
                _dbsession.begin_nested()

                # 获取对应答题卡列表数据
                if ExamInfoData.ExamState == 2:
                    ScantronDataList: list = self._scantronModel.FindExamID(_dbsession, ID)
                    if len(ScantronDataList) > 0:
                        for i in ScantronDataList:
                            ScantronData: ScantronEntity = i
                            # 删除答题卡选项
                            ScantronSolutionDataList: list = self._scantronSolutionModel.FindScantronID(_dbsession, ScantronData.ID)
                            if len(ScantronSolutionDataList) > 0:
                                for j in ScantronSolutionDataList:
                                    ScantronSolutionData: ScantronSolutionEntity = j
                                    SSDelInfo: Result = self._scantronSolutionModel.Delete(_dbsession, ScantronSolutionData.ID)
                                    if SSDelInfo.State == False:
                                        result.Memo = SSDelInfo.Memo
                                        return result
                            # 删除答题卡
                            SDelInfo: Result = self._scantronModel.Delete(_dbsession, ScantronData.ID)
                            if SDelInfo.State == False:
                                result.Memo = SDelInfo.Memo
                                return result

                try:
                    ExamInfoData.ExamState = 1
                    ExamInfoData.ExamDuration = 0
                    ExamInfoData.PassLine = 0
                    ExamInfoData.TotalScore = 0
                    ExamInfoData.UpdateTime = self._common.Time()
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                Desc = 'reset exam No.:' + ExamInfoData.ExamNo
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result

    def ExamIntoHistory(self, ClientHost: str, Token: str, ID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result = self.ExamIntoHistoryAction(ClientHost, ID, AdminID)
        _dbsession.close()
        return result

    def ExamIntoHistoryAction(self, ClientHost: str, ID: int, AdminID: int = 0) -> Result:
        result = Result()
        _dbsession = DBsession()
        ExamInfoData: ExamInfoEntity = self._examInfoModel.Find(_dbsession, ID)
        if ExamInfoData is None:
            result.Memo = self._lang.ExamDataDoesNotExist
        elif ID <= 0:
            result.Memo = self._lang.WrongID
        else:
            _dbsession.begin_nested()

            ExamInfoData: ExamInfoEntity = self._examInfoModel.Find(_dbsession, ID)
            if ExamInfoData is None:
                result.Memo = self._lang.ExamDataDoesNotExist
            elif ExamInfoData.ExamState == 2 and self._common.Time() <= ExamInfoData.EndTime:
                result.Memo = 'ID:' + str(ID) + self._lang.HasNotYetTakenTheExam
            else:
                # 获取报名下的答题卡
                ScantronDataList: list = self._scantronModel.FindExamID(_dbsession, ID)
                if len(ScantronDataList) > 0:
                    for i in ScantronDataList:
                        ScantronData: ScantronEntity = i

                        # 当前报名下的答题卡转入历史
                        ScantronHistoryData = ScantronHistoryEntity()
                        ScantronHistoryData.QuestionTitle = ScantronData.QuestionTitle
                        ScantronHistoryData.QuestionCode = ScantronData.QuestionCode
                        ScantronHistoryData.QuestionType = ScantronData.QuestionType
                        ScantronHistoryData.Marking = ScantronData.Marking
                        ScantronHistoryData.KnowledgeID = ScantronData.KnowledgeID
                        ScantronHistoryData.Description = ScantronData.Description
                        ScantronHistoryData.Attachment = ScantronData.Attachment
                        ScantronHistoryData.Score = ScantronData.Score
                        ScantronHistoryData.ExamID = ScantronData.ExamID
                        ScantronHistoryData.HeadlineContent = ScantronData.HeadlineContent
                        AddInfo: Result = self._scantronHistoryModel.Insert(_dbsession, ScantronHistoryData)
                        if AddInfo.State == False:
                            result.Memo = AddInfo.Memo
                            return result

                        # 当前报名下的答题卡选项转入历史
                        ScantronSolutionDataList: list = self._scantronSolutionModel.FindScantronID(_dbsession, ScantronData.ID)
                        if len(ScantronSolutionDataList) > 0:
                            for s in ScantronSolutionDataList:
                                ScantronSolutionData: ScantronSolutionEntity = s

                                # 当前答题卡选项转入历史
                                ScantronSolutionHistoryData = ScantronSolutionHistoryEntity()
                                ScantronSolutionHistoryData.ScantronHistoryID = ScantronHistoryData.ID
                                ScantronSolutionHistoryData.Option = ScantronSolutionData.Option
                                ScantronSolutionHistoryData.OptionAttachment = ScantronSolutionData.OptionAttachment
                                ScantronSolutionHistoryData.CorrectAnswer = ScantronSolutionData.CorrectAnswer
                                ScantronSolutionHistoryData.CorrectItem = ScantronSolutionData.CorrectItem
                                ScantronSolutionHistoryData.ScoreRatio = ScantronSolutionData.ScoreRatio
                                ScantronSolutionHistoryData.Position = ScantronSolutionData.Position
                                ScantronSolutionHistoryData.CandidateAnswer = ScantronSolutionData.CandidateAnswer
                                AddInfo: Result = self._scantronSolutionHistoryModel.Insert(_dbsession, ScantronSolutionHistoryData)
                                if AddInfo.State == False:
                                    result.Memo = AddInfo.Memo
                                    return result

                                # 删除当前答题卡选项
                                DelInfo: Result = self._scantronSolutionModel.Delete(_dbsession, ScantronSolutionData.ID)
                                if DelInfo.State == False:
                                    result.Memo = DelInfo.Memo
                                    return result

                        # 删除当前答题卡数据
                        DelInfo: Result = self._scantronModel.Delete(_dbsession, ScantronData.ID)
                        if DelInfo.State == False:
                            result.Memo = DelInfo.Memo
                            return result

                # 当前报名数据添加到历史
                ExamInfoHistoryData = ExamInfoHistoryEntity()
                ExamInfoHistoryData.SubjectName = ExamInfoData.SubjectName
                ExamInfoHistoryData.ExamNo = ExamInfoData.ExamNo
                ExamInfoHistoryData.TotalScore = ExamInfoData.TotalScore
                ExamInfoHistoryData.PassLine = ExamInfoData.PassLine
                ExamInfoHistoryData.ActualScore = ExamInfoData.ActualScore
                ExamInfoHistoryData.ExamDuration = ExamInfoData.ExamDuration
                ExamInfoHistoryData.StartTime = ExamInfoData.StartTime
                ExamInfoHistoryData.EndTime = ExamInfoData.EndTime
                ExamInfoHistoryData.ActualDuration = ExamInfoData.ActualDuration
                ExamInfoHistoryData.Pass = ExamInfoData.Pass
                ExamInfoHistoryData.ExamineeID = ExamInfoData.ExamineeID
                ExamInfoHistoryData.ExamState = ExamInfoData.ExamState
                ExamInfoHistoryData.ExamType = ExamInfoData.ExamType
                AddInfo: Result = self._examInfoHistoryModel.Insert(_dbsession, ExamInfoHistoryData)
                if AddInfo.State == False:
                    result.Memo = AddInfo.Memo
                    return result

                # 写入日志
                Desc = 'exam info history No.:' + ExamInfoData.ExamNo
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                # 删除原有报名数据
                DelInfo: Result = self._examInfoModel.Delete(_dbsession, ExamInfoData.ID)
                if DelInfo.State == False:
                    result.Memo = DelInfo.Memo
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result

    def GradeTheExam(self, ClientHost: str, Token: str, ID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result = self.GradeTheExamAction(ClientHost, ID, AdminID)
        _dbsession.close()
        return result

    def GradeTheExamAction(self, ClientHost: str, ID: int, AdminID: int = 0) -> Result:
        result = Result()
        _dbsession = DBsession()
        if ID <= 0:
            result.Memo = self._lang.WrongID
        else:
            # 获取报名数据
            ExamInfoData: ExamInfoEntity = self._examInfoModel.Find(_dbsession, ID)
            if ExamInfoData is None:
                result.Memo = self._lang.ExamDataDoesNotExist
            elif ExamInfoData.ActualScore > 0:
                result.Memo = self._lang.ScoringCompleted
                result.State = True
            elif ExamInfoData.ExamState != 3:
                result.Memo = self._lang.ExamNotCompleted
            else:
                # 获取答题卡数据
                ScantronDataList: list = self._scantronModel.FindExamID(_dbsession, ExamInfoData.ID)
                if len(ScantronDataList) == 0:
                    result.Memo = self._lang.WrongData
                else:
                    TotalScore: float = 0.00
                    for i in ScantronDataList:
                        ScantronData: ScantronEntity = i
                        # print(ScantronData.ID)
                        if ScantronData.QuestionType > 0:
                            # 获取答题卡选项数据
                            ScantronSolutionDataList: list = self._scantronSolutionModel.FindScantronID(_dbsession, ScantronData.ID)
                            # print(len(ScantronSolutionDataList))
                            if len(ScantronSolutionDataList) == 0:
                                result.Memo = self._lang.ScantronSolutionDataError
                                return result
                            else:
                                Correct: bool = True
                                # 单选 判断 多选
                                if ScantronData.QuestionType >= 1 and ScantronData.QuestionType <= 3:
                                    for j in ScantronSolutionDataList:
                                        ScantronSolutionData: ScantronSolutionEntity = j
                                        if ScantronSolutionData.CorrectAnswer == 1 and ScantronSolutionData.CandidateAnswer == 'True':
                                            Correct = False
                                        if ScantronSolutionData.CorrectAnswer == 2 and ScantronSolutionData.CandidateAnswer == 'False':
                                            Correct = False
                                # 填空 问答 实训
                                elif ScantronData.QuestionType >= 4 and ScantronData.QuestionType <= 6:
                                    for j in ScantronSolutionDataList:
                                        ScantronSolutionData: ScantronSolutionEntity = j
                                        if ScantronSolutionData.CorrectItem != ScantronSolutionData.CandidateAnswer:
                                            Correct = False
                                # 拖拽
                                elif ScantronData.QuestionType == 7:
                                    for j in ScantronSolutionDataList:
                                        ScantronSolutionData: ScantronSolutionEntity = j
                                        if ScantronSolutionData.Position == 2:
                                            if ScantronSolutionData.CorrectItem != '' and ScantronSolutionData.CandidateAnswer == '':
                                                Correct = False
                                            if ScantronSolutionData.CorrectItem == '' and ScantronSolutionData.CandidateAnswer != '':
                                                Correct = False
                                            if ScantronSolutionData.CorrectItem != '' and ScantronSolutionData.CandidateAnswer != '':
                                                SubID: int = int(ScantronSolutionData.CandidateAnswer)
                                                if SubID > 0:
                                                    ScantronSolutionDataSub: ScantronSolutionEntity = self._scantronSolutionModel.Find(_dbsession, SubID)
                                                    if ScantronSolutionDataSub is not None and ScantronSolutionData.CorrectItem != ScantronSolutionDataSub.Option:
                                                        Correct = False
                                # 连线
                                elif ScantronData.QuestionType == 8:
                                    for j in ScantronSolutionDataList:
                                        ScantronSolutionData: ScantronSolutionEntity = j
                                        if ScantronSolutionData.Position == 2:
                                            if ScantronSolutionData.CorrectItem != '' and ScantronSolutionData.CandidateAnswer == '':
                                                Correct = False
                                            if ScantronSolutionData.CorrectItem == '' and ScantronSolutionData.CandidateAnswer != '':
                                                Correct = False
                                            if ScantronSolutionData.CorrectItem != '' and ScantronSolutionData.CandidateAnswer != '':
                                                CandidateAnswerList: list = ScantronSolutionData.CandidateAnswer.split(',')
                                                # 答案数量是否相同
                                                if len(ScantronSolutionData.CorrectItem.split('<->')) != len(CandidateAnswerList):
                                                    Correct = False
                                                for c in CandidateAnswerList:
                                                    SubID: int = int(c)
                                                    if SubID > 0:
                                                        ScantronSolutionDataSub: ScantronSolutionEntity = self._scantronSolutionModel.Find(_dbsession, SubID)
                                                        if ScantronSolutionDataSub is not None and ScantronSolutionDataSub.Option not in ScantronSolutionData.CorrectItem:
                                                            Correct = False
                                else:
                                    continue
                                if Correct == True:
                                    TotalScore += float(ScantronData.Score)
                        else:
                            continue

                    _dbsession.begin_nested()

                    try:
                        ExamInfoData.ActualScore = TotalScore
                        ExamInfoData.UpdateTime = self._common.Time()
                        _dbsession.commit()
                    except Exception as e:
                        result.Memo = str(e)
                        _dbsession.rollback()
                        return result

                    Desc = 'grade the exam No.:' + ExamInfoData.ExamNo
                    if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                        result.Memo = self._lang.LoggingFailed
                        return result

                    _dbsession.commit()
                    result.State = True
        _dbsession.close()
        return result

    def ImportExamInfo(self, ClientHost: str, Token: str, FileType: str, Contents: bytes) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif FileType == '':
            result.Memo = self._lang.WrongFileType
        elif len(Contents) == '':
            result.Memo = self._lang.NoData
        else:
            FileType = self._common.MIME(FileType)
            if FileType == '':
                result.Memo = self._lang.WrongFileType
                return result
            if FileType != '.xls' and FileType != '.xlsx':
                result.Memo = self._lang.WrongFileType
                return result

            # 保存路径
            ResourcePath: str = self._rootPath + 'Resource/ExamInfo/'
            try:
                self._file.MkDirs(ResourcePath)
            except Exception as e:
                result.Memo = str(e)
                return result

            # 写入文件
            UploadPath = ResourcePath + str(self._common.TimeMS()) + '.' + FileType
            try:
                with open(UploadPath, 'wb') as f:
                    f.write(Contents)
            except Exception as e:
                result.Memo = str(e)
                return result

            _dbsession.begin_nested()

            # 解析Excel
            try:
                XBook: xlrd.Book = xlrd.open_workbook(UploadPath)  # 读取文件
                XSheet: xlrd.sheet.Sheet = XBook.sheets()[0]  # 获取第一页
                XNrows = XSheet.nrows  # 有效行数
                j = 0
                if XNrows > 2:
                    for i in XSheet:
                        j += 1
                        if j == XNrows: break

                        XSheetListValue = XSheet.row_values(j, start_colx=0, end_colx=None)
                        # print(XSheetListValue)
                        SubjectName: str = str(XSheetListValue[0]).strip()
                        ExamType: int = int(XSheetListValue[1])
                        ExamNo: str = str(XSheetListValue[2]).strip()
                        ExamineeNo: str = str(XSheetListValue[3]).strip()
                        Name: str = str(XSheetListValue[4]).strip()
                        ClassName: str = str(XSheetListValue[5]).strip()
                        Contact: str = str(XSheetListValue[6]).strip()

                        RowInfo: str = str(j) + self._lang.Row + ' '
                        if SubjectName == '':
                            result.Memo = RowInfo + self._lang.WrongSubjectName
                            _dbsession.rollback()
                            return result

                        if ExamType != 1 and ExamType != 2:
                            result.Code = RowInfo + self._lang.WrongExamType
                            _dbsession.rollback()
                            return result

                        if ExamNo == '':
                            result.Memo = RowInfo + self._lang.WrongExamNo
                            _dbsession.rollback()
                            return result

                        if ExamineeNo != '' and Name == '':
                            result.Code = RowInfo + self._lang.WrongName
                            _dbsession.rollback()
                            return result

                        if ExamineeNo == '' and Name != '':
                            result.Code = RowInfo + self._lang.WrongExamineeNo
                            _dbsession.rollback()
                            return result

                        if ExamineeNo != '' and ClassName == '':
                            result.Code = RowInfo + self._lang.WrongClassName
                            _dbsession.rollback()
                            return result

                        ExamInfoData = ExamInfoEntity()

                        SubjectData: SubjectEntity = self._subjectModel.FindSubjectCode(_dbsession, SubjectName)
                        if SubjectData is None:
                            result.Memo = RowInfo + SubjectName + ' ' + self._lang.SubjectDataDoesNotExist
                            _dbsession.rollback()
                            return result

                        ExamInfoObj: ExamInfoEntity = self._examInfoModel.FindExamNo(_dbsession, ExamNo)
                        if ExamInfoObj is not None:
                            result.Memo = RowInfo + ExamNo + ' ' + self._lang.ExamNoDataAlreadyExists
                            _dbsession.rollback()
                            return result

                        # 选填项 ===================================================================================
                        if ClassName != '':
                            ClassData: ClassEntity = self._classModel.FindClassCode(_dbsession, ClassName)
                            if ClassData is None:
                                result.Memo = RowInfo + ClassName + ' ' + self._lang.ClassDataDoesNotExist
                                _dbsession.rollback()
                                return result

                        if ExamineeNo != '':
                            ExamineeObj: ExamineeEntity = self._examineeModel.FindExamineeNo(_dbsession, ExamineeNo)
                            if ExamineeObj is not None:
                                ExamInfoData.ExamineeID = ExamineeObj.ID
                            else:
                                ExamineeData = ExamineeEntity()
                                ExamineeData.ExamineeNo = ExamineeNo
                                ExamineeData.Name = Name
                                ExamineeData.ClassID = ClassData.ID
                                ExamineeData.Contact = Contact
                                AddInfo: Result = self._examineeModel.Insert(_dbsession, ExamineeData)
                                if AddInfo.State == False:
                                    result.Memo = AddInfo.Memo
                                    return result
                                else:
                                    ExamInfoData.ExamineeID = ExamineeData.ID
                        # ===================================================================================

                        # 是否有相同科目未考试的报名记录
                        CheckExamInfoData: ExamInfoEntity = self._examInfoModel.CheckExam(_dbsession, ExamInfoData.ExamineeID, SubjectName, ExamType)
                        if CheckExamInfoData is not None:
                            if CheckExamInfoData.ExamState == 1 or CheckExamInfoData.ExamState == 2:
                                result.Memo = RowInfo + ExamNo + ' ' + self._lang.AlreadyRegisteredForTheSameSubject
                                _dbsession.rollback()
                                return result

                        ExamInfoData.SubjectName = SubjectName
                        ExamInfoData.ExamNo = ExamNo
                        ExamInfoData.ExamType = ExamType
                        AddInfo: Result = self._examInfoModel.Insert(_dbsession, ExamInfoData)
                        if AddInfo.State == False:
                            result.Memo = AddInfo.Memo
                            return result

                        Desc = 'import exam No.:' + ExamNo
                        if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                            result.Memo = self._lang.LoggingFailed
                            return result
            except Exception as e:
                self._file.DeleteFile(UploadPath)
                _dbsession.rollback()
                result.Memo = str(e)
                return result

            self._file.DeleteFile(UploadPath)
            _dbsession.commit()
            result.State = True
        _dbsession.close()
        return result

    def DownloadExamInfoDemo(self, Token: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            FileName: str = self._rootPath + 'Resource/demo.xls'
            with open(FileName, 'rb') as f:
                FileEncode = b64encode(f.read())
                FileEncodeStr = str(FileEncode, 'utf-8')
            result.State = True
            result.Memo = self._file.CheckFileType(FileName)
            result.Data = FileEncodeStr
        _dbsession.close()
        return result
