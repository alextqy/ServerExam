# -*- coding:utf-8 -*-
from Controller.BaseController import *

PaperRuleRouter = APIRouter()
PaperRulePrefix = ''


# 新建试卷规则
@PaperRuleRouter.post('/New/Paper/Rule')
async def NewPaperRule(
        request: Request,
        Token: str = Form(''),
        HeadlineID: int = Form(0),
        QuestionType: int = Form(0),
        KnowledgeID: int = Form(0),
        QuestionNum: int = Form(0),
        SingleScore: float = Form(0),
        PaperID: int = Form(0),
) -> Result:
    return paperRuleLogic.NewPaperRule(request.client.host, Token.strip(), HeadlineID, QuestionType, KnowledgeID, QuestionNum, SingleScore, PaperID)


# 禁用试题规则
@PaperRuleRouter.post('/Paper/Rule/Disabled')
async def PaperRuleDisabled(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return paperRuleLogic.PaperRuleDisabled(request.client.host, Token.strip(), ID)


# 删除试题规则
@PaperRuleRouter.post('/Paper/Rule/Delete')
async def PaperRuleDelete(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return paperRuleLogic.PaperRuleDelete(request.client.host, Token.strip(), ID)


# 试卷规则列表
@PaperRuleRouter.post('/Paper/Rule/List')
async def PaperRuleList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        PaperID: int = Form(0),
        PaperRuleState: int = Form(0),
) -> Result:
    return paperRuleLogic.PaperRuleList(Token.strip(), Page, PageSize, PaperID, PaperRuleState)


# 试题规则详情
@PaperRuleRouter.post('/Paper/Rule/Info')
async def PaperRuleInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return paperRuleLogic.PaperRuleInfo(Token.strip(), ID)
