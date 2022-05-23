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
                        # 试卷选项分析
                        
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
        elif Description == '':
            result.Memo = 'wrong description'
        else:
            QuestionData: QuestionEntity = self._questionModel.Find(_dbsession, ID)
            if QuestionData is None:
                result.Memo = 'data error'
            else:
                _dbsession.begin_nested()

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