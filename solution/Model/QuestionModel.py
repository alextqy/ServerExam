from Model.BaseModel import *


class QuestionModel(BaseModel):
    EType: QuestionEntity = QuestionEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Data: EType) -> Result:
        _result = Result()
        Data.QuestionTitle = Data.QuestionTitle.strip()
        Data.Description = Data.Description.strip()
        if Data.QuestionTitle == '':
            _result.Memo = 'param err'
            return _result
        if Data.QuestionType <= 0:
            _result.Memo = 'param err'
            return _result
        # if Data.QuestionState <= 0:
        #     _result.Memo = 'param err'
        #     return _result
        # if Data.Marking <= 0:
        #     _result.Memo = 'param err'
        #     return _result
        if Data.KnowledgeID <= 0:
            _result.Memo = 'param err'
            return _result
        Data.QuestionState = 2
        Data.Marking = 1
        Data.QuestionCode = self._common.StrMD5(Data.QuestionTitle.strip())
        try:
            _dbsession.add(Data)
            _dbsession.commit()
            _dbsession.flush()
        except Exception as e:
            _result.Memo = str(e)
            _dbsession.rollback()
            return _result

        _result.State = True
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

        _result.State = True
        return _result

    def Find(self, _dbsession: DBsession, ID: int) -> EType:
        return _dbsession.query(self.EType).filter(self.EType.ID == ID).first()

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, Stext: str, QuestionType: int, QuestionState: int, Marking: int, KnowledgeID: int) -> ResultList:
        _result = ResultList()
        _result.State = True
        _result.Page = Page
        _result.PageSize = PageSize
        _result.TotalPage = 0
        if _dbsession.query(self.EType).count() > 0:
            _result.TotalPage = math.ceil(_dbsession.query(self.EType).count() / PageSize)
        if Page <= 0:
            Page = 1
        if PageSize <= 0:
            PageSize = 10
        if _result.TotalPage > 0 and Page > _result.TotalPage:
            Page = _result.TotalPage
        sql = _dbsession.query(self.EType)
        sql = sql.order_by(desc(self.EType.ID))
        if Stext != '':
            sql = sql.filter(or_(self.EType.QuestionCode.ilike('%' + self._common.StrMD5(Stext.strip()) + '%')))
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

    def CountType(self, _dbsession: DBsession, KnowledgeID: int, QuestionType: int) -> int:
        return _dbsession.query(self.EType).filter(self.EType.KnowledgeID == KnowledgeID).filter(self.EType.QuestionType == QuestionType).filter(self.EType.QuestionState == 1).count()