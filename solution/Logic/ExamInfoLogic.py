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
        elif ExamineeID <= 0:
            result.Memo = 'wrong examinee ID'
        elif ExamType <= 0:
            result.Memo = 'wrong exam type'
        elif self._subjectModel.FindSubjectCode(_dbsession, SubjectName) is None:
            result.Memo = 'subject data error'
        elif self._examInfoModel.FindExamNo(_dbsession, ExamNo) is not None:
            result.Memo = 'exam No. data already exists'
        elif self._examineeModel.Find(_dbsession, ExamineeID) is None:
            result.Memo = 'examinee data does not exist'
        else:
            # 该考生是否有相同科目的报名且未考试
            CheckData: ExamInfoEntity = self._examInfoModel.CheckExam(_dbsession, ExamineeID, SubjectName)
            if CheckData is not None:
                if CheckData.ExamState < 3:
                    result.Memo = 'already registered for the same subject'
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
            if self.LogSysAction(_dbsession, 1, 0, Desc, ClientHost) == False:
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
                                        _dbsession.rollback()
                                        result.Memo = SSDelInfo.Memo
                                        return result
                            # 删除答题卡
                            SDelInfo: Result = self._scantronModel.Delete(_dbsession, ScantronData.ID)
                            if SDelInfo.State == False:
                                _dbsession.rollback()
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

    def GenerateTestPaper(self, Token: str, ID: int) -> Result:
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
            return self.GenerateTestPaperAction(ID)

    def GenerateTestPaperAction(self, ID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        ExamInfoData: ExamInfoEntity = self._examInfoModel.Find(_dbsession, ID)
        if ExamInfoData is None:
            result.Memo = 'registration data does not exist'
        elif ExamInfoData.ExamState == 2:
            result.Memo = 'question data already exists'
        elif ExamInfoData.ExamState == 3:
            result.Memo = 'exam completed'
        elif ExamInfoData.ExamState == 4:
            result.Memo = 'registration data disabled'
        elif ExamInfoData.ExamineeID > 0 and self._examineeModel.Find(_dbsession, ExamInfoData.ExamineeID) is None:
            result.Memo = 'examinee data does not exist'
        else:
            SubjectData: SubjectEntity = self._subjectModel.FindSubjectCode(_dbsession, ExamInfoData.SubjectName)
            if SubjectData is None:
                result.Memo = 'subject data does not exist'
            else:
                PaperData: PaperEntity = self._paperModel.FindSubjectPaper(_dbsession, SubjectData.ID)
                if PaperData is None:
                    result.Memo = 'paper data does not exist'
                else:
                    PaperRuleListData: list = self._paperRuleModel.AllPaperRule(_dbsession, PaperData.ID)
                    if len(PaperRuleListData) == 0:
                        result.Memo = 'paper data does not exist'
                    else:
                        for i in PaperRuleListData:
                            PaperRuleData: PaperRuleEntity = i
                            if PaperRuleData.HeadlineID > 0:
                                HeadlineData: HeadlineEntity = self._headlineModel.Find(_dbsession, PaperRuleData.HeadlineID)
                                if HeadlineData is None:
                                    result.Memo = 'headline data error'
                                    return result
                            if PaperRuleData.KnowledgeID > 0:
                                if PaperRuleData.QuestionType == 0 or PaperRuleData.QuestionNum == 0:
                                    result.Memo = 'exam paper rules error'
                                    return result
        return result