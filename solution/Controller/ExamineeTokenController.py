from Controller.BaseController import *

ExamineeTokenRouter = APIRouter()
ExamineeTokenPrefix = ''


# 学号登录(获取报名列表)
@ExamineeTokenRouter.post('/Sign/In/Student/ID')
async def SignInStudentID(
        request: Request,
        Account: str = Form(''),
) -> Result:
    return examineeTokenLogic.SignInStudentID(Account.strip())


# 准考证号登录
@ExamineeTokenRouter.post('/Sign/In/Admission/Ticket')
async def SignInAdmissionTicket(
        request: Request,
        ExamNo: str = Form(''),
) -> Result:
    return examineeTokenLogic.SignInAdmissionTicket(request.client.host, ExamNo.strip())


# 获取答题卡列表
@ExamineeTokenRouter.post('/Exam/Scantron/List')
async def ExamScantronList(
        request: Request,
        Token: str = Form(''),
) -> Result:
    return examineeTokenLogic.ExamScantronList(Token.strip())


# 获取答题卡选项信息
@ExamineeTokenRouter.post('/Exam/Scantron/Solution/Info')
async def ExamScantronSolutionInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return examineeTokenLogic.ExamScantronSolutionInfo(Token.strip(), ID)


# 作答
@ExamineeTokenRouter.post('/Exam/Answer')
async def ExamAnswer(
        request: Request,
        Token: str = Form(''),
        ScantronID: int = Form(0),
        ID: int = Form(0),
        Answer: str = Form(''),
) -> Result:
    return examineeTokenLogic.ExamAnswer(Token.strip(), ScantronID, ID, Answer.strip())