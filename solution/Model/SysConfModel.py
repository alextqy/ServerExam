# -*- coding:utf-8 -*-
from Model.BaseModel import *


class SysConfModel(BaseModel):
    EType: SysConfEntity = SysConfEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Data: EType) -> Result:
        _result = Result()
        Data.Key = Data.Key.strip()
        Data.Value = Data.Value.strip()
        Data.Description = Data.Description.strip()
        if Data.Type <= 0:
            _result.Memo = self._lang.ParamErr
            return _result
        if Data.Key == '':
            _result.Memo = self._lang.ParamErr
            return _result
        if Data.Value == '':
            _result.Memo = self._lang.ParamErr
            return _result
        if Data.Description == '':
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

        _result.State = True
        return _result

    def Find(self, _dbsession: DBsession, ID: int) -> EType:
        return _dbsession.query(self.EType).filter(self.EType.ID == ID).first()

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, Stext: str, Type: int) -> ResultList:
        _result = ResultList()
        _result.State = True
        _result.Page = Page
        _result.PageSize = PageSize
        _result.TotalPage = 0
        if _dbsession.query(self.EType).count() > 0:
            _result.TotalPage = math.ceil(_dbsession.query(self.EType).count() / PageSize)
        if Page <= 0:
            Page = 1
        if PageSize <= 0:
            PageSize = 10
        if _result.TotalPage > 0 and Page > _result.TotalPage:
            Page = _result.TotalPage
        sql = _dbsession.query(self.EType)
        sql = sql.order_by(desc(self.EType.ID))
        if Stext != '':
            sql = sql.filter(or_(self.EType.Key.ilike('%' + Stext.strip() + '%')))
        if Type > 0:
            sql = sql.filter(self.EType.Type == Type)
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result

    def FindKey(self, _dbsession: DBsession, Key: str) -> EType:
        return _dbsession.query(self.EType).filter(self.EType.Key == Key).first()