from Logic.BaseLogic import *


class QuestionSolutionLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewQuestionSolution(self, ClientHost: str, Token: str, QuestionID: int, Option: str, CorrectAnswer: int, CorrectItem: str, ScoreRatio: float, Position: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif QuestionID <= 0:
            result.Memo = self._lang.WrongQuestionID
        # elif Option == '':
        #     result.Memo = self._lang.WrongOption
        # elif CorrectAnswer <= 0:
        #     result.Memo = self._lang.WrongCorrectAnswer
        # elif CorrectItem == '':
        #     result.Memo = self._lang.WrongCorrectItem
        # elif ScoreRatio <= 0:
        #     result.Memo = self._lang.WrongScoreRatio
        # elif Position <= 0:
        #     result.Memo = self._lang.WrongPosition
        else:
            QuestionData: QuestionEntity = self._questionModel.Find(_dbsession, QuestionID)
            if QuestionData is None:
                result.Memo = self._lang.QuestionDataError
            else:
                '''
                单选 ##################################################################
                Option
                CorrectAnswer
                '''
                if QuestionData.QuestionType == 1:
                    if Option == '':
                        result.Memo = self._lang.WrongOption
                        return result
                    if CorrectAnswer <= 0:
                        result.Memo = self._lang.WrongCorrectAnswer
                        return result
                    QuestionSolutionList: list = self._questionSolutionModel.FindQuestionID(_dbsession, QuestionData.ID)
                    if len(QuestionSolutionList) > 0:
                        SolutionDataList: list = QuestionSolutionList
                        # 判断重复选项
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            if SolutionData.Option == Option:
                                result.Memo = self._lang.DuplicateOptions
                                return result
                        # 判断多个正确答案
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            if CorrectAnswer == 2 and SolutionData.CorrectAnswer == CorrectAnswer:
                                result.Memo = self._lang.TooManyCorrectAnswer
                                return result
                    ScoreRatio = 1.00
                '''
                判断 ##################################################################
                Option
                CorrectAnswer
                '''
                if QuestionData.QuestionType == 2:
                    if Option == '':
                        result.Memo = self._lang.WrongOption
                        return result
                    if CorrectAnswer <= 0:
                        result.Memo = self._lang.WrongCorrectAnswer
                        return result
                    QuestionSolutionList: list = self._questionSolutionModel.FindQuestionID(_dbsession, QuestionData.ID)
                    if len(QuestionSolutionList) > 0:
                        SolutionDataList: list = QuestionSolutionList
                        # 判断题只能有两个选项
                        if len(SolutionDataList) >= 2:
                            result.Memo = self._lang.TooManyOptions
                            return result
                        # 判断重复选项
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            if SolutionData.Option == Option:
                                result.Memo = self._lang.DuplicateOptions
                                return result
                        # 单个正确答案
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            if CorrectAnswer == 1 and SolutionData.CorrectAnswer == CorrectAnswer:
                                result.Memo = self._lang.TooManyWrongAnswer
                                return result
                            if CorrectAnswer == 2 and SolutionData.CorrectAnswer == CorrectAnswer:
                                result.Memo = self._lang.TooManyCorrectAnswer
                                return result
                    ScoreRatio = 1.00
                '''
                多选(必须全对才给分) ##################################################################
                Option
                CorrectAnswer
                '''
                if QuestionData.QuestionType == 3:
                    if Option == '':
                        result.Memo = self._lang.WrongOption
                        return result
                    if CorrectAnswer <= 0:
                        result.Memo = self._lang.WrongCorrectAnswer
                        return result
                    QuestionSolutionList: list = self._questionSolutionModel.FindQuestionID(_dbsession, QuestionData.ID)
                    if len(QuestionSolutionList) > 0:
                        SolutionDataList: list = QuestionSolutionList
                        # 判断重复选项
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            if SolutionData.Option == Option:
                                result.Memo = self._lang.DuplicateOptions
                                return result
                    ScoreRatio = 1.00
                '''
                填空 ##################################################################
                CorrectItem
                ScoreRatio
                '''
                if QuestionData.QuestionType == 4:
                    if CorrectItem == '':
                        result.Memo = self._lang.WrongCorrectItem
                        return result
                    if ScoreRatio <= 0:
                        result.Memo = self._lang.WrongScoreRatio
                        return result
                    Option = 'none'
                    QuestionSolutionList: list = self._questionSolutionModel.FindQuestionID(_dbsession, QuestionData.ID)
                    if len(QuestionSolutionList) > 0:
                        SolutionDataList: list = QuestionSolutionList
                        # 答案数量是否超过填空数
                        if len(SolutionDataList) >= self._common.CountStr(QuestionData.QuestionTitle, '<->'):
                            result.Memo = self._lang.TooManyAnswers
                            return result
                        # 判断重复答案
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            if SolutionData.CorrectItem == CorrectItem:
                                result.Memo = self._lang.DuplicateOptions
                                return result
                        # 所有选项得分比例总和为1
                        CountScoreRatio = 0
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            CountScoreRatio += SolutionData.ScoreRatio
                        if float(CountScoreRatio) + ScoreRatio > 1:
                            result.Memo = self._lang.WrongScoreRatio
                            return result
                    CorrectAnswer = 1
                '''
                问答 ##################################################################
                CorrectItem
                ScoreRatio
                '''
                if QuestionData.QuestionType == 5:
                    if CorrectItem == '':
                        result.Memo = self._lang.WrongCorrectItem
                        return result
                    if ScoreRatio <= 0:
                        result.Memo = self._lang.WrongScoreRatio
                        return result
                    Option = 'none'
                    QuestionSolutionList: list = self._questionSolutionModel.FindQuestionID(_dbsession, QuestionData.ID)
                    if len(QuestionSolutionList) > 0:
                        SolutionDataList: list = QuestionSolutionList
                        # 判断重复答案
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            if SolutionData.CorrectItem == CorrectItem:
                                result.Memo = self._lang.DuplicateOptions
                                return result
                        CountScoreRatio = 0
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            CountScoreRatio += SolutionData.ScoreRatio
                        # 所有选项得分比例总和为1
                        if float(CountScoreRatio) + ScoreRatio > 1:
                            result.Memo = self._lang.WrongScoreRatio
                            return result
                    CorrectAnswer = 1
                '''
                代码实训 ##################################################################
                CorrectItem
                '''
                if QuestionData.QuestionType == 6:
                    if CorrectItem == '':
                        result.Memo = self._lang.WrongCorrectItem
                        return result
                    QuestionSolutionList: list = self._questionSolutionModel.FindQuestionID(_dbsession, QuestionData.ID)
                    if len(QuestionSolutionList) >= 1:
                        result.Memo = self._lang.TooManyAnswers
                        return result
                    Option = 'none'
                    CorrectAnswer = 1
                    ScoreRatio = 1.00
                '''
                拖拽题 ##################################################################
                Option
                Position
                CorrectItem
                '''
                if QuestionData.QuestionType == 7:
                    if Option == '':
                        result.Memo = self._lang.WrongOption
                        return result
                    if Position <= 0:
                        result.Memo = self._lang.WrongPosition
                        return result
                    if Position == 1:  # 左侧为备选项 不能设置正确答案
                        CorrectItem = ''
                    CorrectAnswer = 1
                    if CorrectItem != '':
                        CorrectAnswer = 2
                    QuestionSolutionList: list = self._questionSolutionModel.FindQuestionID(_dbsession, QuestionData.ID)
                    if len(QuestionSolutionList) > 0:
                        SolutionDataList: list = QuestionSolutionList
                        # 判断重复选项
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            if SolutionData.Option == Option:
                                result.Memo = self._lang.DuplicateOptions
                                return result
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            if SolutionData.CorrectItem != '' and SolutionData.CorrectItem == CorrectItem:
                                result.Memo = self._lang.DuplicateCorrectItem
                                return result
                        if CorrectItem != '':
                            CorrectItemData: QuestionSolutionEntity = self._questionSolutionModel.FindCorrectItem(_dbsession, QuestionID, CorrectItem)
                            # 答案项是否存在
                            if CorrectItemData is None:
                                result.Memo = self._lang.CorrectItemDataError
                                return result
                            # 答案必须为左侧选项ID
                            if CorrectItemData.Position == 2:
                                result.Memo = self._lang.TheAnswerMustBeTheLeftOptionID
                                return result
                    ScoreRatio = 1.00
                '''
                连线题 ##################################################################
                Option
                Position
                CorrectItem
                '''
                if QuestionData.QuestionType == 8:
                    if Option == '':
                        result.Memo = self._lang.WrongOption
                        return result
                    if Position <= 0:
                        result.Memo = self._lang.WrongPosition
                        return result
                    if Position == 1:  # 左侧为备选项 不能设置正确答案
                        CorrectItem = ''
                    CorrectAnswer = 1  # 答案内容不为空 则为正确答案
                    if CorrectItem != '':
                        CorrectAnswer = 2
                    QuestionSolutionList: list = self._questionSolutionModel.FindQuestionID(_dbsession, QuestionData.ID)
                    if len(QuestionSolutionList) > 0:
                        SolutionDataList: list = QuestionSolutionList
                        # 判断重复选项
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            if SolutionData.Option == Option:
                                result.Memo = self._lang.DuplicateOptions
                                return result
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            if SolutionData.CorrectItem != '' and SolutionData.CorrectItem == CorrectItem:
                                result.Memo = self._lang.DuplicateCorrectItem
                                return result
                        if CorrectItem != '':
                            CorrectItemList: list = list(set(CorrectItem.split('<->')))
                            for i in CorrectItemList:
                                CorrectItemStr: str = i
                                # 答案是否存在于其他选项中
                                for j in SolutionDataList:
                                    SolutionData: QuestionSolutionEntity = j
                                    if CorrectItemStr in SolutionData.CorrectItem:
                                        result.Memo = self._lang.DuplicateAnswer
                                        return result
                                # 答案项是否存在
                                CorrectItemData: QuestionSolutionEntity = self._questionSolutionModel.FindCorrectItem(_dbsession, QuestionID, CorrectItemStr)
                                if CorrectItemData is None:
                                    result.Memo = self._lang.CorrectItemDataError
                                    return result
                                # 答案项是否属于当前试题
                                if CorrectItemData.QuestionID != QuestionData.ID:
                                    result.Memo = self._lang.QuestionIDError
                                    return result
                                # 答案必须为左侧选项ID
                                if CorrectItemData.Position == 2:
                                    result.Memo = self._lang.TheAnswerMustBeTheLeftOptionID
                                    return result
                    ScoreRatio = 1.00

                _dbsession.begin_nested()

                QuestionData = QuestionSolutionEntity()
                QuestionData.QuestionID = QuestionID
                QuestionData.Option = Option
                QuestionData.CorrectAnswer = CorrectAnswer
                QuestionData.CorrectItem = CorrectItem
                QuestionData.ScoreRatio = ScoreRatio
                QuestionData.Position = Position
                AddInfo: Result = self._questionSolutionModel.Insert(_dbsession, QuestionData)
                if AddInfo.State == False:
                    result.Memo = AddInfo.Memo
                    return result

                Desc = 'new question solution:' + Option
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()
                result.State = True
        return result

    def QuestionSolutionAttachment(self, ClientHost: str, Token: str, ID: int, FileType: str, AttachmentContents: bytes) -> Result:
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
            QuestionSolutionData: QuestionSolutionEntity = self._questionSolutionModel.Find(_dbsession, ID)
            if QuestionSolutionData is None:
                result.Memo = self._lang.QuestionSolutionDataError
            else:
                if QuestionSolutionData.OptionAttachment != 'none':
                    self._file.DeleteFile(QuestionSolutionData.OptionAttachment)

                ResourcePath: str = self._rootPath + 'Resource/QuestionSolution/'
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
                    QuestionSolutionData.OptionAttachment = UploadPath
                    QuestionSolutionData.UpdateTime = self._common.Time()
                    _dbsession.commit()
                except Exception as e:
                    result.Memo = str(e)
                    _dbsession.rollback()
                    return result

                Desc = 'update question solution attachment ID:' + str(ID) + ' file path:' + UploadPath
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                _dbsession.commit()

                result.State = True
                result.Data = UploadPath
        return result

    def QuestionSolutionDelete(self, ClientHost: str, Token: str, ID: int):
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
            QuestionSolutionData: QuestionSolutionEntity = self._questionSolutionModel.Find(_dbsession, ID)
            if QuestionSolutionData is None:
                result.Memo = self._lang.QuestionSolutionDataError
            else:
                _dbsession.begin_nested()

                DeleteInfo: Result = self._questionSolutionModel.Delete(_dbsession, ID)
                if DeleteInfo.State == False:
                    DeleteInfo.Memo = str(e)
                    return result

                Desc = 'delete question solution option&correct item:' + QuestionSolutionData.Option + '&' + QuestionSolutionData.CorrectItem
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = self._lang.LoggingFailed
                    return result

                if QuestionSolutionData.OptionAttachment != 'none':
                    try:
                        self._file.DeleteFile(QuestionSolutionData.OptionAttachment)
                    except Exception as e:
                        result.Memo = str(e)
                        _dbsession.rollback()
                        return result

                QuestionData: QuestionEntity = self._questionModel.Find(_dbsession, QuestionSolutionData.QuestionID)
                # 所属试题设置为禁用状态
                if QuestionData is not None:
                    try:
                        QuestionData.QuestionState = 2
                        _dbsession.commit()
                    except Exception as e:
                        result.Memo = str(e)
                        _dbsession.rollback()
                        return result

                _dbsession.commit()
                result.State = True
        return result

    def QuestionSolutionList(self, Token: str, Page: int, PageSize: int, QuestionID: int) -> ResultList:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = self._lang.WrongToken
        elif AdminID == 0:
            result.Memo = self._lang.PermissionDenied
        elif QuestionID <= 0:
            result.Memo = self._lang.WrongQuestionID
        else:
            result: ResultList = self._questionSolutionModel.List(_dbsession, Page, PageSize, QuestionID)
        return result