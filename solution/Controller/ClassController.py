# -*- coding:utf-8 -*-
from Controller.BaseController import *

ClassRouter = APIRouter()
ClassPrefix = ''


# 新建班级
@ClassRouter.post('/New/Class')
async def NewClass(
        request: Request,
        Token: str = Form(''),
        ClassName: str = Form(''),
        Description: str = Form(''),
):
    return classLogic.NewClass(request.client.host, Token.strip(), ClassName.strip(), Description.strip())


# 修改班级信息
@ClassRouter.post('/Update/Class/Info')
async def UpdateClassInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
        ClassName: str = Form(''),
        Description: str = Form(''),
):
    return classLogic.UpdateClassInfo(request.client.host, Token.strip(), ID, ClassName.strip(), Description.strip())


# 班级列表
@ClassRouter.post('/Class/List')
async def ClassList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        Stext: str = Form(''),
):
    return classLogic.ClassList(Token.strip(), Page, PageSize, Stext.strip())


# 班级详情
@ClassRouter.post('/Class/Info')
async def ClassInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
):
    return classLogic.ClassInfo(Token.strip(), ID)


# 全部班级
@ClassRouter.post('/Classes')
async def Classes(
        request: Request,
        Token: str = Form(''),
):
    return classLogic.Classes(Token.strip())
