# -*- coding:utf-8 -*-
from Controller.BaseController import *

ExamineeRouter = APIRouter()
ExamineePrefix = ''


# 添加考生
@ExamineeRouter.post('/New/Examinee')
async def NewExaminee(
        request: Request,
        Token: str = Form(''),
        ExamineeNo: str = Form(''),
        Name: str = Form(''),
        ClassID: int = Form(0),
        Contact: str = Form(''),
) -> Result:
    return examineeLogic.NewExaminee(request.client.host, Token.strip(), ExamineeNo.strip(), Name.strip(), ClassID, Contact.strip())


# 更新考生信息
@ExamineeRouter.post('/Update/Examinee')
async def UpdateExaminee(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
        Name: str = Form(''),
        Contact: str = Form(''),
) -> Result:
    return examineeLogic.UpdateExaminee(request.client.host, Token.strip(), ID, Name.strip(), Contact.strip())


# 考生列表
@ExamineeRouter.post('/Examinee/List')
async def ExamineeList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        Stext: str = Form(''),
        ClassID: int = Form(0),
) -> ResultList:
    return examineeLogic.ExamineeList(Token.strip(), Page, PageSize, Stext.strip(), ClassID)


# 考生详情
@ExamineeRouter.post('/Examinee/Info')
async def ExamineeInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return examineeLogic.ExamineeInfo(Token.strip(), ID)


# 全部考生
@ExamineeRouter.post('/Examinees')
async def Examinees(
        request: Request,
        Token: str = Form(''),
) -> Result:
    return examineeLogic.Examinees(Token.strip())