# -*- coding:utf-8 -*-
from Controller.BaseController import *

ScantronSolutionRouter = APIRouter()
ScantronSolutionPrefix = ''


# 答题卡列表
@ScantronSolutionRouter.post('/Scantron/Solution/List')
async def ScantronSolutionList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        ScantronID: int = Form(0),
        Position: int = Form(0),
) -> ResultList:
    return scantronSolutionLogic.ScantronSolutionList(Token.strip(), Page, PageSize, ScantronID, Position)


# 答题卡详情
@ScantronSolutionRouter.post('/Scantron/Solution/Info')
async def ScantronSolutionInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return scantronSolutionLogic.ScantronSolutionInfo(Token.strip(), ID)