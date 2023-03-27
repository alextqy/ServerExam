# -*- coding:utf-8 -*-
from Controller.BaseController import *

SubjectRouter = APIRouter()
SubjectPrefix = ''


# 新建科目
@SubjectRouter.post('/New/Subject')
async def NewSubject(
        request: Request,
        Token: str = Form(''),
        SubjectName: str = Form(''),
):
    return subjectLogic.NewSubject(request.client.host, Token.strip(), SubjectName.strip())


# 禁用/启用 科目
@SubjectRouter.post('/Subject/Disabled')
async def SubjectDisabled(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
):
    return subjectLogic.SubjectDisabled(request.client.host, Token.strip(), ID)


# 修改科目详情
@SubjectRouter.post('/Update/Subject/Info')
async def UpdateSubjectInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
        SubjectName: str = Form(''),
):
    return subjectLogic.UpdateSubjectInfo(request.client.host, Token.strip(), ID, SubjectName.strip())


# 科目列表
@SubjectRouter.post('/Subject/List')
async def SubjectList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        Stext: str = Form(''),
        SubjectState: int = Form(0),
):
    return subjectLogic.SubjectList(Token.strip(), Page, PageSize, Stext.strip(), SubjectState)


# 科目详情
@SubjectRouter.post('/Subject/Info')
async def SubjectInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
):
    return subjectLogic.SubjectInfo(Token.strip(), ID)


# 全部科目
@SubjectRouter.post('/Subjects')
async def Subjects(
        request: Request,
        Token: str = Form(''),
):
    return subjectLogic.Subjects(Token.strip())