from Model.BaseModel import *


class ManagerModel(BaseModel):
    EType: ManagerEntity = ManagerEntity

    def __init__(self):
        super().__init__()

    def Insert(self, _dbsession: DBsession, Data: EType) -> Result:
        _result = Result()
        Data.Account = Data.Account.strip()
        Data.PWD = Data.PWD.strip()
        Data.Name = Data.Name.strip()
        if Data.Account == '':
            _result.Memo = 'param err'
            return _result
        if Data.PWD == '':
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
        Data.PWD = self._common.UserPWD(Data.PWD.strip())
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
        Data: ManagerEntity = _dbsession.query(self.EType).filter(self.EType.ID == ID).first()
        if Data is not None:
            try:
                Data.Account = Param.Account.strip() if Param.Account.strip() != '' else Data.Account
                # Data.PWD = self._common.UserPWD(Param.PWD.strip()) if Param.PWD.strip() != '' and Param.PWD.strip() != Data.PWD else Data.PWD
                Data.Name = Param.Name.strip() if Param.Name.strip() != '' else Data.Name
                Data.State = Param.State if Param.State > 0 else Data.State
                Data.Permission = Param.Permission if Param.Permission > 0 else Data.Permission
                Data.UpdateTime = self._common.Time()
                _dbsession.commit()
            except Exception as e:
                _result.Memo = str(e)
                _dbsession.rollback()
                return _result
            _result.Status = True
        return _result

    def Find(self, _dbsession: DBsession, ID: int) -> EType:
        return _dbsession.query(self.EType).filter(self.EType.ID == ID).first()

    def List(self, _dbsession: DBsession, Page: int, PageSize: int, Stext: str, State: int, Permission: int) -> Result:
        _result = ResultList()
        _result.Status = True
        _result.Page = Page
        _result.PageSize = PageSize
        _result.TotalPage = math.ceil(_dbsession.query(self.EType).count() / PageSize)
        sql = _dbsession.query(self.EType)
        sql = sql.order_by(desc(self.EType.ID))
        if Stext != '':
            sql = sql.filter(or_(self.EType.Account.ilike('%' + Stext.strip() + '%'), self.EType.Name.ilike('%' + Stext.strip() + '%')))
        if State > 0:
            sql = sql.filter(self.EType.State == State)
        if Permission > 0:
            self = sql.filter(self.EType.Permission == Permission)
        _result.Data = sql.limit(PageSize).offset((Page - 1) * PageSize).all()
        return _result

    def FindAccount(self, _dbsession: DBsession, Account: str) -> EType:
        return _dbsession.query(self.EType).filter(self.EType.Account == Account.strip()).first()

    def FindToken(self, _dbsession: DBsession, Token: str) -> EType:
        return _dbsession.query(self.EType).filter(self.EType.Token == Token.strip()).first()

    def ChangePassword(self, _dbsession: DBsession, Data: EType, Password: str) -> bool:
        try:
            Data.PWD = self._common.UserPWD(Password.strip()) if Password.strip() != '' and self._common.UserPWD(Password.strip()) != Data.PWD else Data.PWD
            _dbsession.commit()
        except Exception as e:
            return False
        return True