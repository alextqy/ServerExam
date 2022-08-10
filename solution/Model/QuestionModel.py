# -*- coding:utf-8 -*-
from Model.BaseModel import *


class QuestionModel(BaseModel):
    EType: QuestionEntity = QuestionEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Data: EType) -> Result:
        _result = Result()
        Data.QuestionTitle = Data.QuestionTitle.strip()
        Data.Description = Data.Description.strip()
        if Data.QuestionTitle == '':
            _result.Memo = self._lang.ParamErr
            return _result
        if Data.QuestionType <= 0:
            _result.Memo = self._lang.ParamErr
            return _result
        # if Data.QuestionState <= 0:
        #     _result.Memo = self._lang.ParamErr
        #     return _result
        # if Data.Marking <= 0:
        #     _result.Memo = self._lang.ParamErr
        #     return _result
        if Data.KnowledgeID <= 0:
            _result.Memo = self._lang.ParamErr
            return _result
        if Data.QuestionType == 6:
            if Data.Language == '':
                _result.Memo = self._lang.ParamErr
                return _result
            if Data.LanguageVersion == '':
                _result.Memo = self._lang.ParamErr
            Data.Language = Data.Language.lower()
            Data.LanguageVersion = Data.LanguageVersion.lower()
        if Data.QuestionType != 6:
            Data.Language = ''
            Data.LanguageVersion = ''
        Data.QuestionState = 2
        Data.Marking = 1
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

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, Stext: str, QuestionType: int, QuestionState: int, Marking: int, KnowledgeID: int) -> ResultList:
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
            sql = sql.filter(or_(self.EType.QuestionTitle.ilike('%' + Stext.strip() + '%')))
        if QuestionType > 0:
            sql = sql.filter(self.EType.QuestionType == QuestionType)
        if QuestionState > 0:
            sql = sql.filter(self.EType.QuestionState == QuestionState)
        if Marking > 0:
            sql = sql.filter(self.EType.Marking == Marking)
        if KnowledgeID > 0:
            sql = sql.filter(self.EType.KnowledgeID == KnowledgeID)
        if sql.count() > 0:
            _result.TotalPage = math.ceil(sql.count() / PageSize)
        if _result.TotalPage > 0 and Page > _result.TotalPage:
            Page = _result.TotalPage
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result

    def CountType(self, _dbsession: DBsession, KnowledgeID: int, QuestionType: int) -> int:
        return _dbsession.query(self.EType).filter(self.EType.KnowledgeID == KnowledgeID).filter(self.EType.QuestionType == QuestionType).filter(self.EType.QuestionState == 1).count()

    def PaperRuleQuestion(self, _dbsession: DBsession, KnowledgeID: int, QuestionType: int) -> list:
        return _dbsession.query(self.EType).filter(self.EType.KnowledgeID == KnowledgeID).filter(self.EType.QuestionType == QuestionType).filter(self.EType.QuestionState == 1).all()

    def FindQuestionCode(self, _dbsession: DBsession, QuestionCode: str) -> EType:
        return _dbsession.query(self.EType).filter(self.EType.QuestionCode == QuestionCode).first()

    def FindQuestionType(self, _dbsession: DBsession, QuestionType: int) -> list:
        return _dbsession.query(self.EType).filter(self.EType.QuestionState == 1).filter(self.EType.QuestionType == QuestionType).all()