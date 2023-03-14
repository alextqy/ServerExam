# -*- coding:utf-8 -*-
from Model.BaseModel import *


class ScantronHistoryModel(BaseModel):
    EType: ScantronHistoryEntity = ScantronHistoryEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Data: EType):
        _result = Result()
        Data.CreateTime = self._common.Time()
        # Data.QuestionTitle = Data.QuestionTitle.strip()
        # Data.QuestionCode = Data.QuestionCode.strip()
        # Data.Description = Data.Description.strip()
        # Data.Attachment = Data.Attachment.strip()
        # Data.HeadlineContent = Data.HeadlineContent.strip()
        if Data.HeadlineContent == '':
            if Data.QuestionTitle == '':
                _result.Memo = self._lang.ParamErr
                return _result
            if Data.QuestionType <= 0:
                _result.Memo = self._lang.ParamErr
                return _result
            if Data.KnowledgeID <= 0:
                _result.Memo = self._lang.ParamErr
                return _result
            if Data.Score <= 0:
                _result.Memo = self._lang.ParamErr
                return _result
        if Data.ExamID <= 0:
            _result.Memo = self._lang.ParamErr
            return _result
        Data.Right = 0
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

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, ExamID: int):
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
        if ExamID > 0:
            sql = sql.filter(self.EType.ExamID == ExamID)
        if sql.count() > 0:
            _result.TotalPage = math.ceil(sql.count() / PageSize)
        if _result.TotalPage > 0 and Page > _result.TotalPage:
            Page = _result.TotalPage
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result