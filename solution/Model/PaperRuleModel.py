from Model.BaseModel import *


class PaperRuleModel(BaseModel):
    EType: PaperRuleEntity = PaperRuleEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Data: EType) -> Result:
        _result = Result()
        if Data.HeadlineID <= 0:
            if Data.QuestionType <= 0:
                _result.Memo = 'param err'
                return _result
            if Data.QuestionNum <= 0:
                _result.Memo = 'param err'
                return _result
            if Data.SingleScore <= 0:
                _result.Memo = 'param err'
                return _result
            if Data.PaperID <= 0:
                _result.Memo = 'param err'
                return _result
        if Data.QuestionType <= 0:
            if Data.HeadlineID <= 0:
                _result.Memo = 'param err'
                return _result
        if Data.PaperRuleState <= 0:
            _result.Memo = 'param err'
            return _result
        try:
            _dbsession.add(Data)
            _dbsession.commit()
            _dbsession.flush()
        except Exception as e:
            _result.Memo = str(e)
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
        Data: PaperRuleEntity = _dbsession.query(self.EType).filter(self.EType.ID == ID).first()
        if Data is not None:
            try:
                Data.HeadlineID = Param.HeadlineID if Param.HeadlineID > 0 else Data.HeadlineID
                Data.QuestionType = Param.QuestionType if Param.QuestionType > 0 else Data.QuestionType
                Data.QuestionNum = Param.QuestionNum if Param.QuestionNum > 0 else Data.QuestionNum
                Data.SingleScore = Param.SingleScore if Param.SingleScore > 0 else Data.SingleScore
                Data.PaperID = Param.PaperID if Param.PaperID > 0 else Data.PaperID
                Data.PaperRuleState = Param.PaperRuleState if Param.PaperRuleState > 0 else Data.PaperRuleState
                Data.UpdateTime = self._common.Time()
                _dbsession.commit()
            except Exception as e:
                _result.Memo = str(e)
                _dbsession.rollback()
                return _result
            _result.Status = True
        return _result

    def Find(self, _dbsession: DBsession, ID: int) -> EType:
        return _dbsession.query(self.EType).filter(self.EType.ID == ID).first()

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, PaperID: int, PaperRuleState: int) -> Result:
        _result = ResultList()
        _result.Status = True
        _result.Page = Page
        _result.PageSize = PageSize
        _result.TotalPage = math.ceil(_dbsession.query(self.EType).count() / PageSize)
        sql = _dbsession.query(self.EType)
        sql = sql.order_by(desc(self.EType.ID))
        sql = sql.filter(self.EType.PaperID == PaperID)
        sql = sql.filter(self.EType.PaperRuleState == PaperRuleState)
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result