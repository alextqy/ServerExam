from Controller.BaseController import *

KnowledgeRouter = APIRouter()
KnowledgePrefix = ''


# 新建知识点
@KnowledgeRouter.post('/New/Knowledge')
async def NewKnowledge(
        request: Request,
        Token: str = Form(''),
        KnowledgeName: str = Form(''),
        SubjectID: int = Form(0),
) -> Result:
    return knowledgeLogic.NewKnowledge(request.client.host, Token.strip(), KnowledgeName.strip(), SubjectID)


# 禁用/启用 知识点
@KnowledgeRouter.post('/Knowledge/Disabled')
async def KnowledgeDisabled(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return knowledgeLogic.KnowledgeDisabled(request.client.host, Token.strip(), ID)


# 修改知识点信息
@KnowledgeRouter.post('/Update/Knowledge/Info')
async def UpdateKnowledgeInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
        KnowledgeName: str = Form(''),
) -> Result:
    return knowledgeLogic.UpdateKnowledgeInfo(request.client.host, Token.strip(), ID, KnowledgeName.strip())


# 知识点列表
@KnowledgeRouter.post('/Knowledge/List')
async def KnowledgeList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        Stext: str = Form(''),
        SubjectID: int = Form(0),
        KnowledgeState: int = Form(0),
) -> Result:
    return knowledgeLogic.KnowledgeList(Token.strip(), Page, PageSize, Stext.strip(), SubjectID, KnowledgeState)


# 知识点详情
@KnowledgeRouter.post('/Knowledge/Info')
async def KnowledgeInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return knowledgeLogic.KnowledgeInfo(Token.strip(), ID)
