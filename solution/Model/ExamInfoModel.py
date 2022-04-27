from Model.BaseModel import *


class ExamineeModel(BaseModel):
    EType: ExamInfoEntity = ExamInfoEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Data: EType) -> Result:
        _result = Result()
        if Data.SubjectName == '':
            _result.Memo = 'param err'
            return _result
        if Data.ExamNo == '':
            _result.Memo = 'param err'
            return _result
        if Data.TotalScore <= 0:
            _result.Memo = 'param err'
            return _result
        if Data.PassLine <= 0:
            _result.Memo = 'param err'
            return _result
        # if Data.ActualScore <= 0:
        #     _result.Memo = 'param err'
        #     return _result
        if Data.ExamDuration <= 0:
            _result.Memo = 'param err'
            return _result
        # if Data.StartTime <= 0:
        #     _result.Memo = 'param err'
        #     return _result
        # if Data.EndTime <= 0:
        #     _result.Memo = 'param err'
        #     return _result
        # if Data.ActualDuration <= 0:
        #     _result.Memo = 'param err'
        #     return _result
        if Data.Pass <= 0:
            _result.Memo = 'param err'
            return _result
        if Data.ExamineeID <= 0:
            _result.Memo = 'param err'
            return _result

        Data.SubjectName = Data.SubjectName.strip()
        Data.ExamNo = Data.ExamNo.strip()
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
                Data.SubjectName = Param.SubjectName.strip() if Param.SubjectName != '' else Data.SubjectName
                Data.ExamNo = Param.ExamNo.strip() if Param.ExamNo != '' else Data.ExamNo
                Data.TotalScore = Param.TotalScore if Param.TotalScore > 0 else Data.TotalScore
                Data.PassLine = Param.PassLine if Param.PassLine > 0 else Data.PassLine
                Data.ActualScore = Param.ActualScore if Param.ActualScore > 0 else Data.ActualScore
                Data.ExamDuration = Param.ExamDuration if Param.ExamDuration > 0 else Data.ExamDuration
                Data.TotalScore = Param.TotalScore if Param.TotalScore > 0 else Data.TotalScore
                Data.TotalScore = Param.TotalScore if Param.TotalScore > 0 else Data.TotalScore
                Data.TotalScore = Param.TotalScore if Param.TotalScore > 0 else Data.TotalScore
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

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, Stext: str) -> Result:
        _result = ResultList()
        _result.Status = True
        _result.Page = Page
        _result.PageSize = PageSize
        _result.TotalPage = math.ceil(_dbsession.query(self.EType).count() / PageSize)
        sql = _dbsession.query(self.EType)
        sql = sql.order_by(desc(self.EType.ID))
        # if Stext != '':
        #     sql = sql.filter(or_(self.EType.Name.ilike('%' + Stext.strip() + '%'), self.EType.ExamineeNo.ilike('%' + Stext.strip() + '%')))
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result