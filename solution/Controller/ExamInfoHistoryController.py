from Controller.BaseController import *

ExamInfoHistoryRouter = APIRouter()
ExamInfoHistoryPrefix = ''


# 报名历史列表
@ExamInfoHistoryRouter.post('/ExamInfo/History/List')
async def ExamInfoHistoryList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        Stext: str = Form(''),
        ExamState: int = Form(0),
        ExamType: int = Form(0),
) -> ResultList:
    return examInfoHistoryLogic.ExamInfoHistoryList(Token.strip(), Page, PageSize, Stext.strip(), ExamState, ExamType)


# 报名历史详情
@ExamInfoHistoryRouter.post('/ExamInfo/History')
async def ExamInfoHistory(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return examInfoHistoryLogic.ExamInfoHistory(Token.strip(), ID)