# -*- coding:utf-8 -*-
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
):
    return teacherLogic.NewTeacher(request.client.host, Token.strip(), Account.strip(), Password.strip(), Name.strip())


# 禁用/启用 教师
@TeacherRouter.post('/Teacher/Disabled')
async def TeacherDisabled(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
):
    return teacherLogic.TeacherDisabled(request.client.host, Token.strip(), ID)


# 更新教师信息
@TeacherRouter.post('/Update/Teacher/Info')
async def UpdateTeacherInfo(
        request: Request,
        Token: str = Form(''),
        Password: str = Form(''),
        Name: str = Form(''),
        ID: int = Form(0),
):
    return teacherLogic.UpdateTeacherInfo(request.client.host, Token.strip(), Password.strip(), Name.strip(), ID)


# 教师列表
@TeacherRouter.post('/Teacher/List')
async def TeacherList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        Stext: str = Form(''),
        State: int = Form(0),
):
    return teacherLogic.TeacherList(Token.strip(), Page, PageSize, Stext.strip(), State)


# 教师详情
@TeacherRouter.post('/Teacher/Info')
async def TeacherInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
):
    return teacherLogic.TeacherInfo(Token.strip(), ID)


# 全部教师
@TeacherRouter.post('/Teachers')
async def Teachers(
        request: Request,
        Token: str = Form(''),
):
    return teacherLogic.Teachers(Token.strip())


# ========================================================================= teacher side =========================================================================


# 教师登录
@TeacherRouter.post('/Teacher/Sign/In')
async def TeacherSignIn(
        request: Request,
        Account: str = Form(''),
        Password: str = Form(''),
):
    return teacherLogic.TeacherSignIn(request.client.host, Account.strip(), Password.strip())


# 教师退出
@TeacherRouter.post('/Teacher/Sign/Out')
async def TeacherSignOut(
        request: Request,
        Token: str = Form(''),
):
    return teacherLogic.TeacherSignOut(request.client.host, Token.strip())


# 教师详情
@TeacherRouter.post('/Check/Teacher/Info')
async def CheckTeacherInfo(
        request: Request,
        Token: str = Form(''),
):
    return teacherLogic.CheckTeacherInfo(Token.strip())


# 更新教师信息
@TeacherRouter.post('/Teacher/Update')
async def TeacherUpdate(
        request: Request,
        Token: str = Form(''),
        Name: str = Form(''),
):
    return teacherLogic.TeacherUpdate(request.client.host, Token.strip(), Name.strip())


# 教师修改密码
@TeacherRouter.post('/Teacher/Change/Password')
async def TeacherChangePassword(
        request: Request,
        Token: str = Form(''),
        NewPassword: str = Form(''),
):
    return teacherLogic.TeacherChangePassword(request.client.host, Token.strip(), NewPassword.strip())


# 教师所在班级列表
@TeacherRouter.post('/The/Teacher/Class')
async def TheTeacherClass(
        request: Request,
        Token: str = Form(''),
):
    return teacherLogic.TheTeacherClass(Token.strip())