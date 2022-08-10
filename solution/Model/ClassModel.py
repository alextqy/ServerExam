# -*- coding:utf-8 -*-
from Model.BaseModel import *


class ClassModel(BaseModel):
    EType: ClassEntity = ClassEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Data: EType) -> Result:
        _result = Result()
        Data.ClassName = Data.ClassName.strip()
        Data.Description = Data.Description.strip()
        if Data.ClassName == '':
            _result.Memo = self._lang.ParamErr
            return _result
        if Data.Description == '':
            Data.Description = 'none'
        Data.ClassCode = self._common.StrMD5(Data.ClassName.strip())
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

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, Stext: str) -> ResultList:
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
            sql = sql.filter(or_(self.EType.ClassName.ilike('%' + Stext.strip() + '%')))
        if sql.count() > 0:
            _result.TotalPage = math.ceil(sql.count() / PageSize)
        if _result.TotalPage > 0 and Page > _result.TotalPage:
            Page = _result.TotalPage
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result

    def FindClassName(self, _dbsession: DBsession, ClassName: str) -> EType:
        return _dbsession.query(self.EType).filter(self.EType.ClassName == ClassName.strip()).first()

    def FindClassCode(self, _dbsession: DBsession, ClassName: str) -> EType:
        return _dbsession.query(self.EType).filter(self.EType.ClassCode == self._common.StrMD5(ClassName.strip())).first()

    def Classes(self, _dbsession: DBsession) -> ResultList:
        _result = ResultList()
        _result.State = True
        sql = _dbsession.query(self.EType)
        _result.Data = sql.all()
        return _result