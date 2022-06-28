from Controller.BaseController import *

ExamLogRouter = APIRouter()
ExamLogPrefix = ''


# 系统日志列表
@ExamLogRouter.post('/Exam/Log/List')
async def ExamLogList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        Stext: str = Form(''),
        Type: int = Form(0),
) -> ResultList:
    return examLogLogic.ExamLogList(Token.strip(), Page, PageSize, Stext.strip(), Type)


# 日志详情
@ExamLogRouter.post('/Exam/Log/Info')
async def ExamLogInfo(request: Request, Token: str = Form(''), ID: int = Form(0)) -> Result:
    return examLogLogic.ExamLogInfo(Token.strip(), ID)