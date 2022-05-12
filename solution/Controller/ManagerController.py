from Controller.BaseController import *

ManagerRouter = APIRouter()
ManagerPrefix = ''


# 管理员登录
@ManagerRouter.post('/Manager/Sign/In')
async def ManagerSignIn(
        request: Request,
        Account: str = Form(''),
        Password: str = Form(''),
) -> Result:
    return managerLogic.ManagerSignIn(request.client.host, Account.strip(), Password.strip())


# 管理员退出
@ManagerRouter.post('/Manager/Sign/Out')
async def ManagerSignOut(
        request: Request,
        Token: str = Form(''),
) -> Result:
    return managerLogic.ManagerSignOut(request.client.host, Token.strip())


# 新建管理员
@ManagerRouter.post('/New/Manager')
async def NewManager(
        request: Request,
        Token: str = Form(''),
        Account: str = Form(''),
        Password: str = Form(''),
        Name: str = Form(''),
) -> Result:
    return managerLogic.NewManager(request.client.host, Token.strip(), Account.strip(), Password.strip(), Name.strip())


# 禁用/启用 管理员
@ManagerRouter.post('/Manager/Disabled')
async def ManagerDisabled(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return managerLogic.ManagerDisabled(request.client.host, Token.strip(), ID)


# 管理员修改密码
@ManagerRouter.post('/Manager/Change/Password')
async def ManagerChangePassword(
        request: Request,
        Token: str = Form(''),
        NewPassword: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return managerLogic.ManagerChangePassword(request.client.host, Token.strip(), NewPassword.strip(), ID)


# 更新管理员信息
@ManagerRouter.post('/Update/Manager/Info')
async def UpdateManagerInfo(
        request: Request,
        Token: str = Form(''),
        Name: str = Form(''),
        Permission: int = Form(0),
        ID: int = Form(0),
) -> Result:
    return managerLogic.UpdateManagerInfo(request.client.host, Token.strip(), Name.strip(), Permission, ID)


# 管理员列表
@ManagerRouter.post('/Manager/List')
async def ManagerList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        Stext: str = Form(''),
        State: int = Form(0),
        Permission: int = Form(0),
) -> Result:
    return managerLogic.ManagerList(Token.strip(), Page, PageSize, Stext.strip(), State, Permission)


# 管理员详情
@ManagerRouter.post('/Manager/Info')
async def ManagerInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return managerLogic.ManagerInfo(Token.strip(), ID)