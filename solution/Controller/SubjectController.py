from Controller.BaseController import *

SubjectRouter = APIRouter()
SubjectPrefix = ''


# 新建科目
@SubjectRouter.post('/New/Subject')
async def NewSubject(request: Request, Token: str = Form(''), SubjectName: str = Form('')) -> Result:
    Token = Token.strip()
    SubjectName = SubjectName.strip()
    return subjectLogic.NewSubject(request.client.host, Token, SubjectName)


# 禁用/启用 科目
@SubjectRouter.post('/Subject/Disabled')
async def SubjectDisabled(request: Request, Token: str = Form(''), ID: int = Form(0)) -> Result:
    Token = Token.strip()
    return subjectLogic.SubjectDisabled(request.client.host, Token, ID)


# 科目详情
@SubjectRouter.post('/Update/Subject/Info')
async def UpdateSubjectInfo(request: Request, Token: str = Form(''), ID: int = Form(0), SubjectName: str = Form('')) -> Result:
    Token = Token.strip()
    SubjectName = SubjectName.strip()
    return subjectLogic.UpdateSubjectInfo(request.client.host, Token, ID, SubjectName)


# 科目列表
@SubjectRouter.post('/Subject/List')
async def SubjectList(request: Request, Token: str = Form(''), Page: int = Form(1), PageSize: int = Form(10), Stext: str = Form(''), SubjectState: int = Form(0)) -> Result:
    Token = Token.strip()
    Stext = Stext.strip()
    return subjectLogic.SubjectList(Token, Page, PageSize, Stext, SubjectState)


# 科目详情
@SubjectRouter.post('/Subject/Info')
async def SubjectInfo(request: Request, Token: str = Form(''), ID: int = Form(0)) -> Result:
    Token = Token.strip()
    ID = ID
    return subjectLogic.SubjectInfo(Token, ID)