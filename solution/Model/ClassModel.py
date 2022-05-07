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
            _result.Memo = 'param err'
            return _result
        # if Data.Description == '':
        #     _result.Memo = 'param err'
        #     return _result
        Data.ClassCode = self._common.StrMD5(Data.ClassName.strip())
        try:
            _dbsession.add(Data)
            _dbsession.commit()
            _dbsession.flush()
        except Exception as e:
            _result.Memo = str(e)
            _dbsession.rollback()
            return _result

        _result.Status = True
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

        _result.Status = True
        return _result

    def Update(self, _dbsession: DBsession, ID: int, Param: EType) -> Result:
        _result = Result()
        Data: ClassEntity = _dbsession.query(self.EType).filter(self.EType.ID == ID).first()
        if Data is not None:
            try:
                Data.ClassName = Param.ClassName.strip() if Param.ClassName.strip() != '' else Data.ClassName
                Data.ClassCode = self._common.StrMD5(Param.ClassName.strip()) if Param.ClassName.strip() != '' and Param.ClassName.strip() != Data.ClassName else Data.ClassCode
                Data.Description = Param.Description.strip() if Param.Description.strip() != '' else Data.Description
                _dbsession.commit()
            except Exception as e:
                _result.Memo = str(e)
                _dbsession.rollback()
                return _result
            _result.Status = True
        return _result

    def Find(self, _dbsession: DBsession, ID: int) -> EType:
        return _dbsession.query(self.EType).filter(self.EType.ID == ID).first()

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, Stext: str) -> ResultList:
        _result = ResultList()
        _result.Status = True
        _result.Page = Page
        _result.PageSize = PageSize
        _result.TotalPage = math.ceil(_dbsession.query(self.EType).count() / PageSize)
        sql = _dbsession.query(self.EType)
        sql = sql.order_by(desc(self.EType.ID))
        if Stext != '':
            sql = sql.filter(or_(self.EType.ClassCode.ilike('%' + Stext.strip() + '%')))
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result