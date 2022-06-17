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