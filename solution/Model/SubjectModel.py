# -*- coding:utf-8 -*-
from Model.BaseModel import *


class SubjectModel(BaseModel):
    EType: SubjectEntity = SubjectEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Data: EType) -> Result:
        _result = Result()
        Data.CreateTime = self._common.Time()
        Data.SubjectName = Data.SubjectName.strip()
        if Data.SubjectName == '':
            _result.Memo = self._lang.ParamErr
            return _result
        # if Data.SubjectState <= 0:
        #     _result.Memo = self._lang.ParamErr
        #     return _result
        Data.SubjectState = 1
        Data.SubjectCode = self._common.StrMD5(Data.SubjectName.strip())
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

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, Stext: str, SubjectState: int) -> ResultList:
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
            sql = sql.filter(or_(self.EType.SubjectName.ilike('%' + Stext.strip() + '%')))
        if SubjectState > 0:
            sql = sql.filter(self.EType.SubjectState == SubjectState)
        if sql.count() > 0:
            _result.TotalPage = math.ceil(sql.count() / PageSize)
        if _result.TotalPage > 0 and Page > _result.TotalPage:
            Page = _result.TotalPage
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result

    def FindSubjectCode(self, _dbsession: DBsession, SubjectName: str) -> EType:
        return _dbsession.query(self.EType).filter(self.EType.SubjectCode == self._common.StrMD5(SubjectName.strip())).first()

    # def FindSubjectName(self, _dbsession: DBsession, SubjectName: str) -> EType:
    #     return _dbsession.query(self.EType).filter(self.EType.SubjectName == SubjectName.strip()).first()

    # def SubjectList(self, _dbsession: DBsession, SubjectState: int = 1) -> list:
    #     return _dbsession.query(self.EType).filter(self.EType.SubjectState == SubjectState).all()

    def Subjects(self, _dbsession: DBsession) -> ResultList:
        _result = ResultList()
        _result.State = True
        sql = _dbsession.query(self.EType)
        sql = sql.filter(self.EType.SubjectState == 1)
        _result.Data = sql.all()
        return _result