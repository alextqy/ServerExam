# -*- coding:utf-8 -*-
from Controller.BaseController import *

ExamInfoRouter = APIRouter()
ExamInfoPrefix = ''


# 新建报名
@ExamInfoRouter.post('/New/ExamInfo')
async def NewExamInfo(
        request: Request,
        Token: str = Form(''),
        SubjectName: str = Form(''),
        ExamNo: str = Form(''),
        ExamineeNo: str = Form(''),
        ExamType: int = Form(0),
):
    return examInfoLogic.NewExamInfo(request.client.host, Token.strip(), SubjectName.strip(), ExamNo.strip(), ExamineeNo, ExamType)


# 报名作废
@ExamInfoRouter.post('/ExamInfo/Disabled')
async def ExamInfoDisabled(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
):
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
        Pass: int = Form(0),
        StartState: int = Form(0),
        SuspendedState: int = Form(0),
        ExamineeID: int = Form(0),
):
    return examInfoLogic.ExamInfoList(Token.strip(), Page, PageSize, Stext.strip(), ExamState, ExamType, Pass, StartState, SuspendedState, ExamineeID)


# 报名详情
@ExamInfoRouter.post('/ExamInfo')
async def ExamInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
):
    return examInfoLogic.ExamInfo(Token.strip(), ID)


# 生成试卷
@ExamInfoRouter.post('/Generate/Test/Paper')
async def GenerateTestPaper(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
):
    return examInfoLogic.GenerateTestPaper(request.client.host, Token.strip(), ID)


# 重置报名试题数据
@ExamInfoRouter.post('/Reset/Exam/Question/Data')
async def ResetExamQuestionData(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
):
    return examInfoLogic.ResetExamQuestionData(request.client.host, Token.strip(), ID)


# 报名转入历史
@ExamInfoRouter.post('/Exam/Into/History')
async def ExamIntoHistory(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
):
    return examInfoLogic.ExamIntoHistory(request.client.host, Token.strip(), ID)


# 打分
@ExamInfoRouter.post('/Grade/The/Exam')
async def GradeTheExam(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
):
    return examInfoLogic.GradeTheExam(request.client.host, Token.strip(), ID)


# 导入报名
@ExamInfoRouter.post('/Import/Exam/Info')
async def ImportExamInfo(
        request: Request,
        Token: str = Form(''),
        ExcelFile: UploadFile = File(...),
        ContentType: str = Form(''),
):
    Contents: bytes = await ExcelFile.read()
    return examInfoLogic.ImportExamInfo(request.client.host, Token.strip(), ContentType, Contents)


# 下载导入文件Demo
@ExamInfoRouter.post('/Download/Exam/Info/Demo')
async def DownloadExamInfoDemo(
        request: Request,
        Token: str = Form(''),
):
    return examInfoLogic.DownloadExamInfoDemo(Token.strip())


# 报名暫停
@ExamInfoRouter.post('/ExamInfo/Suspend')
async def ExamInfoSuspend(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
):
    return examInfoLogic.ExamInfoSuspend(request.client.host, Token.strip(), ID)