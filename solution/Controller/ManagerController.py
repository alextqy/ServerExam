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