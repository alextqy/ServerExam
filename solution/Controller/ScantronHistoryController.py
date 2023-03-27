# -*- coding:utf-8 -*-
from Controller.BaseController import *

ScantronHistoryRouter = APIRouter()
ScantronHistoryPrefix = ''


# 答题卡列表
@ScantronHistoryRouter.post('/Scantron/History/List')
async def ScantronHistoryList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        ExamID: int = Form(0),
):
    return scantronHistoryLogic.ScantronHistoryList(Token.strip(), Page, PageSize, ExamID)


# 答题卡详情
@ScantronHistoryRouter.post('/Scantron/History/Info')
async def ScantronHistoryInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
):
    return scantronHistoryLogic.ScantronHistoryInfo(Token.strip(), ID)


# 查看附件
@ScantronHistoryRouter.post('/Scantron/History/View/Attachments')
async def ScantronHistoryViewAttachments(
        request: Request,
        Token: str = Form(''),
        FilePath: str = Form(''),
):
    return scantronHistoryLogic.ScantronHistoryViewAttachments(Token.strip(), FilePath)