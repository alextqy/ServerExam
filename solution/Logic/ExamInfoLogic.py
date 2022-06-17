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
                    CheckData: ExamInfoEntity = self._examInfoModel.CheckExam(_dbsession, ExamineeID, SubjectName)
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
            elif ExamInfoData.ExamState == 3:
                result.Memo = self._lang.ExamCompleted
            elif ExamInfoData.ExamState == 4:
                result.State = True
            else:
                _dbsession.begin_nested()

                # 待考状态的报名 作废时要删除对应的答题卡和答题卡选项
                if ExamInfoData.ExamState == 2:
                    ScantronDataList: list = self._scantronModel.AllInExamID(_dbsession, ID)
                    if len(ScantronDataList) > 0:
                        for i in ScantronDataList:
                            ScantronData: ScantronEntity = i
                            # 删除答题卡选项
                            ScantronSolutionDataList: list = self._scantronSolutionModel.AllInScantronID(_dbsession, ScantronData.ID)
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
                                _dbsession.rollback()
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
        return result

    def ExamInfoList(self, Token: str, Page: int, PageSize: int, Stext: str, ExamState: int, ExamType: int) -> ResultList:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: ResultList = self._examInfoModel.List(_dbsession, Page, PageSize, Stext, ExamState, ExamType)
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
                    PaperRuleListData: list = self._paperRuleModel.AllPaperRule(_dbsession, PaperData.ID)
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
                                    QuestionSolutionDataList: list = self._questionSolutionModel.AllSolutions(_dbsession, QuestionData.ID)
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
            elif ExamInfoData.ExamState == 3:
                result.Memo = self._lang.ExamCompleted
            elif ExamInfoData.ExamState == 4:
                result.Memo = self._lang.ExamDataDisabled
            else:
                _dbsession.begin_nested()

                # 获取对应答题卡列表数据
                if ExamInfoData.ExamState == 2:
                    ScantronDataList: list = self._scantronModel.AllInExamID(_dbsession, ID)
                    if len(ScantronDataList) > 0:
                        for i in ScantronDataList:
                            ScantronData: ScantronEntity = i
                            # 删除答题卡选项
                            ScantronSolutionDataList: list = self._scantronSolutionModel.AllInScantronID(_dbsession, ScantronData.ID)
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
            elif ExamInfoData.ExamState == 2:
                result.Memo = 'ID:' + str(ID) + self._lang.HasNotYetTakenTheExam
            else:
                # 获取报名下的答题卡
                ScantronDataList: list = self._scantronModel.AllInExamID(_dbsession, ID)
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
                        ScantronSolutionDataList: list = self._scantronSolutionModel.AllInScantronID(_dbsession, ScantronData.ID)
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
        return result
