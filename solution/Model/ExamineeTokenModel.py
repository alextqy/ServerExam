from Model.BaseModel import *


class ExamineeTokenModel(BaseModel):
    DBType: ExamineeTokenEntity = ExamineeTokenEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Token: str, ExamID: str) -> Result:
        _result = Result()
        if Token == '':
            _result.Memo = 'param err'
            return _result
        if ExamID == '':
            _result.Memo = 'param err'
            return _result

        Examinee = self.DBType()
        Examinee.Token = Token.strip()
        Examinee.ExamID = ExamID.strip()
        try:
            _dbsession.add(Examinee)
            _dbsession.commit()
            _dbsession.flush()
        except Exception as e:
            _result.Memo = str(e.orig)
            _dbsession.rollback()
            return _result

        _result.Status = True
        _result.Data = Examinee.ID
        return _result

    def Delete(self, _dbsession: DBsession, ID: int) -> Result:
        _result = Result()
        try:
            Data = _dbsession.query(self.DBType).filter(self.DBType.ID == ID).first()
            _dbsession.delete(Data)
            _dbsession.commit()
        except Exception as e:
            _result.Memo = str(e)
            _dbsession.rollback()
            return _result

        _result.Status = True
        return _result

    def Update(self, _dbsession: DBsession, ID: int, Token: str, ExamID: int) -> Result:
        _result = Result()
        try:
            Data = _dbsession.query(self.DBType).filter(self.DBType.ID == ID).first()
            Data.Token = Token if Token != '' else Data.Token
            Data.ExamID = ExamID if ExamID != '' else Data.ExamID
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
        _result.Data = _dbsession.query(self.DBType).filter(self.DBType.ID == ID).first()
        return _result

    def List(self, _dbsession: DBsession, Page: int, PageSize: int) -> Result:
        _result = ResultList()
        _result.Status = True
        _result.Page = Page
        _result.PageSize = PageSize
        _result.TotalPage = math.ceil(_dbsession.query(self.DBType).count() / PageSize)
        sql = _dbsession.query(self.DBType)
        sql = sql.order_by(desc(self.DBType.ID))
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result