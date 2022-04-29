from Model.BaseModel import *


class SysLogModel(BaseModel):
    EType: SysLogEntity = SysLogEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Data: EType) -> Result:
        _result = Result()
        Data.Description = Data.Description.strip()
        Data.IP = Data.IP.strip()
        if Data.Type <= 0:
            _result.Memo = 'param err'
            return _result
        if Data.ManagerID <= 0:
            _result.Memo = 'param err'
            return _result
        if Data.Description == '':
            _result.Memo = 'param err'
            return _result
        if Data.IP == '':
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
                Data.Name = Param.Name.strip() if Param.Name.strip() != '' else Data.Name
                Data.ExamineeNo = Param.ExamineeNo.strip() if Param.ExamineeNo.strip() != '' else Data.ExamineeNo
                Data.Contact = Param.Contact.strip() if Param.Contact.strip() != '' else Data.Contact
                Data.ClassID = Param.ClassID if Param.ClassID > 0 else Data.ClassID
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

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, Stext: str, Type: int, ManagerID: int) -> Result:
        _result = ResultList()
        _result.Status = True
        _result.Page = Page
        _result.PageSize = PageSize
        _result.TotalPage = math.ceil(_dbsession.query(self.EType).count() / PageSize)
        sql = _dbsession.query(self.EType)
        sql = sql.order_by(desc(self.EType.ID))
        if Stext != '':
            sql = sql.filter(or_(self.EType.IP.ilike('%' + Stext.strip() + '%')))
        if Type > 0:
            sql = sql.filter(self.EType.Type == Type)
        if ManagerID > 0:
            sql = sql.filter(self.EType.ManagerID == ManagerID)
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result