# -*- coding:utf-8 -*-
from Model.BaseModel import *


class PaperRuleModel(BaseModel):
    EType: PaperRuleEntity = PaperRuleEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Data: EType) -> Result:
        _result = Result()
        Data.CreateTime = self._common.Time()
        if Data.HeadlineID <= 0:
            if Data.KnowledgeID <= 0:
                _result.Memo = self._lang.ParamErr
                return _result
            if Data.QuestionType <= 0:
                _result.Memo = self._lang.ParamErr
                return _result
            if Data.QuestionNum <= 0:
                _result.Memo = self._lang.ParamErr
                return _result
            if Data.SingleScore <= 0:
                _result.Memo = self._lang.ParamErr
                return _result
        if Data.KnowledgeID <= 0:
            if Data.HeadlineID <= 0:
                _result.Memo = self._lang.ParamErr
                return _result
        if Data.PaperID <= 0:
            _result.Memo = self._lang.ParamErr
            return _result

        Data.PaperRuleState = 1
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

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, PaperID: int, PaperRuleState: int) -> ResultList:
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
        sql = sql.filter(self.EType.PaperID == PaperID)
        sql = sql.filter(self.EType.PaperRuleState == PaperRuleState)
        if sql.count() > 0:
            _result.TotalPage = math.ceil(sql.count() / PageSize)
        if _result.TotalPage > 0 and Page > _result.TotalPage:
            Page = _result.TotalPage
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result

    def FindPaperID(self, _dbsession: DBsession, PaperID: int) -> list:
        return _dbsession.query(self.EType).filter(self.EType.PaperID == PaperID).filter(self.EType.PaperRuleState == 1).all()

    def CheckPaperRule(self, _dbsession: DBsession, PaperID: int, KnowledgeID: int, QuestionType: int) -> EType:
        return _dbsession.query(self.EType).filter(self.EType.PaperID == PaperID).filter(self.EType.KnowledgeID == KnowledgeID).filter(self.EType.QuestionType == QuestionType).filter(self.EType.PaperRuleState == 1).first()