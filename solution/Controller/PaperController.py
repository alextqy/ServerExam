from Controller.BaseController import *

PaperRouter = APIRouter()
PaperPrefix = ''


# 新建试卷
@PaperRouter.post('/New/Paper')
async def NewPaper(request: Request, Token: str = Form(''), PaperName: str = Form(''), SubjectID: int = Form(0), TotalScore: float = Form(0), PassLine: float = Form(0), ExamDuration: int = Form(0)) -> Result:
    Token = Token.strip()
    PaperName = PaperName.strip()
    return paperLogic.NewPaper(request.client.host, Token, PaperName, SubjectID, TotalScore, PassLine, ExamDuration)


# 禁用/启用 试卷
@PaperRouter.post('/Paper/Disabled')
async def PaperDisabled(request: Request, Token: str = Form(''), ID: int = Form(0)) -> Result:
    Token = Token.strip()
    return paperLogic.PaperDisabled(request.client.host, Token, ID)
