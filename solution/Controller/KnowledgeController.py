from Controller.BaseController import *

KnowledgeRouter = APIRouter()
KnowledgePrefix = ''


# 新建知识点
@KnowledgeRouter.post('/New/Knowledge')
async def NewKnowledge(request: Request, Token: str = Form(''), KnowledgeName: str = Form(''), SubjectID: int = Form(0)) -> Result:
    Token = Token.strip()
    KnowledgeName = KnowledgeName.strip()
    return knowledgeLogic.NewKnowledge(request.client.host, Token, KnowledgeName, SubjectID)


# 禁用/启用 知识点
@KnowledgeRouter.post('/Knowledge/Disabled')
async def KnowledgeDisabled(request: Request, Token: str = Form(''), ID: int = Form(0)) -> Result:
    Token = Token.strip()
    return knowledgeLogic.KnowledgeDisabled(request.client.host, Token, ID)


# 修改知识点信息
@KnowledgeRouter.post('/Update/Knowledge/Info')
async def UpdateKnowledgeInfo(request: Request, Token: str = Form(''), ID: int = Form(0), KnowledgeName: str = Form('')) -> Result:
    Token = Token.strip()
    KnowledgeName = KnowledgeName.strip()
    return knowledgeLogic.UpdateKnowledgeInfo(request.client.host, Token, ID, KnowledgeName)


# 知识点列表
@KnowledgeRouter.post('/Knowledge/List')
async def KnowledgeList(request: Request, Token: str = Form(''), Page: int = Form(1), PageSize: int = Form(10), Stext: str = Form(''), SubjectID: int = Form(0), KnowledgeState: int = Form(0)) -> Result:
    Token = Token.strip()
    Stext = Stext.strip()
    return knowledgeLogic.KnowledgeList(Token, Page, PageSize, Stext, SubjectID, KnowledgeState)


# 知识点详情
@KnowledgeRouter.post('/Knowledge/Info')
async def KnowledgeInfo(request: Request, Token: str = Form(''), ID: int = Form(0)) -> Result:
    Token = Token.strip()
    return knowledgeLogic.KnowledgeInfo(Token, ID)
