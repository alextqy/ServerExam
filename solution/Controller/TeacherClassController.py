# -*- coding:utf-8 -*-
from Controller.BaseController import *

TeacherClassRouter = APIRouter()
TeacherClassPrefix = ''


# 新建教师班级关联数据
@TeacherClassRouter.post('/New/Teacher/Class')
async def NewTeacherClass(
        request: Request,
        Token: str = Form(''),
        TeacherID: int = Form(0),
        ClassID: int = Form(0),
):
    return teacherClassLogic.NewTeacherClass(request.client.host, Token.strip(), TeacherID, ClassID)


# 删除教师班级对应数据
@TeacherClassRouter.post('/Delete/Teacher/Class')
async def DeleteTeacherClass(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
):
    return teacherClassLogic.DeleteTeacherClass(request.client.host, Token.strip(), ID)


# 教师班级列表
@TeacherClassRouter.post('/Teacher/Class/List')
async def TeacherClassList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        TeacherID: int = Form(0),
        ClassID: int = Form(0),
):
    return teacherClassLogic.TeacherClassList(Token.strip(), Page, PageSize, TeacherID, ClassID)


# 教师列表
@TeacherClassRouter.post('/Teachers')
async def TeacherClassList(
        request: Request,
        Token: str = Form(''),
        ClassID: int = Form(0),
):
    return teacherClassLogic.Teachers(Token.strip(), ClassID)