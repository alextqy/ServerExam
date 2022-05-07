from Controller.BaseController import *

SubjectRouter = APIRouter()
SubjectPrefix = ''


# 新建科目
@SubjectRouter.post('/New/Subject')
async def NewSubject(request: Request, Token: str = Form(''), SubjectName: str = Form('')) -> Result:
    Token = Token.strip()
    SubjectName = SubjectName.strip()
    return subjectLogic.NewSubject(Token, SubjectName)


# 禁用/启用 科目
@SubjectRouter.post('/Subject/Disabled')
async def SubjectDisabled(request: Request, Token: str = Form(''), ID: int = Form(0)) -> Result:
    Token = Token.strip()
    return subjectLogic.SubjectDisabled(Token, ID)


@SubjectRouter.post('/Update/Subject/Info')
async def UpdateSubjectInfo(request: Request, Token: str = Form(''), ID: int = Form(0), SubjectName: str = Form('')) -> Result:
    Token = Token.strip()
    SubjectName = SubjectName.strip()
    return subjectLogic.UpdateSubjectInfo(Token, ID, SubjectName)
