# -*- coding:utf-8 -*-
from Model.BaseModel import *


class ExamineeModel(BaseModel):
    EType: ExamineeEntity = ExamineeEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Data: EType):
        _result = Result()
        Data.CreateTime = self._common.Time()
        Data.Name = Data.Name.strip()
        Data.ExamineeNo = Data.ExamineeNo.strip()
        # Data.Contact = Data.Contact.strip()
        if Data.Name == '':
            _result.Memo = self._lang.ParamErr
            return _result
        if Data.ExamineeNo == '':
            _result.Memo = self._lang.ParamErr
            return _result
        if Data.ClassID <= 0:
            _result.Memo = self._lang.ParamErr
            return _result
        try:
            _dbsession.add(Data)
            _dbsession.commit()
            _dbsession.flush()
        except Exception as e:
            _result.Memo = str(e)
            _dbsession.rollback()
            return _result

        _result.State = True
        _result.Data = Data.ID
        return _result

    def Delete(self, _dbsession: DBsession, ID: int):
        _result = Result()
        try:
            Data = _dbsession.query(self.EType).filter(self.EType.ID == ID).first()
            _dbsession.delete(Data)
            _dbsession.commit()
        except Exception as e:
            _result.Memo = str(e)
            _dbsession.rollback()
            return _result

        _result.State = True
        return _result

    def Find(self, _dbsession: DBsession, ID: int) -> EType:
        return _dbsession.query(self.EType).filter(self.EType.ID == ID).first()

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, Stext: str, ClassID: int):
        _result = ResultList()
        _result.State = True
        _result.Page = Page
        _result.PageSize = PageSize
        _result.TotalPage = 0
        if Page <= 0:
            Page = 1
        if PageSize <= 0:
            PageSize = 10
        sql = _dbsession.query(self.EType)
        sql = sql.order_by(desc(self.EType.ID))
        if Stext != '':
            sql = sql.filter(or_(self.EType.Name.ilike('%' + Stext.strip() + '%'), self.EType.ExamineeNo.ilike('%' + Stext.strip() + '%')))
        if ClassID > 0:
            sql = sql.filter(self.EType.ClassID == ClassID)
        if sql.count() > 0:
            _result.TotalPage = math.ceil(sql.count() / PageSize)
        if _result.TotalPage > 0 and Page > _result.TotalPage:
            Page = _result.TotalPage
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result

    def FindExamineeNo(self, _dbsession: DBsession, ExamineeNo: str) -> EType:
        return _dbsession.query(self.EType).filter(self.EType.ExamineeNo == ExamineeNo).first()

    def Examinees(self, _dbsession: DBsession):
        _result = Result()
        _result.State = True
        sql = _dbsession.query(self.EType)
        _result.Data = sql.all()
        return _result