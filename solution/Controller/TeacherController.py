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
