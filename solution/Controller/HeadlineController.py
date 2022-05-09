from Controller.BaseController import *

HeadlineRouter = APIRouter()
HeadlinePrefix = ''


# 新建大标题
@HeadlineRouter.post('/New/Headline')
async def NewHeadline(request: Request, Token: str = Form(''), Content: str = Form('')) -> Result:
    Token = Token.strip()
    Content = Content.strip()
    return headlineLogic.NewHeadline(request.client.host, Token, Content)


# 修改大标题
@HeadlineRouter.post('/Update/Headline/Info')
async def UpdateHeadlineInfo(request: Request, Token: str = Form(''), ID: int = Form(''), Content: str = Form('')) -> Result:
    Token = Token.strip()
    Content = Content.strip()
    return headlineLogic.UpdateHeadlineInfo(request.client.host, Token, ID, Content)


# 大标题列表
@HeadlineRouter.post('/Headline/List')
async def HeadlineList(request: Request, Token: str = Form(''), Page: int = Form(1), PageSize: int = Form(10), Stext: str = Form('')) -> Result:
    Token = Token.strip()
    Stext = Stext.strip()
    return headlineLogic.HeadlineList(Token, Page, PageSize, Stext)


# 大标题详情
@HeadlineRouter.post('/Headline/Info')
async def HeadlineInfo(request: Request, Token: str = Form(''), ID: int = Form(0)) -> Result:
    Token = Token.strip()
    return headlineLogic.HeadlineInfo(Token, ID)