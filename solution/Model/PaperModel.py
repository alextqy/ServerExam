# -*- coding:utf-8 -*-
from Model.BaseModel import *


class PaperModel(BaseModel):
    EType: PaperEntity = PaperEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Data: EType) -> Result:
        _result = Result()
        Data.CreateTime = self._common.Time()
        Data.PaperName = Data.PaperName.strip()
        if Data.PaperName == '':
            _result.Memo = self._lang.ParamErr
            return _result
        if Data.SubjectID <= 0:
            _result.Memo = self._lang.ParamErr
            return _result
        if Data.TotalScore <= 0:
            _result.Memo = self._lang.ParamErr
            return _result
        if Data.PassLine <= 0:
            _result.Memo = self._lang.ParamErr
            return _result
        if Data.ExamDuration <= 0:
            _result.Memo = self._lang.ParamErr
            return _result
        # if Data.PaperState <= 0:
        #     _result.Memo = self._lang.ParamErr
        #     return _result

        Data.PaperState = 2
        Data.PaperCode = self._common.StrMD5(Data.PaperName.strip())
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

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, Stext: str, SubjectID: int, PaperState: int) -> ResultList:
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
            sql = sql.filter(or_(self.EType.PaperName.ilike('%' + Stext.strip() + '%')))
        if SubjectID > 0:
            sql = sql.filter(self.EType.SubjectID == SubjectID)
        if PaperState > 0:
            sql = sql.filter(self.EType.PaperState == PaperState)
        if sql.count() > 0:
            _result.TotalPage = math.ceil(sql.count() / PageSize)
        if _result.TotalPage > 0 and Page > _result.TotalPage:
            Page = _result.TotalPage
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result

    def FindPaperCode(self, _dbsession: DBsession, PaperName: str) -> EType:
        return _dbsession.query(self.EType).filter(self.EType.PaperCode == self._common.StrMD5(PaperName)).first()

    def SubjectPaper(self, _dbsession: DBsession, SubjectID: int) -> list:
        return _dbsession.query(self.EType).filter(self.EType.SubjectID == SubjectID).all()

    def FindSubjectPaper(self, _dbsession: DBsession, SubjectID: int) -> EType:
        return _dbsession.query(self.EType).filter(self.EType.SubjectID == SubjectID).filter(self.EType.PaperState == 1).first()