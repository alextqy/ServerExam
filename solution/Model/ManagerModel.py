from Model.BaseModel import *


class ManagerModel(BaseModel):
    EType: ManagerEntity = ManagerEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Data: EType) -> Result:
        _result = Result()
        Data.Account = Data.Account.strip()
        Data.Password = Data.Password.strip()
        Data.Name = Data.Name.strip()
        if Data.Account == '':
            _result.Memo = 'param err'
            return _result
        if Data.Password == '':
            _result.Memo = 'param err'
            return _result
        if Data.Name == '':
            _result.Memo = 'param err'
            return _result
        if Data.State <= 0:
            _result.Memo = 'param err'
            return _result
        if Data.Permission <= 0:
            _result.Memo = 'param err'
            return _result
        Data.Password = self._common.UserPWD(Data.Password.strip())
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
        Data: ManagerEntity = _dbsession.query(self.EType).filter(self.EType.ID == ID).first()
        if Data is not None:
            Data.Password = ''
            Data.Token = ''
        return Data

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, Stext: str, State: int, Permission: int) -> ResultList:
        _result = ResultList()
        _result.State = True
        _result.Page = Page
        _result.PageSize = PageSize
        _result.TotalPage = math.ceil(_dbsession.query(self.EType).count() / PageSize)
        if Page <= 0:
            Page = 1
        if PageSize <= 0:
            PageSize = 10
        if Page > _result.TotalPage:
            Page = _result.TotalPage
        sql = _dbsession.query(self.EType)
        sql = sql.order_by(desc(self.EType.ID))
        if Stext != '':
            sql = sql.filter(or_(self.EType.Account.ilike('%' + Stext.strip() + '%'), self.EType.Name.ilike('%' + Stext.strip() + '%')))
        if State > 0:
            sql = sql.filter(self.EType.State == State)
        if Permission > 0:
            sql = sql.filter(self.EType.Permission == Permission)
        DataList = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        for i in DataList:
            i.Password = ''
            i.Token = ''
        _result.Data = DataList
        return _result

    def FindAccount(self, _dbsession: DBsession, Account: str) -> EType:
        Data: ManagerEntity = _dbsession.query(self.EType).filter(self.EType.Account == Account.strip()).first()
        return Data

    def FindToken(self, _dbsession: DBsession, Token: str) -> EType:
        return _dbsession.query(self.EType).filter(self.EType.Token == Token.strip()).first()

    def ChangePassword(self, _dbsession: DBsession, Data: EType, Password: str) -> Result:
        _result = Result()
        try:
            Data.Password = self._common.UserPWD(Password.strip()) if Password.strip() != '' and self._common.UserPWD(Password.strip()) != Data.Password else Data.Password
            Data.UpdateTime = self._common.Time()
            _dbsession.commit()
        except Exception as e:
            _dbsession.rollback()
            _result.Memo = str(e)
            return _result
        _result.State = True
        return _result