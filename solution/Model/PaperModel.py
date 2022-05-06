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
        if Data.PaperState <= 0:
            _result.Memo = 'param err'
            return _result
        Data.PaperCode = self._common.StrMD5(Data.PaperName.strip())
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
        Data: PaperEntity = _dbsession.query(self.EType).filter(self.EType.ID == ID).first()
        if Data is not None:
            try:
                Data.PaperName = Param.PaperName.strip() if Param.PaperName.strip() != '' else Data.PaperName
                Data.PaperCode = self._common.StrMD5(Param.PaperName.strip()) if Param.PaperName.strip() != '' and Param.PaperName.strip() != Data.PaperName else Data.PaperCode
                Data.SubjectID = Param.SubjectID if Param.SubjectID > 0 else Data.SubjectID
                Data.TotalScore = Param.TotalScore if Param.TotalScore > 0 else Data.TotalScore
                Data.PassLine = Param.PassLine if Param.PassLine > 0 else Data.PassLine
                Data.ExamDuration = Param.ExamDuration if Param.ExamDuration > 0 else Data.ExamDuration
                Data.PaperState = Param.PaperState if Param.PaperState > 0 else Data.PaperState
                Data.UpdateTime = self._common.Time()
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

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, Stext: str, SubjectID: int, PaperState: int) -> Result:
        _result = ResultList()
        _result.Status = True
        _result.Page = Page
        _result.PageSize = PageSize
        _result.TotalPage = math.ceil(_dbsession.query(self.EType).count() / PageSize)
        sql = _dbsession.query(self.EType)
        sql = sql.order_by(desc(self.EType.ID))
        if Stext != '':
            sql = sql.filter(or_(self.EType.PaperCode.ilike('%' + Stext.strip() + '%')))
        if SubjectID > 0:
            sql = sql.filter(self.EType.SubjectID == SubjectID)
        if PaperState > 0:
            sql = sql.filter(self.EType.PaperState == PaperState)
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result