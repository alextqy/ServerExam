from Model.BaseModel import *


class ExamineeModel(BaseModel):
    DBType: ExamineeEntity = ExamineeEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Name: str, ExamineeNo: str, Contact: str) -> Result:
        _result = Result()
        if Name == '':
            _result.Memo = 'param err'
            return _result
        if ExamineeNo == '':
            _result.Memo = 'param err'
            return _result

        Examinee = self.DBType()
        Examinee.Name = Name.strip()
        Examinee.ExamineeNo = ExamineeNo.strip()
        Examinee.Contact = Contact.strip()
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

    def Update(self, _dbsession: DBsession, ID: int, Name: str, ExamineeNo: str, Contact: str) -> Result:
        _result = Result()
        try:
            Data = _dbsession.query(self.DBType).filter(self.DBType.ID == ID).first()
            Data.Name = Name.strip() if Name != '' else Data.Name
            Data.ExamineeNo = ExamineeNo.strip() if ExamineeNo != '' else Data.ExamineeNo
            Data.Contact = Contact.strip() if Contact != '' else Data.Contact
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

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, Stext: str) -> Result:
        _result = ResultList()
        _result.Status = True
        _result.Page = Page
        _result.PageSize = PageSize
        _result.TotalPage = math.ceil(_dbsession.query(self.DBType).count() / PageSize)
        sql = _dbsession.query(self.DBType)
        sql = sql.order_by(desc(self.DBType.ID))
        if Stext != '':
            sql = sql.filter(or_(self.DBType.Name.ilike('%' + Stext.strip() + '%'), self.DBType.ExamineeNo.ilike('%' + Stext.strip() + '%')))
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result