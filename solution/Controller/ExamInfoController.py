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
) -> Result:
    return examInfoLogic.NewExamInfo(request.client.host, Token.strip(), SubjectName.strip(), ExamNo.strip(), ExamineeID)


# 报名作废
@ExamInfoRouter.post('/ExamInfo/Disabled')
async def ExamInfoDisabled(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return examInfoLogic.ExamInfoDisabled(request.client.host, Token.strip(), ID)