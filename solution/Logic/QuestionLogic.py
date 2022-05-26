from Logic.BaseLogic import *


class QuestionLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewQuestion(self, ClientHost: str, Token: str, QuestionTitle: str, QuestionType: int, KnowledgeID: int, Description: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif QuestionTitle == '':
            result.Memo = 'wrong question title'
        elif QuestionType <= 0:
            result.Memo = 'wrong question type'
        elif QuestionType == 4 and QuestionTitle.find('<->') == -1:
            result.Memo = 'no vacancy'
        elif KnowledgeID <= 0:
            result.Memo = 'wrong knowledge id'
        else:
            KnowledgeData: KnowledgeEntity = self._knowledgeModel.Find(_dbsession, KnowledgeID)
            if KnowledgeData is None:
                result.Memo = 'knowledge data error'
            else:
                _dbsession.begin_nested()

                QuestionData: QuestionEntity = QuestionEntity()
                QuestionData.QuestionTitle = QuestionTitle
                QuestionData.QuestionType = QuestionType
                QuestionData.KnowledgeID = KnowledgeID
                QuestionData.Description = Description
                AddInfo: Result = self._questionModel.Insert(_dbsession, QuestionData)
                if AddInfo.State == False:
                    result.Memo = AddInfo.Memo
                    return result

                Desc = 'new question:' + QuestionTitle
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result

                _dbsession.commit()
                result.State = True
        return result

    def QuestionAttachment(self, ClientHost: str, Token: str, ID: int, FileType: str, AttachmentContents: bytes) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif ID <= 0:
            result.Memo = 'wrong id'
        elif FileType == '':
            result.Memo = 'wrong file type'
        elif len(AttachmentContents) > (UploadFile.spool_max_size / 2):
            result.Memo = 'too large file'
        else:
            QuestionData: QuestionEntity = self._questionModel.Find(_dbsession, ID)
            if QuestionData is None:
                result.Memo = 'data error'
            else:
                if QuestionData.Attachment != 'none':
                    self._file.DeleteFile(QuestionData.Attachment)

                _dbsession.begin_nested()

                try:
                    UploadPath = self._rootPath + 'Resource/Question/' + str(self._common.TimeMS()) + '.' + FileType
                    with open(UploadPath, 'wb') as f:
                        f.write(AttachmentContents)
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                try:
                    QuestionData.Attachment = UploadPath
                    QuestionData.UpdateTime = self._common.Time()
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                Desc = 'update question attachment id:' + str(ID) + ' file path:' + UploadPath
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result

                _dbsession.commit()

                result.State = True
                result.Data = UploadPath
        return result

    def QuestionDisabled(self, ClientHost: str, Token: str, ID: int) -> Result:
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
            QuestionData: QuestionEntity = self._questionModel.Find(_dbsession, ID)
            if QuestionData is None:
                result.Memo = 'data error'
            else:
                _dbsession.begin_nested()

                try:
                    if QuestionData.QuestionState == 2:
                        # 试卷选项合理性解析
                        QuestionSolutionList: ResultList = self._questionSolutionModel.AllSolutions(_dbsession, QuestionData.ID)
                        QuestionSolutionDataList: list = QuestionSolutionList.Data
                        if len(QuestionSolutionDataList) == 0:
                            result.Memo = 'no options'
                            return result

                        if QuestionData.QuestionType == 1:  # 单选题 ##################################################################
                            # 不能低于两个选项
                            if len(QuestionSolutionDataList) < 2:
                                result.Memo = 'need more than two options'
                                return result
                            # 答案统计
                            CorrectAnswerCount: int = 0
                            WrongAnswerCount: int = 0
                            for i in QuestionSolutionDataList:
                                Data: QuestionSolutionEntity = i
                                if Data.CorrectAnswer == 1:
                                    WrongAnswerCount += 1
                                if Data.CorrectAnswer == 2:
                                    CorrectAnswerCount += 1
                            # 是否设置唯一正确答案
                            if CorrectAnswerCount != 1:
                                result.Memo = 'too many correct answers'
                                return result
                            # 是否设置错误答案
                            if WrongAnswerCount == 0:
                                result.Memo = 'no wrong answer'
                                return result

                        if QuestionData.QuestionType == 2:  # 判断题 ##################################################################
                            # 只需要两个选项
                            if len(QuestionSolutionDataList) != 2:
                                result.Memo = 'just need two options'
                                return result
                            # 答案统计
                            CorrectAnswerCount: int = 0
                            WrongAnswerCount: int = 0
                            for i in QuestionSolutionDataList:
                                Data: QuestionSolutionEntity = i
                                if Data.CorrectAnswer == 1:
                                    WrongAnswerCount += 1
                                if Data.CorrectAnswer == 2:
                                    CorrectAnswerCount += 1
                            if CorrectAnswerCount != 1:
                                result.Memo = 'just need one correct answer'
                                return result
                            if WrongAnswerCount != 1:
                                result.Memo = 'just need one wrong answer'
                                return result

                        if QuestionData.QuestionType == 3:  # 多选题 ##################################################################
                            # 不能低于两个选项
                            if len(QuestionSolutionDataList) < 2:
                                result.Memo = 'need more than two options'
                                return result
                            # 答案统计
                            CorrectAnswerCount: int = 0
                            for i in QuestionSolutionDataList:
                                Data: QuestionSolutionEntity = i
                                if Data.CorrectAnswer == 2:
                                    CorrectAnswerCount += 1
                            if CorrectAnswerCount < 2:
                                result.Memo = 'at least two correct answers'
                                return result

                        if QuestionData.QuestionType == 4:  # 填空题 ##################################################################
                            # 答案数量是否超过填空数
                            if len(QuestionSolutionDataList) != self._common.CountStr(QuestionData.QuestionTitle, '<->'):
                                result.Memo = 'wrong number of options'
                                return result
                            # 得分比例统计
                            ScoreRatioCount: float = 0
                            for i in QuestionSolutionDataList:
                                Data: QuestionSolutionEntity = i
                                ScoreRatioCount += Data.ScoreRatio
                            if ScoreRatioCount != 1:
                                result.Memo = 'the sum of the score ratios is not 1'
                                return result

                        if QuestionData.QuestionType == 5:  # 问答题 ##################################################################
                            # 得分比例统计
                            ScoreRatioCount: float = 0
                            for i in QuestionSolutionDataList:
                                Data: QuestionSolutionEntity = i
                                ScoreRatioCount += Data.ScoreRatio
                            if ScoreRatioCount != 1:
                                result.Memo = 'the sum of the score ratios is not 1'
                                return result

                        if QuestionData.QuestionType == 6:  # 代码实训 ##################################################################
                            # 只需要一个答案
                            if len(QuestionSolutionDataList) != 1:
                                result.Memo = 'just need an answer'
                                return result

                        if QuestionData.QuestionType == 7 or QuestionData.QuestionType == 8:  # 拖拽题 连线题 ##################################################################
                            # 不能低于四个选项
                            if len(QuestionSolutionDataList) < 4:
                                result.Memo = 'need more than four options'
                                return result
                            # 选项解析
                            EmptyAnswer: bool = True
                            LeftPositionCount: int = 0
                            RightPositionCount: int = 0
                            for i in QuestionSolutionDataList:
                                Data: QuestionSolutionEntity = i
                                if Data.Position == 1:
                                    LeftPositionCount += 1
                                if Data.Position == 2:
                                    RightPositionCount += 1
                                if Data.CorrectItem != '':
                                    EmptyAnswer = False
                            # 两侧选项数量是否一致
                            if LeftPositionCount != RightPositionCount:
                                result.Memo = 'inconsistent number of options on both sides'
                                return result
                            # 是否设置答案
                            if EmptyAnswer == True:
                                result.Memo = 'no answer set'
                                return result

                        QuestionData.QuestionState = 1
                    else:
                        QuestionData.QuestionState = 2
                    QuestionData.UpdateTime = self._common.Time()
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                if QuestionData.QuestionState == 1:
                    Desc = 'enable question id:' + str(ID)
                if QuestionData.QuestionState == 2:
                    Desc = 'disable question id:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result

                _dbsession.commit()
                result.State = True
        return result

    def UpdateQuestionInfo(self, ClientHost: str, Token: str, ID: int, QuestionTitle: str, QuestionType: int, Description: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif ID <= 0:
            result.Memo = 'wrong id'
        elif QuestionTitle == '':
            result.Memo = 'wrong question title'
        elif QuestionType == 4 and QuestionTitle.find('<->') == -1:
            result.Memo = 'no vacancy'
        elif QuestionType <= 0:
            result.Memo = 'wrong question type'
        else:
            QuestionData: QuestionEntity = self._questionModel.Find(_dbsession, ID)
            if QuestionData is None:
                result.Memo = 'data error'
            else:
                _dbsession.begin_nested()

                if Description == '':
                    Description = 'none'

                try:
                    QuestionData.QuestionTitle = QuestionTitle
                    QuestionData.QuestionType = QuestionType
                    QuestionData.Description = Description
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                Desc = 'update question id:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
                    return result

                _dbsession.commit()
                result.State = True
        return result

    def QuestionList(self, Token: str, Page: int, PageSize: int, Stext: str, QuestionType: int, QuestionState: int, KnowledgeID: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        else:
            result: ResultList = self._questionModel.List(_dbsession, Page, PageSize, Stext, QuestionType, QuestionState, 1, KnowledgeID)
        return result

    def QuestionInfo(self, Token: str, ID: int) -> Result:
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
            QuestionData: QuestionEntity = self._questionModel.Find(_dbsession, ID)
            if QuestionData is None:
                result.Memo = 'data error'
            else:
                result.State = True
                result.Data = QuestionData
        return result