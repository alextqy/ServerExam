# -*- coding:utf-8 -*-
from Controller.BaseController import *

HeadlineRouter = APIRouter()
HeadlinePrefix = ''


# 新建大标题
@HeadlineRouter.post('/New/Headline')
async def NewHeadline(
        request: Request,
        Token: str = Form(''),
        Content: str = Form(''),
) -> Result:
    return headlineLogic.NewHeadline(request.client.host, Token.strip(), Content.strip())


# 修改大标题
@HeadlineRouter.post('/Update/Headline/Info')
async def UpdateHeadlineInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
        Content: str = Form(''),
) -> Result:
    return headlineLogic.UpdateHeadlineInfo(request.client.host, Token.strip(), ID, Content.strip())


# 大标题列表
@HeadlineRouter.post('/Headline/List')
async def HeadlineList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        Stext: str = Form(''),
) -> ResultList:
    return headlineLogic.HeadlineList(Token.strip(), Page, PageSize, Stext.strip())


# 大标题详情
@HeadlineRouter.post('/Headline/Info')
async def HeadlineInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return headlineLogic.HeadlineInfo(Token.strip(), ID)


@HeadlineRouter.post('/Headlines')
async def Headlines(
        request: Request,
        Token: str = Form(''),
) -> Result:
    return headlineLogic.Headlines(Token.strip())