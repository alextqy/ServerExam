from Model.BaseModel import *


class ExamineeModel(BaseModel):
    EType: ExamineeEntity = ExamineeEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Data: EType) -> Result:
        _result = Result()
        Data.Name = Data.Name.strip()
        Data.ExamineeNo = Data.ExamineeNo.strip()
        Data.Contact = Data.Contact.strip()
        if Data.Name == '':
            _result.Memo = 'param err'
            return _result
        if Data.ExamineeNo == '':
            _result.Memo = 'param err'
            return _result
        # if Data.Contact == '':
        #     _result.Memo = 'param err'
        #     return _result
        if Data.ClassID <= 0:
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
        Data: ExamineeEntity = _dbsession.query(self.EType).filter(self.EType.ID == ID).first()
        if Data is not None:
            try:
                Data.Name = Param.Name.strip() if Param.Name.strip() != '' else Data.Name
                Data.ExamineeNo = Param.ExamineeNo.strip() if Param.ExamineeNo.strip() != '' else Data.ExamineeNo
                Data.Contact = Param.Contact.strip() if Param.Contact.strip() != '' else Data.Contact
                Data.ClassID = Param.ClassID if Param.ClassID > 0 else Data.ClassID
                _dbsession.commit()
            except Exception as e:
                _result.Memo = str(e)
                _dbsession.rollback()
                return _result
            _result.Status = True
        return _result

    def Find(self, _dbsession: DBsession, ID: int) -> EType:
        return _dbsession.query(self.EType).filter(self.EType.ID == ID).first()

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, Stext: str, ClassID: int) -> ResultList:
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
            sql = sql.filter(or_(self.EType.Name.ilike('%' + Stext.strip() + '%'), self.EType.ExamineeNo.ilike('%' + Stext.strip() + '%')))
        if ClassID > 0:
            sql = sql.filter(self.EType.ClassID == ClassID)
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result