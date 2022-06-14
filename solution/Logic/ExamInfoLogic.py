from Logic.BaseLogic import *


class ExamInfoLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewExamInfo(self, ClientHost: str, Token: str, SubjectName: str, ExamNo: str, ExamineeID: int, ExamType: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif SubjectName == '':
            result.Memo = 'wrong subject name'
        elif ExamNo == '':
            result.Memo = 'wrong exam No.'
        elif ExamType <= 0:
            result.Memo = 'wrong exam type'
        else:
            SubjectData: SubjectEntity = self._subjectModel.FindSubjectCode(_dbsession, SubjectName)
            if SubjectData is None:
                result.Memo = 'subject data error'
            elif SubjectData.SubjectState == 2:
                result.Memo = 'subject data is disabled'
            else:
                if ExamineeID > 0:
                    # 考生信息是否存在
                    if self._examineeModel.Find(_dbsession, ExamineeID) is None:
                        result.Memo = 'examinee data does not exist'
                        return result
                    # 该考生是否有相同科目的报名且未考试
                    CheckData: ExamInfoEntity = self._examInfoModel.CheckExam(_dbsession, ExamineeID, SubjectName)
                    if CheckData is not None:
                        if CheckData.ExamState < 3:
                            result.Memo = 'already registered for the same subject'
                            return result

                CheckExamNo: ExamInfoEntity = self._examInfoModel.FindExamNo(_dbsession, ExamNo)
                if CheckExamNo.ExamState != 4:
                    result.Memo = 'exam No. data already exists'
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
                    result.Memo = 'logging failed'
                    return result

                _dbsession.commit()
                result.State = True
        return result

    def ExamInfoDisabled(self, ClientHost: str, Token: str, ID: int) -> Result:
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
            ExamInfoData: ExamInfoEntity = self._examInfoModel.Find(_dbsession, ID)
            if ExamInfoData is None:
                result.Memo = 'exam data error'
            elif ExamInfoData.ExamState == 3:
                result.Memo = 'exam completed'
            elif ExamInfoData.ExamState == 4:
                result.Memo = ''
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

                Desc = 'disable exam ID:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result

                _dbsession.commit()
                result.State = True
        return result

    def ExamInfoList(self, Token: str, Page: int, PageSize: int, Stext: str, ExamState: int, ExamType: int) -> ResultList:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        else:
            result: ResultList = self._examInfoModel.List(_dbsession, Page, PageSize, Stext, ExamState, ExamType)
        return result

    def ExamInfo(self, Token: str, ID: int) -> Result:
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
            ExamInfoData: ExamInfoEntity = self._examInfoModel.Find(_dbsession, ID)
            if ExamInfoData is None:
                result.Memo = 'exam data error'
            else:
                result.State = True
                result.Data = ExamInfoData
        return result

    def GenerateTestPaper(self, ClientHost: str, Token: str, ID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        else:
            result = self.GenerateTestPaperAction(ClientHost, ID, AdminID)
        return result

    def GenerateTestPaperAction(self, ClientHost: str, ID: int, AdminID: int = 0) -> Result:
        result = Result()
        _dbsession = DBsession()
        ExamInfoData: ExamInfoEntity = self._examInfoModel.Find(_dbsession, ID)
        if ID <= 0:
            result.Memo = 'wrong ID'
        elif ExamInfoData is None:
            result.Memo = 'registration data does not exist'
        elif ExamInfoData.ExamState == 2:  # 已有试题
            result.Memo = 'question data already exists'
        elif ExamInfoData.ExamState == 3:  # 考试已完成
            result.Memo = 'exam completed'
        elif ExamInfoData.ExamState == 4:  # 报名已禁用
            result.Memo = 'registration data disabled'
        elif ExamInfoData.ExamineeID > 0 and self._examineeModel.Find(_dbsession, ExamInfoData.ExamineeID) is None:  # 考生不存在
            result.Memo = 'examinee data does not exist'
        else:
            # 科目数据
            SubjectData: SubjectEntity = self._subjectModel.FindSubjectCode(_dbsession, ExamInfoData.SubjectName)
            if SubjectData is None:
                result.Memo = 'subject data does not exist'
            else:
                # 获取当前科目下的有效试卷
                PaperData: PaperEntity = self._paperModel.FindSubjectPaper(_dbsession, SubjectData.ID)
                if PaperData is None:
                    result.Memo = 'paper data does not exist'
                else:
                    # 获取当前试卷下所有有效试卷规则
                    PaperRuleListData: list = self._paperRuleModel.AllPaperRule(_dbsession, PaperData.ID)
                    if len(PaperRuleListData) == 0:
                        result.Memo = 'paper data does not exist'
                    else:
                        _dbsession.begin_nested()

                        # 遍历试卷规则
                        for i in PaperRuleListData:
                            PaperRuleData: PaperRuleEntity = i

                            # 解析大标题数据 ===============================================================================
                            if PaperRuleData.HeadlineID > 0:
                                HeadlineData: HeadlineEntity = self._headlineModel.Find(_dbsession, PaperRuleData.HeadlineID)
                                if HeadlineData is None:
                                    result.Memo = 'headline data error'
                                    _dbsession.rollback()
                                    return result
                                if HeadlineData.Content == '':
                                    result.Memo = 'headline data error'
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
                                    result.Memo = 'exam paper rules error'
                                    _dbsession.rollback()
                                    return result
                                # 获取该知识点下对应类型的试题数据
                                QuestionDataList: list = self._questionModel.PaperRuleQuestion(_dbsession, PaperRuleData.KnowledgeID, PaperRuleData.QuestionType)
                                if len(QuestionDataList) < PaperRuleData.QuestionNum:
                                    result.Memo = 'not enough questions'
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
                                        result.Memo = 'wrong question options'
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

                        ExamInfoData.ExamState = 2  # 报名状态改为待考

                        Desc = 'generate test paper exam No.:' + str(ExamInfoData.ID)
                        if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                            result.Memo = 'logging failed'
                            return result

                        _dbsession.commit()
                        result.State = True
        return result

    def ResetExamQuestionData(self, ClientHost: str, Token: str, ID: int) -> Result:
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
            # 获取报名数据
            ExamInfoData: ExamInfoEntity = self._examInfoModel.Find(_dbsession, ID)
            if ExamInfoData is None:
                result.Memo = 'exam data error'
            elif ExamInfoData.ExamState == 3:
                result.Memo = 'exam completed'
            elif ExamInfoData.ExamState == 4:
                result.Memo = 'exam data disabled'
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

                Desc = 'reset exam ID:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result

                _dbsession.commit()
                result.State = True
        return result
