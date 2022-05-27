from Controller.BaseController import *

PaperRouter = APIRouter()
PaperPrefix = ''


# 新建试卷
@PaperRouter.post('/New/Paper')
async def NewPaper(
        request: Request,
        Token: str = Form(''),
        PaperName: str = Form(''),
        SubjectID: int = Form(0),
        TotalScore: float = Form(0),
        PassLine: float = Form(0),
        ExamDuration: int = Form(0),
) -> Result:
    return paperLogic.NewPaper(request.client.host, Token.strip(), PaperName.strip(), SubjectID, TotalScore, PassLine, ExamDuration)


# 禁用/启用 试卷
@PaperRouter.post('/Paper/Disabled')
async def PaperDisabled(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return paperLogic.PaperDisabled(request.client.host, Token.strip(), ID)


# 修改试卷信息
@PaperRouter.post('/Update/Paper/Info')
async def UpdatePaperInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
        PaperName: str = Form(''),
        TotalScore: float = Form(0),
        PassLine: float = Form(0),
        ExamDuration: int = Form(0),
) -> Result:
    return paperLogic.UpdatePaperInfo(request.client.host, Token.strip(), ID, PaperName.strip(), TotalScore, PassLine, ExamDuration)


# 试卷列表
@PaperRouter.post('/Paper/List')
async def PaperList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        Stext: str = Form(''),
        SubjectID: int = Form(0),
        PaperState: int = Form(0),
) -> ResultList:
    return paperLogic.PaperList(Token.strip(), Page, PageSize, Stext.strip(), SubjectID, PaperState)


# 试卷详情
@PaperRouter.post('/Paper/Info')
async def PaperInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return paperLogic.PaperInfo(Token.strip(), ID)