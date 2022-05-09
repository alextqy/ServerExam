from Model.BaseModel import *


class KnowledgeModel(BaseModel):
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
        # if Data.KnowledgeState <= 0:
        #     _result.Memo = 'param err'
        #     return _result
        Data.KnowledgeState = 1
        Data.KnowledgeCode = self._common.StrMD5(Data.KnowledgeName.strip())
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
        Data: KnowledgeEntity = _dbsession.query(self.EType).filter(self.EType.ID == ID).first()
        if Data is not None:
            try:
                Data.KnowledgeName = Param.KnowledgeName.strip() if Param.KnowledgeName.strip() != '' else Data.KnowledgeName
                Data.KnowledgeCode = self._common.StrMD5(Param.KnowledgeName.strip()) if Param.KnowledgeName.strip() != '' and Param.KnowledgeName.strip() != Data.KnowledgeName else Data.KnowledgeCode
                Data.SubjectID = Param.SubjectID if Param.SubjectID > 0 else Data.SubjectID
                Data.KnowledgeState = Param.KnowledgeState if Param.KnowledgeState > 0 else Data.KnowledgeState
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

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, Stext: str, SubjectID: int, KnowledgeState: int) -> ResultList:
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
            sql = sql.filter(or_(self.EType.KnowledgeCode.ilike('%' + self._common.StrMD5(Stext.strip()) + '%')))
        if SubjectID > 0:
            sql = sql.filter(self.EType.SubjectID == SubjectID)
        if KnowledgeState > 0:
            sql = sql.filter(self.EType.KnowledgeState == KnowledgeState)
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result

    def FindKnowledgeName(self, _dbsession: DBsession, KnowledgeName: str) -> EType:
        return _dbsession.query(self.EType).filter(self.EType.KnowledgeName == KnowledgeName.strip()).first()