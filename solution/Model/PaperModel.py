from Model.BaseModel import *


class PaperModel(BaseModel):
    EType: PaperEntity = PaperEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Data: EType) -> Result:
        _result = Result()
        Data.PaperName = Data.PaperName.strip()
        if Data.PaperName == '':
            _result.Memo = 'param err'
            return _result
        if Data.SubjectID <= 0:
            _result.Memo = 'param err'
            return _result
        if Data.TotalScore <= 0:
            _result.Memo = 'param err'
            return _result
        if Data.PassLine <= 0:
            _result.Memo = 'param err'
            return _result
        if Data.ExamDuration <= 0:
            _result.Memo = 'param err'
            return _result
        # if Data.PaperState <= 0:
        #     _result.Memo = 'param err'
        #     return _result

        Data.ExamDuration *= 60
        Data.PaperState = 1
        Data.PaperCode = self._common.StrMD5(Data.PaperName.strip())
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

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, Stext: str, SubjectID: int, PaperState: int) -> ResultList:
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
        if Stext != '':
            sql = sql.filter(or_(self.EType.PaperCode.ilike('%' + self._common.StrMD5(Stext.strip()) + '%')))
        if SubjectID > 0:
            sql = sql.filter(self.EType.SubjectID == SubjectID)
        if PaperState > 0:
            sql = sql.filter(self.EType.PaperState == PaperState)
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result

    def FindPaperCode(self, _dbsession: DBsession, PaperName: str) -> EType:
        return _dbsession.query(self.EType).filter(self.EType.PaperCode == self._common.StrMD5(PaperName)).first()