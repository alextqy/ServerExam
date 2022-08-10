# -*- coding:utf-8 -*-
from Model.BaseModel import *


class TeacherClassModel(BaseModel):
    EType: TeacherClassEntity = TeacherClassEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Data: EType) -> Result:
        _result = Result()
        if Data.TeacherID <= 0:
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

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, TeacherID: int, ClassID: int) -> ResultList:
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
        if TeacherID > 0:
            sql = sql.filter(self.EType.TeacherID == TeacherID)
        if ClassID > 0:
            sql = sql.filter(self.EType.ClassID == ClassID)
        if sql.count() > 0:
            _result.TotalPage = math.ceil(sql.count() / PageSize)
        if _result.TotalPage > 0 and Page > _result.TotalPage:
            Page = _result.TotalPage
        DataList = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        for i in DataList:
            i.Password = ''
            i.Token = ''
        _result.Data = DataList
        return _result

    def CheckClass(self, _dbsession: DBsession, ClassID: int) -> list:
        return _dbsession.query(self.EType).filter(self.EType.ClassID == ClassID).all()

    def CheckTeacher(self, _dbsession: DBsession, TeacherID: int) -> list:
        return _dbsession.query(self.EType).filter(self.EType.TeacherID == TeacherID).all()

    def CheckData(self, _dbsession: DBsession, TeacherID: int, ClassID: int) -> EType:
        return _dbsession.query(self.EType).filter(self.EType.TeacherID == TeacherID).filter(self.EType.ClassID == ClassID).first()