from Model.BaseModel import *
from Entity.ExamineeEntity import ExamineeEntity


class ExamineeModel(BaseModel):

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Name: str, ExamineeNo: str, Contact: str) -> Result:
        _result = Result()
        Examinee = ExamineeEntity()
        Examinee.Name = Name
        Examinee.ExamineeNo = ExamineeNo
        Examinee.Contact = Contact
        Examinee.CreateTime = self._common.Time()
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
            Data = _dbsession.query(ExamineeEntity).filter(ExamineeEntity.ID == ID).first()
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
            Data = _dbsession.query(ExamineeEntity).filter(ExamineeEntity.ID == ID).first()
            Data.Name = Name if Name != '' else Data.Name
            Data.ExamineeNo = ExamineeNo if ExamineeNo != '' else Data.ExamineeNo
            Data.Contact = Contact if Contact != '' else Data.Contact
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
        _result.Data = _dbsession.query(ExamineeEntity).filter(ExamineeEntity.ID == ID).first()
        return _result

    def List(self, _dbsession: DBsession, Page: int, PageSize: int) -> Result:
        _result = ResultList()
        _result.Status = True
        _result.Page = Page
        _result.PageSize = PageSize
        _result.TotalPage = math.ceil(_dbsession.query(ExamineeEntity).count() / PageSize)
        _result.Data = _dbsession.query(ExamineeEntity).order_by(desc(ExamineeEntity.ID)).limit(PageSize).offset(Page * PageSize).all()
        return _result