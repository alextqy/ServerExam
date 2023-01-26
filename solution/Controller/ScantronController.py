# -*- coding:utf-8 -*-
from Controller.BaseController import *

ScantronRouter = APIRouter()
ScantronPrefix = ''


# 答题卡列表
@ScantronRouter.post('/Scantron/List')
async def ScantronList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        ExamID: int = Form(0),
):
    return scantronLogic.ScantronList(Token.strip(), Page, PageSize, ExamID)


# 答题卡详情
@ScantronRouter.post('/Scantron/Info')
async def ScantronInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
):
    return scantronLogic.ScantronInfo(Token.strip(), ID)