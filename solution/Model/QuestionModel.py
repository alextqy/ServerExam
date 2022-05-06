from Model.BaseModel import *


class QuestionModel(BaseModel):
    EType: QuestionEntity = QuestionEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Data: EType) -> Result:
        _result = Result()
        Data.QuestionTitle = Data.QuestionTitle.strip()
        Data.Description = Data.Description.strip()
        Data.Attachment = Data.Attachment.strip()
        if Data.QuestionTitle == '':
            _result.Memo = 'param err'
            return _result
        if Data.QuestionType <= 0:
            _result.Memo = 'param err'
            return _result
        if Data.QuestionState <= 0:
            _result.Memo = 'param err'
            return _result
        if Data.Marking <= 0:
            _result.Memo = 'param err'
            return _result
        if Data.KnowledgeID <= 0:
            _result.Memo = 'param err'
            return _result
        Data.QuestionCode = self._common.StrMD5(Data.QuestionTitle.strip())
        try:
            _dbsession.add(Data)
            _dbsession.commit()
            _dbsession.flush()
        except Exception as e:
            _result.Memo = str(e.orig)
            _dbsession.rollback()
            return _result

        _result.Status = True
        _result.Data = Data.ID
        return _result

    def Delete(self, _dbsession: DBsession, ID: int) -> Result:
        _result = Result()
        try:
            Data = _dbsession.query(self.EType).filter(self.EType.ID == ID).first()
            _dbsession.delete(Data)
            _dbsession.commit()
        except Exception as e:
            _result.Memo = str(e)
            _dbsession.rollback()
            return _result

        _result.Status = True
        return _result

    def Update(self, _dbsession: DBsession, ID: int, Param: EType) -> Result:
        _result = Result()
        Data: QuestionEntity = _dbsession.query(self.EType).filter(self.EType.ID == ID).first()
        if Data is not None:
            try:
                Data.QuestionTitle = Param.QuestionTitle.strip() if Param.QuestionTitle.strip() != '' else Data.QuestionTitle
                Data.QuestionCode = self._common.StrMD5(Param.QuestionTitle.strip()) if Param.QuestionTitle.strip() != '' and Param.QuestionTitle.strip() != Data.QuestionTitle else Data.QuestionCode
                Data.QuestionType = Param.QuestionType if Param.QuestionType > 0 else Data.QuestionType
                Data.QuestionState = Param.QuestionState if Param.QuestionState > 0 else Data.QuestionState
                Data.Marking = Param.Marking if Param.Marking > 0 else Data.Marking
                Data.KnowledgeID = Param.KnowledgeID if Param.KnowledgeID > 0 else Data.KnowledgeID
                Data.Description = Param.Description if Param.Description.strip() != '' else Data.Description
                Data.Attachment = Param.Attachment if Param.Attachment.strip() != '' else Data.Attachment
                Data.UpdateTime = self._common.Time()
                _dbsession.commit()
            except Exception as e:
                _result.Memo = str(e.orig)
                _dbsession.rollback()
                return _result
            _result.Status = True
        return _result

    def Find(self, _dbsession: DBsession, ID: int) -> Result:
        _result = Result()
        _result.Status = True
        _result.Data = _dbsession.query(self.EType).filter(self.EType.ID == ID).first()
        return _result

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, Stext: str, QuestionType: int, QuestionState: int, Marking: int, KnowledgeID: int) -> Result:
        _result = ResultList()
        _result.Status = True
        _result.Page = Page
        _result.PageSize = PageSize
        _result.TotalPage = math.ceil(_dbsession.query(self.EType).count() / PageSize)
        sql = _dbsession.query(self.EType)
        sql = sql.order_by(desc(self.EType.ID))
        if Stext != '':
            sql = sql.filter(or_(self.EType.QuestionCode.ilike('%' + Stext.strip() + '%')))
        if QuestionType > 0:
            sql = sql.filter(self.EType.QuestionType == QuestionType)
        if QuestionState > 0:
            sql = sql.filter(self.EType.QuestionState == QuestionState)
        if Marking > 0:
            sql = sql.filter(self.EType.Marking == Marking)
        if KnowledgeID > 0:
            sql = sql.filter(self.EType.KnowledgeID == KnowledgeID)
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result