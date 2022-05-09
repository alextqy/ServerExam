from Model.BaseModel import *


class ScantronHistoryModel(BaseModel):
    EType: ScantronHistoryEntity = ScantronHistoryEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Data: EType) -> Result:
        _result = Result()
        Data.QuestionTitle = Data.QuestionTitle.strip()
        Data.Description = Data.Description.strip()
        Data.Attachment = Data.Attachment.strip()
        Data.HeadlineContent = Data.HeadlineContent.strip()
        if Data.HeadlineContent == '':
            if Data.QuestionTitle == '':
                _result.Memo = 'param err'
                return _result
        if Data.QuestionTitle == '':
            if Data.HeadlineContent == '':
                _result.Memo = 'param err'
                return _result
        Data.QuestionCode = self._common.StrMD5(Data.QuestionTitle.strip())
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

    def Find(self, _dbsession: DBsession, ID: int) -> EType:
        return _dbsession.query(self.EType).filter(self.EType.ID == ID).first()

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, ExamID: int) -> ResultList:
        _result = ResultList()
        _result.Status = True
        _result.Page = Page
        _result.PageSize = PageSize
        _result.TotalPage = math.ceil(_dbsession.query(self.EType).count() / PageSize)
        if Page <= 0:
            Page = 1
        if PageSize <= 0:
            PageSize = 10
        if Page > _result.TotalPage:
            Page = _result.TotalPage
        sql = _dbsession.query(self.EType)
        sql = sql.order_by(desc(self.EType.ID))
        if ExamID > 0:
            sql = sql.filter(self.EType.ExamID == ExamID)
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result