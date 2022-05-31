from Logic.BaseLogic import *


class QuestionSolutionLogic(BaseLogic):

    def __init__(self):
        super().__init__()

    def NewQuestionSolution(self, ClientHost: str, Token: str, QuestionID: int, Option: str, CorrectAnswer: int, CorrectItem: str, ScoreRatio: float, Position: int) -> Result:
        result = Result()
        _dbsession = DBsession()
        AdminID = self.PermissionValidation(_dbsession, Token)
        if Token == '':
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif QuestionID <= 0:
            result.Memo = 'wrong question id'
        # elif Option == '':
        #     result.Memo = 'wrong option'
        # elif CorrectAnswer <= 0:
        #     result.Memo = 'wrong correct answer'
        # elif CorrectItem == '':
        #     result.Memo = 'wrong correct item'
        # elif ScoreRatio <= 0:
        #     result.Memo = 'wrong score ratio'
        # elif Position <= 0:
        #     result.Memo = 'wrong position'
        else:
            QuestionData: QuestionEntity = self._questionModel.Find(_dbsession, QuestionID)
            if QuestionData is None:
                result.Memo = 'question data error'
            else:
                if QuestionData.QuestionType == 1:  # 单选 ##################################################################
                    if Option == '':
                        result.Memo = 'wrong option'
                        return result
                    if CorrectAnswer <= 0:
                        result.Memo = 'wrong correct answer'
                        return result
                    QuestionSolutionList: ResultList = self._questionSolutionModel.AllSolutions(_dbsession, QuestionData.ID)
                    if len(QuestionSolutionList.Data) > 0:
                        SolutionDataList: list = QuestionSolutionList.Data
                        # 判断重复选项
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            if SolutionData.Option == Option:
                                result.Memo = 'duplicate options'
                                return result
                        # 单个正确答案
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            if CorrectAnswer == 2 and SolutionData.CorrectAnswer == CorrectAnswer:
                                result.Memo = 'too many correct answer'
                                return result
                    ScoreRatio = 1.00
                if QuestionData.QuestionType == 2:  # 判断 ##################################################################
                    if Option == '':
                        result.Memo = 'wrong option'
                        return result
                    if CorrectAnswer <= 0:
                        result.Memo = 'wrong correct answer'
                        return result
                    QuestionSolutionList: ResultList = self._questionSolutionModel.AllSolutions(_dbsession, QuestionData.ID)
                    if len(QuestionSolutionList.Data) > 0:
                        SolutionDataList: list = QuestionSolutionList.Data
                        # 判断题只能有两个选项
                        if len(SolutionDataList) >= 2:
                            result.Memo = 'too many options'
                            return result
                        # 判断重复选项
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            if SolutionData.Option == Option:
                                result.Memo = 'duplicate options'
                                return result
                        # 单个正确答案
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            if CorrectAnswer == 1 and SolutionData.CorrectAnswer == CorrectAnswer:
                                result.Memo = 'too many correct answer'
                                return result
                            if CorrectAnswer == 2 and SolutionData.CorrectAnswer == CorrectAnswer:
                                result.Memo = 'too many wrong answer'
                                return result
                    ScoreRatio = 1.00
                if QuestionData.QuestionType == 3:  # 多选(必须全对才给分) ##################################################################
                    if Option == '':
                        result.Memo = 'wrong option'
                        return result
                    if CorrectAnswer <= 0:
                        result.Memo = 'wrong correct answer'
                        return result
                    QuestionSolutionList: ResultList = self._questionSolutionModel.AllSolutions(_dbsession, QuestionData.ID)
                    if len(QuestionSolutionList.Data) > 0:
                        SolutionDataList: list = QuestionSolutionList.Data
                        # 判断重复选项
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            if SolutionData.Option == Option:
                                result.Memo = 'duplicate options'
                                return result
                    ScoreRatio = 1.00
                if QuestionData.QuestionType == 4:  # 填空 ##################################################################
                    if CorrectItem == '':
                        result.Memo = 'wrong correct item'
                        return result
                    if ScoreRatio <= 0:
                        result.Memo = 'wrong score ratio'
                        return result
                    QuestionSolutionList: ResultList = self._questionSolutionModel.AllSolutions(_dbsession, QuestionData.ID)
                    if len(QuestionSolutionList.Data) > 0:
                        SolutionDataList: list = QuestionSolutionList.Data
                        # 答案数量是否超过填空数
                        if len(SolutionDataList) >= self._common.CountStr(QuestionData.QuestionTitle, '<->'):
                            result.Memo = 'too many answers'
                            return result
                        # 判断重复答案
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            if SolutionData.CorrectItem == CorrectItem:
                                result.Memo = 'duplicate options'
                                return result
                        # 所有选项得分比例总和为1
                        CountScoreRatio = 0
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            CountScoreRatio += SolutionData.ScoreRatio
                        if float(CountScoreRatio) + ScoreRatio > 1:
                            result.Memo = 'wrong score ratio'
                            return result
                    CorrectAnswer = 1
                if QuestionData.QuestionType == 5:  # 问答 ##################################################################
                    if CorrectItem == '':
                        result.Memo = 'wrong correct item'
                        return result
                    if ScoreRatio <= 0:
                        result.Memo = 'wrong score ratio'
                        return result
                    QuestionSolutionList: ResultList = self._questionSolutionModel.AllSolutions(_dbsession, QuestionData.ID)
                    if len(QuestionSolutionList.Data) > 0:
                        SolutionDataList: list = QuestionSolutionList.Data
                        # 判断重复答案
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            if SolutionData.CorrectItem == CorrectItem:
                                result.Memo = 'duplicate options'
                                return result
                        CountScoreRatio = 0
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            CountScoreRatio += SolutionData.ScoreRatio
                        # 所有选项得分比例总和为1
                        if float(CountScoreRatio) + ScoreRatio > 1:
                            result.Memo = 'wrong score ratio'
                            return result
                    CorrectAnswer = 1
                if QuestionData.QuestionType == 6:  # 代码实训 ##################################################################
                    if CorrectItem == '':
                        result.Memo = 'wrong correct item'
                        return result
                    QuestionSolutionList: ResultList = self._questionSolutionModel.AllSolutions(_dbsession, QuestionData.ID)
                    if len(QuestionSolutionList.Data) >= 1:
                        result.Memo = 'too many answers'
                        return result
                    CorrectAnswer = 1
                    ScoreRatio = 1.00
                if QuestionData.QuestionType == 7:  # 拖拽题 ##################################################################
                    if Option == '':
                        result.Memo = 'wrong option'
                        return result
                    if Position <= 0:
                        result.Memo = 'wrong position'
                        return result
                    if Position == 1:  # 左侧为备选项 不能设置正确答案
                        CorrectItem = ''
                    CorrectAnswer = 1
                    if CorrectItem != '':
                        CorrectAnswer = 2
                    QuestionSolutionList: ResultList = self._questionSolutionModel.AllSolutions(_dbsession, QuestionData.ID)
                    if len(QuestionSolutionList.Data) > 0:
                        SolutionDataList: list = QuestionSolutionList.Data
                        # 判断重复选项
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            if SolutionData.Option == Option:
                                result.Memo = 'duplicate options'
                                return result
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            if SolutionData.CorrectItem != '' and SolutionData.CorrectItem == CorrectItem:
                                result.Memo = 'duplicate correct item'
                                return result
                        if CorrectItem != '':
                            try:
                                CorrectItemData: QuestionSolutionEntity = self._questionSolutionModel.Find(_dbsession, int(CorrectItem))
                            except Exception as e:
                                result.Memo = str(e)
                                return result
                            # 答案项是否存在
                            if CorrectItemData is None:
                                result.Memo = 'correct item data error'
                                return result
                            # 答案项是否属于当前试题
                            if CorrectItemData.QuestionID != QuestionData.ID:
                                result.Memo = 'question id error'
                                return result
                            # 答案必须为左侧选项ID
                            if CorrectItemData.Position == 2:
                                result.Memo = 'the answer must be the left option id'
                                return result
                    ScoreRatio = 1.00
                if QuestionData.QuestionType == 8:  # 连线题 ##################################################################
                    if Option == '':
                        result.Memo = 'wrong option'
                        return result
                    if Position <= 0:
                        result.Memo = 'wrong position'
                        return result
                    if Position == 1:  # 左侧为备选项 不能设置正确答案
                        CorrectItem = ''
                    CorrectAnswer = 1
                    if CorrectItem != '':
                        CorrectAnswer = 2
                    QuestionSolutionList: ResultList = self._questionSolutionModel.AllSolutions(_dbsession, QuestionData.ID)
                    if len(QuestionSolutionList.Data) > 0:
                        SolutionDataList: list = QuestionSolutionList.Data
                        # 判断重复选项
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            if SolutionData.Option == Option:
                                result.Memo = 'duplicate options'
                                return result
                        for i in SolutionDataList:
                            SolutionData: QuestionSolutionEntity = i
                            if SolutionData.CorrectItem != '' and SolutionData.CorrectItem == CorrectItem:
                                result.Memo = 'duplicate correct item'
                                return result
                        if CorrectItem != '':
                            CorrectItemList: list = CorrectItem.split(',')
                            for i in CorrectItemList:
                                SolutionID: str = i
                                # 答案是否存在于其他选项中
                                for j in SolutionDataList:
                                    SolutionData: QuestionSolutionEntity = j
                                    if SolutionID in SolutionData.CorrectItem:
                                        result.Memo = 'duplicate answer'
                                        return result
                                # 答案项是否存在
                                try:
                                    CorrectItemData: QuestionSolutionEntity = self._questionSolutionModel.Find(_dbsession, int(SolutionID))
                                except Exception as e:
                                    result.Memo = str(e)
                                    return result
                                if CorrectItemData is None:
                                    result.Memo = 'correct item data error'
                                    return result
                                # 答案项是否属于当前试题
                                if CorrectItemData.QuestionID != QuestionData.ID:
                                    result.Memo = 'question id data error'
                                    return result
                                # 答案必须为左侧选项ID
                                if CorrectItemData.Position == 2:
                                    result.Memo = 'the answer must be the left option id'
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
                    result.Memo = 'logging failed'
                    return result

                _dbsession.commit()
                result.State = True
        return result

    def QuestionSolutionAttachment(self, ClientHost: str, Token: str, ID: int, FileType: str, AttachmentContents: bytes) -> Result:
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
            QuestionSolutionData: QuestionSolutionEntity = self._questionSolutionModel.Find(_dbsession, ID)
            if QuestionSolutionData is None:
                result.Memo = 'question solution data error'
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

                Desc = 'update question solution attachment id:' + str(ID) + ' file path:' + UploadPath
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
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
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif ID <= 0:
            result.Memo = 'wrong id'
        else:
            QuestionSolutionData: QuestionSolutionEntity = self._questionSolutionModel.Find(_dbsession, ID)
            if QuestionSolutionData is None:
                result.Memo = 'question solution data error'
            else:
                _dbsession.begin_nested()

                DeleteInfo: Result = self._questionSolutionModel.Delete(_dbsession, ID)
                if DeleteInfo.State == False:
                    DeleteInfo.Memo = str(e)
                    return result

                Desc = 'delete question solution option&correct item:' + QuestionSolutionData.Option + '&' + QuestionSolutionData.CorrectItem
                if self.LogSysAction(_dbsession, 1, AdminID, Desc, ClientHost) == False:
                    result.Memo = 'logging failed'
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
            result.Memo = 'wrong token'
        elif AdminID == 0:
            result.Memo = 'permission denied'
        elif QuestionID <= 0:
            result.Memo = 'wrong question id'
        elif self._questionSolutionModel.Find(_dbsession, QuestionID) is None:
            result.Memo = 'question solution data error'
        else:
            result: ResultList = self._questionSolutionModel.List(_dbsession, Page, PageSize, QuestionID)
        return result