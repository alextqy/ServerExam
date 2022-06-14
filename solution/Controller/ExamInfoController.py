from Controller.BaseController import *

ExamInfoRouter = APIRouter()
ExamInfoPrefix = ''


# 新建管理员
@ExamInfoRouter.post('/New/ExamInfo')
async def NewExamInfo(
        request: Request,
        Token: str = Form(''),
        SubjectName: str = Form(''),
        ExamNo: str = Form(''),
        ExamineeID: int = Form(0),
        ExamType: int = Form(0),
) -> Result:
    return examInfoLogic.NewExamInfo(request.client.host, Token.strip(), SubjectName.strip(), ExamNo.strip(), ExamineeID, ExamType)


# 报名作废
@ExamInfoRouter.post('/ExamInfo/Disabled')
async def ExamInfoDisabled(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return examInfoLogic.ExamInfoDisabled(request.client.host, Token.strip(), ID)


# 报名列表
@ExamInfoRouter.post('/ExamInfo/List')
async def ExamInfoList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        Stext: str = Form(''),
        ExamState: int = Form(0),
        ExamType: int = Form(0),
) -> ResultList:
    return examInfoLogic.ExamInfoList(Token.strip(), Page, PageSize, Stext.strip(), ExamState, ExamType)


# 报名详情
@ExamInfoRouter.post('/ExamInfo')
async def ExamInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return examInfoLogic.ExamInfo(Token.strip(), ID)


# 生成试卷
@ExamInfoRouter.post('/Generate/Test/Paper')
async def GenerateTestPaper(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return examInfoLogic.GenerateTestPaper(request.client.host, Token.strip(), ID)


# 重置报名试题数据
@ExamInfoRouter.post('/Reset/Exam/Question/Data')
async def ResetExamQuestionData(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return examInfoLogic.ResetExamQuestionData(request.client.host, Token.strip(), ID)
