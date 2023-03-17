# -*- coding:utf-8 -*-
from Controller.BaseController import *

ScantronSolutionHistoryRouter = APIRouter()
ScantronSolutionHistoryPrefix = ''


# 历史答题卡选项列表
@ScantronSolutionHistoryRouter.post('/Scantron/Solution/History/List')
async def ScantronSolutionHistoryList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        ScantronID: int = Form(0),
        Position: int = Form(0),
):
    return scantronSolutionHistoryLogic.ScantronSolutionHistoryList(Token.strip(), Page, PageSize, ScantronID, Position)


# 历史答题卡详情
@ScantronSolutionHistoryRouter.post('/Scantron/Solution/History/Info')
async def ScantronSolutionHistoryInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
):
    return scantronSolutionHistoryLogic.ScantronSolutionHistoryInfo(Token.strip(), ID)


# 查看附件
@ScantronSolutionHistoryRouter.post('/Scantron/Solution/History/View/Attachments')
async def ScantronSolutionHistoryViewAttachments(
        request: Request,
        Token: str = Form(''),
        OptionAttachment: str = Form(''),
):
    return scantronSolutionHistoryLogic.ScantronSolutionHistoryViewAttachments(Token.strip(), OptionAttachment)