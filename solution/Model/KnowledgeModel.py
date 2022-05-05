from Model.BaseModel import *


class ExamineeModel(BaseModel):
    EType: KnowledgeEntity = KnowledgeEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Data: EType) -> Result:
        _result = Result()
        Data.KnowledgeName = Data.KnowledgeName.strip()
        if Data.KnowledgeName == '':
            _result.Memo = 'param err'
            return _result
        if Data.SubjectID <= 0:
            _result.Memo = 'param err'
            return _result
        if Data.SubjectState <= 0:
            _result.Memo = 'param err'
            return _result
        Data.KnowledgeCode = self._common.StrMD5(Data.KnowledgeName.strip())
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
                Data.KnowledgeName = Param.KnowledgeName.strip() if Param.KnowledgeName.strip() != '' else Data.KnowledgeName
                Data.KnowledgeCode = self._common.StrMD5(Param.KnowledgeName.strip()) if Param.KnowledgeName.strip() != '' and Param.KnowledgeName.strip() != Data.KnowledgeName else Data.KnowledgeCode
                Data.SubjectID = Param.SubjectID if Param.SubjectID > 0 else Data.SubjectID
                Data.SubjectState = Param.SubjectState if Param.SubjectState > 0 else Data.SubjectState
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

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, Stext: str, SubjectID: int, SubjectState: int) -> Result:
        _result = ResultList()
        _result.Status = True
        _result.Page = Page
        _result.PageSize = PageSize
        _result.TotalPage = math.ceil(_dbsession.query(self.EType).count() / PageSize)
        sql = _dbsession.query(self.EType)
        sql = sql.order_by(desc(self.EType.ID))
        if Stext != '':
            sql = sql.filter(or_(self.EType.KnowledgeCode.ilike('%' + Stext.strip() + '%')))
        if SubjectID > 0:
            sql = sql.filter(self.EType.SubjectID == SubjectID)
        if SubjectState > 0:
            sql = sql.filter(self.EType.SubjectState == SubjectState)
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result