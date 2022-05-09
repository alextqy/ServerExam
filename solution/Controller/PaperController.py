from Controller.BaseController import *

PaperRouter = APIRouter()
PaperPrefix = ''


@PaperRouter.post('/New/Paper')
async def NewPaper(request: Request, Token: str = Form(''), PaperName: str = Form(''), SubjectID: int = Form(0), TotalScore: float = Form(0), PassLine: float = Form(0), ExamDuration: int = Form(0)) -> Result:
    Token = Token.strip()
    PaperName = PaperName.strip()
    return paperLogic.NewPaper(request.client.host, Token, PaperName, SubjectID, TotalScore, PassLine, ExamDuration)