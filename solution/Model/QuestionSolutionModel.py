from Model.BaseModel import *


class QuestionSolutionModel(BaseModel):
    EType: QuestionSolutionEntity = QuestionSolutionEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Data: EType) -> Result:
        _result = Result()
        Data.Option = Data.Option.strip()
        Data.OptionAttachment = Data.OptionAttachment.strip()
        Data.CorrectAnswer = Data.CorrectAnswer.strip()
        if Data.QuestionID < 0:
            _result.Memo = 'param err'
            return _result
        if Data.Option == '':
            _result.Memo = 'param err'
            return _result
        if Data.OptionAttachment == '':
            _result.Memo = 'param err'
            return _result
        if Data.CorrectAnswer == '':
            _result.Memo = 'param err'
            return _result
        if Data.ScoreRatio <= 0:
            _result.Memo = 'param err'
            return _result
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
        Data = _dbsession.query(self.EType).filter(self.EType.ID == ID).first()
        if Data is not None:
            try:
                # Data.QuestionID = Param.QuestionID if Param.QuestionID > 0 else Data.QuestionID
                Data.Option = Param.Option.strip() if Param.Option.strip() != '' else Data.Option
                Data.OptionAttachment = Param.OptionAttachment.strip() if Param.OptionAttachment.strip() != '' else Data.OptionAttachment
                Data.CorrectAnswer = Param.CorrectAnswer.strip() if Param.CorrectAnswer.strip() != '' else Data.CorrectAnswer
                Data.ScoreRatio = Param.ScoreRatio if Param.ScoreRatio > 0 else Data.ScoreRatio
                Data.Position = Param.Position if Param.Position > 0 else Data.Position
                _dbsession.commit()
            except Exception as e:
                _result.Memo = str(e.orig)
                _dbsession.rollback()
                return _result
            _result.Status = True
        return _result

    def Find(self, _dbsession: DBsession, ID) -> Result:
        _result = Result()
        _result.Status = True
        _result.Data = _dbsession.query(self.EType).filter(self.EType.ID == ID).first()
        return _result

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, QuestionID: int) -> Result:
        _result = ResultList()
        _result.Status = True
        _result.Page = Page
        _result.PageSize = PageSize
        _result.TotalPage = math.ceil(_dbsession.query(self.EType).count() / PageSize)
        sql = _dbsession.query(self.EType)
        sql = sql.order_by(desc(self.EType.ID))
        if QuestionID > 0:
            sql = sql.filter(self.EType.QuestionID == QuestionID)
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result