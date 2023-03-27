# -*- coding:utf-8 -*-
from Controller.BaseController import *

ScantronSolutionRouter = APIRouter()
ScantronSolutionPrefix = ''


# 答题卡选项列表
@ScantronSolutionRouter.post('/Scantron/Solution/List')
async def ScantronSolutionList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        ScantronID: int = Form(0),
        Position: int = Form(0),
):
    return scantronSolutionLogic.ScantronSolutionList(Token.strip(), Page, PageSize, ScantronID, Position)


# 答题卡详情
@ScantronSolutionRouter.post('/Scantron/Solution/Info')
async def ScantronSolutionInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
):
    return scantronSolutionLogic.ScantronSolutionInfo(Token.strip(), ID)


# 查看附件
@ScantronSolutionRouter.post('/Scantron/Solution/View/Attachments')
async def ScantronSolutionViewAttachments(
        request: Request,
        Token: str = Form(''),
        OptionAttachment: str = Form(''),
):
    return scantronSolutionLogic.ScantronSolutionViewAttachments(Token.strip(), OptionAttachment)