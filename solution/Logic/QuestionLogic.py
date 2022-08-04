# -*- coding:utf-8 -*-
from Logic.BaseLogic import *


class QuestionLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewQuestion(self, ClientHost: str, Token: str, QuestionTitle: str, QuestionType: int, KnowledgeID: int, Description: str, Language: str = '', LanguageVersion: str = '') -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif QuestionTitle == '':
            result.Memo = self._lang.WrongQuestionTitle
        elif QuestionType <= 0:
            result.Memo = self._lang.WrongQuestionType
        elif QuestionType == 4 and QuestionTitle.find('<->') == -1:
            result.Memo = self._lang.NoVacancy
        elif KnowledgeID <= 0:
            result.Memo = self._lang.WrongKnowledgeID
        elif QuestionType == 6 and Language == '':
            result.Memo = self._lang.WrongLanguage
        elif QuestionType == 6 and LanguageVersion == '':
            result.Memo = self._lang.WrongLanguageVersion
        else:
            KnowledgeData: KnowledgeEntity = self._knowledgeModel.Find(_dbsession, KnowledgeID)
            if KnowledgeData is None:
                result.Memo = self._lang.KnowledgeDataError
            else:
                if Description == '':
                    Description = 'none'

                QuestionCode: str = self._common.StrMD5(self._common.RandomStr() + str(self._common.Time()))
                CheckCode: QuestionEntity = self._questionModel.FindQuestionCode(_dbsession, QuestionCode)
                if CheckCode is not None:
                    result.Memo = self._lang.TryAgain
                    return result

                _dbsession.begin_nested()

                QuestionData: QuestionEntity = QuestionEntity()
                QuestionData.QuestionTitle = QuestionTitle
                QuestionData.QuestionType = QuestionType
                QuestionData.KnowledgeID = KnowledgeID
                QuestionData.Description = Description
                QuestionData.QuestionCode = QuestionCode
                QuestionData.Language = Language
                QuestionData.LanguageVersion = LanguageVersion
                AddInfo: Result = self._questionModel.Insert(_dbsession, QuestionData)
                if AddInfo.State == False:
                    result.Memo = AddInfo.Memo
                    return result

                Desc = 'new question:' + QuestionTitle
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result

    def QuestionAttachment(self, ClientHost: str, Token: str, ID: int, FileType: str, AttachmentContents: bytes) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif ID <= 0:
            result.Memo = self._lang.WrongID
        elif FileType == '':
            result.Memo = self._lang.WrongFileType
        elif len(AttachmentContents) > (UploadFile.spool_max_size / 2):
            result.Memo = self._lang.TooLargeFile
        else:
            FileType = self._common.MIME(FileType)
            if FileType == '':
                result.Memo = self._lang.WrongFileType
                return result

            QuestionData: QuestionEntity = self._questionModel.Find(_dbsession, ID)
            if QuestionData is None:
                result.Memo = self._lang.QuestionDataError
            else:
                if QuestionData.Attachment != 'none':
                    self._file.DeleteFile(QuestionData.Attachment)

                ResourcePath: str = self._rootPath + 'Resource/Question/'
                self._file.MkDirs(ResourcePath)

                _dbsession.begin_nested()

                try:
                    UploadPath = ResourcePath + str(self._common.TimeMS()) + '.' + FileType
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

                Desc = 'update question attachment ID:' + str(ID) + ' file path:' + UploadPath
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()

                result.State = True
                result.Data = UploadPath
        _dbsession.close()
        return result

    def QuestionDisabled(self, ClientHost: str, Token: str, ID: int) -> Result:
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
            QuestionData: QuestionEntity = self._questionModel.Find(_dbsession, ID)
            if QuestionData is None:
                result.Memo = self._lang.QuestionDataError
            else:
                _dbsession.begin_nested()

                try:
                    if QuestionData.QuestionState == 2:
                        # 试卷选项合理性解析
                        QuestionSolutionDataList: list = self._questionSolutionModel.FindQuestionID(_dbsession, QuestionData.ID)
                        if len(QuestionSolutionDataList) == 0:
                            result.Memo = self._lang.NoOptions
                            _dbsession.rollback()
                            return result

                        if QuestionData.QuestionType == 1:  # 单选题 ##################################################################
                            # 不能低于两个选项
                            if len(QuestionSolutionDataList) < 2:
                                result.Memo = self._lang.NeedMoreThanTwoOptions
                                _dbsession.rollback()
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
                                result.Memo = self._lang.NeedACorrectAnswer
                                _dbsession.rollback()
                                return result
                            # 是否设置错误答案
                            if WrongAnswerCount == 0:
                                result.Memo = self._lang.NoWrongAnswer
                                _dbsession.rollback()
                                return result

                        if QuestionData.QuestionType == 2:  # 判断题 ##################################################################
                            # 只需要两个选项
                            if len(QuestionSolutionDataList) != 2:
                                result.Memo = self._lang.JustNeedTwoOptions
                                _dbsession.rollback()
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
                                result.Memo = self._lang.JustNeedOneCorrectAnswer
                                _dbsession.rollback()
                                return result
                            if WrongAnswerCount != 1:
                                result.Memo = self._lang.JustNeedOneWrongAnswer
                                _dbsession.rollback()
                                return result

                        if QuestionData.QuestionType == 3:  # 多选题 ##################################################################
                            # 不能低于两个选项
                            if len(QuestionSolutionDataList) < 2:
                                result.Memo = self._lang.NeedMoreThanTwoOptions
                                _dbsession.rollback()
                                return result
                            # 正确答案统计
                            CorrectAnswerCount: int = 0
                            for i in QuestionSolutionDataList:
                                Data: QuestionSolutionEntity = i
                                if Data.CorrectAnswer == 2:
                                    CorrectAnswerCount += 1
                            if CorrectAnswerCount < 2:
                                result.Memo = self._lang.AtLeastTwoCorrectAnswers
                                _dbsession.rollback()
                                return result

                        if QuestionData.QuestionType == 4:  # 填空题 ##################################################################
                            # 答案数量是否超过填空数
                            if len(QuestionSolutionDataList) != self._common.CountStr(QuestionData.QuestionTitle, '<->'):
                                result.Memo = self._lang.WrongNumberOfOptions
                                _dbsession.rollback()
                                return result
                            # 得分比例统计
                            ScoreRatioCount: float = 0
                            for i in QuestionSolutionDataList:
                                Data: QuestionSolutionEntity = i
                                ScoreRatioCount += Data.ScoreRatio
                            if ScoreRatioCount != 1:
                                result.Memo = self._lang.TheSumOfTheScoreRatiosIsNotOne
                                _dbsession.rollback()
                                return result

                        if QuestionData.QuestionType == 5:  # 问答题 ##################################################################
                            # 得分比例统计
                            ScoreRatioCount: float = 0
                            for i in QuestionSolutionDataList:
                                Data: QuestionSolutionEntity = i
                                ScoreRatioCount += Data.ScoreRatio
                            if ScoreRatioCount != 1:
                                result.Memo = self._lang.TheSumOfTheScoreRatiosIsNotOne
                                _dbsession.rollback()
                                return result

                        if QuestionData.QuestionType == 6:  # 编程 ##################################################################
                            # 只需要一个答案
                            if len(QuestionSolutionDataList) != 1:
                                result.Memo = self._lang.JustNeedAnAnswer
                                _dbsession.rollback()
                                return result
                            # 是否对应的运行环境
                            from CodeExec.DockerTools import ImageIsExistsAction
                            ImageInfo: Result = ImageIsExistsAction(QuestionData.Language, QuestionData.LanguageVersion)
                            if ImageInfo.State == False:
                                result.Memo = self._lang.TheCodeRuntimeEnvironmentHasNotBeenBuilt
                                return result

                        if QuestionData.QuestionType == 7 or QuestionData.QuestionType == 8:  # 拖拽 连线 ##################################################################
                            # 不能低于四个选项
                            if len(QuestionSolutionDataList) < 4:
                                result.Memo = self._lang.NeedMoreThanFourOptions
                                _dbsession.rollback()
                                return result
                            # 选项解析
                            EmptyAnswer: bool = True  # 判断答案是否为空
                            LeftPositionCount: int = 0  # 左侧选项统计
                            RightPositionCount: int = 0  # 右侧选项统计
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
                                result.Memo = self._lang.InconsistentNumberOfOptionsOnBothSides
                                _dbsession.rollback()
                                return result
                            # 是否设置答案
                            if EmptyAnswer == True:
                                result.Memo = self._lang.NoSetAnswer
                                _dbsession.rollback()
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
                    Desc = 'enable question ID:' + str(ID)
                if QuestionData.QuestionState == 2:
                    Desc = 'disable question ID:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result

    def UpdateQuestionInfo(self, ClientHost: str, Token: str, ID: int, QuestionTitle: str, QuestionType: int, Description: str, Language: str, LanguageVersion: str) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif ID <= 0:
            result.Memo = self._lang.WrongID
        elif QuestionTitle == '':
            result.Memo = self._lang.WrongQuestionTitle
        elif QuestionType == 4 and QuestionTitle.find('<->') == -1:
            result.Memo = self._lang.NoVacancy
        elif QuestionType <= 0:
            result.Memo = self._lang.WrongQuestionType
        elif QuestionType == 6 and Language == '':
            result.Memo = self._lang.WrongLanguage
        elif QuestionType == 6 and LanguageVersion == '':
            result.Memo = self._lang.WrongLanguageVersion
        else:
            QuestionData: QuestionEntity = self._questionModel.Find(_dbsession, ID)
            if QuestionData is None:
                result.Memo = self._lang.QuestionDataError
            else:
                _dbsession.begin_nested()

                if Description == '':
                    Description = 'none'

                try:
                    QuestionData.QuestionTitle = QuestionTitle
                    QuestionData.QuestionType = QuestionType
                    QuestionData.Description = Description
                    QuestionData.Language = Language
                    QuestionData.LanguageVersion = LanguageVersion
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                Desc = 'update question ID:' + str(ID)
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.State = True
        _dbsession.close()
        return result

    def QuestionList(self, Token: str, Page: int, PageSize: int, Stext: str, QuestionType: int, QuestionState: int, KnowledgeID: int) -> ResultList:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        else:
            result: ResultList = self._questionModel.List(_dbsession, Page, PageSize, Stext, QuestionType, QuestionState, 1, KnowledgeID)
        _dbsession.close()
        return result

    def QuestionInfo(self, Token: str, ID: int) -> Result:
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
            QuestionData: QuestionEntity = self._questionModel.Find(_dbsession, ID)
            if QuestionData is None:
                result.Memo = self._lang.QuestionDataError
            else:
                result.State = True
                result.Data = QuestionData
        _dbsession.close()
        return result