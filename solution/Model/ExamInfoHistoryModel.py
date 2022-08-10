# -*- coding:utf-8 -*-
from Model.BaseModel import *


class ExamInfoHistoryModel(BaseModel):
    EType: ExamInfoHistoryEntity = ExamInfoHistoryEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Data: EType) -> Result:
        _result = Result()
        Data.SubjectName = Data.SubjectName.strip()
        Data.ExamNo = Data.ExamNo.strip()
        if Data.SubjectName == '':
            _result.Memo = self._lang.ParamErr
            return _result
        if Data.ExamNo == '':
            _result.Memo = self._lang.ParamErr
            return _result
        # if Data.TotalScore <= 0:
        #     _result.Memo = self._lang.ParamErr
        #     return _result
        # if Data.PassLine <= 0:
        #     _result.Memo = self._lang.ParamErr
        #     return _result
        # if Data.ActualScore <= 0:
        #     _result.Memo = self._lang.ParamErr
        #     return _result
        # if Data.ExamDuration <= 0:
        #     _result.Memo = self._lang.ParamErr
        #     return _result
        # if Data.StartTime <= 0:
        #     _result.Memo = self._lang.ParamErr
        #     return _result
        # if Data.EndTime <= 0:
        #     _result.Memo = self._lang.ParamErr
        #     return _result
        # if Data.ActualDuration <= 0:
        #     _result.Memo = self._lang.ParamErr
        #     return _result
        # if Data.Pass <= 0:
        #     _result.Memo = self._lang.ParamErr
        #     return _result
        # if Data.ExamineeID <= 0:
        #     _result.Memo = self._lang.ParamErr
        #     return _result
        # if Data.ExamState <= 0:
        #     _result.Memo = self._lang.ParamErr
        #     return _result
        if Data.ExamType <= 0:
            _result.Memo = self._lang.ParamErr
            return _result
        if Data.Pass <= 0:
            Data.Pass = 1
        if Data.ExamState <= 0:
            Data.ExamState = 1
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

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, Stext: str, ExamState: int, ExamType: int, Pass: int) -> ResultList:
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
            sql = sql.filter(or_(self.EType.SubjectName.ilike('%' + Stext.strip() + '%'), self.EType.ExamNo.ilike('%' + Stext.strip() + '%')))
        if ExamState > 0:
            sql = sql.filter(self.EType.ExamState == ExamState)
        if ExamType > 0:
            sql = sql.filter(self.EType.ExamType == ExamType)
        if Pass > 0:
            sql = sql.filter(self.EType.Pass == Pass)
        if sql.count() > 0:
            _result.TotalPage = math.ceil(sql.count() / PageSize)
        if _result.TotalPage > 0 and Page > _result.TotalPage:
            Page = _result.TotalPage
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result