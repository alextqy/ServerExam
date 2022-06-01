from Controller.BaseController import *

TeacherRouter = APIRouter()
TeacherPrefix = ''


# 管理员登录
@TeacherRouter.post('/New/Teacher')
async def NewTeacher(
        request: Request,
        Token: str = Form(''),
        Account: str = Form(''),
        Password: str = Form(''),
        Name: str = Form(''),
        ClassID: int = Form(0),
) -> Result:
    return teacherLogic.NewTeacher(request.client.host, Token.strip(), Account.strip(), Password.strip(), Name.strip(), ClassID)


# 禁用/启用 教师
@TeacherRouter.post('/Teacher/Disabled')
async def TeacherDisabled(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return teacherLogic.TeacherDisabled(request.client.host, Token.strip(), ID)


# 更新教师信息
@TeacherRouter.post('/Update/Teacher/Info')
async def UpdateTeacherInfo(
        request: Request,
        Token: str = Form(''),
        Password: str = Form(''),
        Name: str = Form(''),
        ClassID: int = Form(0),
        ID: int = Form(0),
) -> Result:
    return teacherLogic.UpdateTeacherInfo(request.client.host, Token.strip(), Password.strip(), Name.strip(), ClassID, ID)


# 教师列表
@TeacherRouter.post('/Teacher/List')
async def TeacherList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        Stext: str = Form(''),
        State: int = Form(0),
        ClassID: int = Form(0),
) -> ResultList:
    return teacherLogic.TeacherList(Token.strip(), Page, PageSize, Stext.strip(), State, ClassID)


# 教师详情
@TeacherRouter.post('/Teacher/Info')
async def TeacherInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return teacherLogic.TeacherInfo(Token.strip(), ID)