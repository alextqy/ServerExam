from Controller.BaseController import *

ManagerRouter = APIRouter()
ManagerPrefix = ''


# 管理员登录
@ManagerRouter.post('/Manager/Sign/In')
async def ManagerSignIn(request: Request, Account: str = Form(''), Password: str = Form('')) -> Result:
    Account = Account.strip()
    Password = Password.strip()
    return managerLogic.ManagerSignIn(Account, Password)


# 管理员退出
@ManagerRouter.post('/Manager/Sign/Out')
async def ManagerSignOut(request: Request, Token: str = Form('')) -> Result:
    Token = Token.strip()
    return managerLogic.ManagerSignOut(Token)


# 新建管理员
@ManagerRouter.post('/New/Manager')
async def NewManager(request: Request, Token: str = Form(''), Account: str = Form(''), Password: str = Form(''), Name: str = Form('')) -> Result:
    Token = Token.strip()
    Account = Account.strip()
    Password = Password.strip()
    Name = Name.strip()
    return managerLogic.NewManager(Token, Account, Password, Name)


# 禁用/启用 管理员
@ManagerRouter.post('/Manager/Disabled')
async def ManagerDisabled(request: Request, Token: str = Form(''), ID: int = Form(0)) -> Result:
    Token = Token.strip()
    return managerLogic.ManagerDisabled(Token, ID)


# 管理员修改密码
@ManagerRouter.post('/Manager/Change/Password')
async def ManagerChangePassword(request: Request, Token: str = Form(''), NewPassword: str = Form(''), ID: int = Form(0)) -> Result:
    Token = Token.strip()
    NewPassword = NewPassword.strip()
    return managerLogic.ManagerChangePassword(Token, NewPassword, ID)


# 更新管理员信息
@ManagerRouter.post('/Update/Manager/Info')
async def UpdateManagerInfo(request: Request, Token: str = Form(''), Name: str = Form(''), Permission: int = Form(0), ID: int = Form(0)) -> Result:
    Token = Token.strip()
    Name = Name.strip()
    return managerLogic.UpdateManagerInfo(Token, Name, Permission, ID)
