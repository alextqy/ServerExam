# -*- coding:utf-8 -*-
from Controller.BaseController import *

TeacherRouter = APIRouter()
TeacherPrefix = ''


# 管理员登录
@TeacherRouter.post('/New/Teacher')
async def NewTeacher(
        request: Request,
        Token: str = Form(''),
        Account: str = Form(''),
        Password: str = Form(''),
        Name: str = Form(''),
):
    return teacherLogic.NewTeacher(request.client.host, Token.strip(), Account.strip(), Password.strip(), Name.strip())


# 禁用/启用 教师
@TeacherRouter.post('/Teacher/Disabled')
async def TeacherDisabled(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
):
    return teacherLogic.TeacherDisabled(request.client.host, Token.strip(), ID)


# 更新教师信息
@TeacherRouter.post('/Update/Teacher/Info')
async def UpdateTeacherInfo(
        request: Request,
        Token: str = Form(''),
        Password: str = Form(''),
        Name: str = Form(''),
        ID: int = Form(0),
):
    return teacherLogic.UpdateTeacherInfo(request.client.host, Token.strip(), Password.strip(), Name.strip(), ID)


# 教师列表
@TeacherRouter.post('/Teacher/List')
async def TeacherList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        Stext: str = Form(''),
        State: int = Form(0),
):
    return teacherLogic.TeacherList(Token.strip(), Page, PageSize, Stext.strip(), State)


# 教师详情
@TeacherRouter.post('/Teacher/Info')
async def TeacherInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
):
    return teacherLogic.TeacherInfo(Token.strip(), ID)


# 全部教师
@TeacherRouter.post('/Teachers')
async def Teachers(
        request: Request,
        Token: str = Form(''),
):
    return teacherLogic.Teachers(Token.strip())


# ========================================================================= teacher side =========================================================================


# 教师登录
@TeacherRouter.post('/Teacher/Sign/In')
async def TeacherSignIn(
        request: Request,
        Account: str = Form(''),
        Password: str = Form(''),
):
    return teacherLogic.TeacherSignIn(request.client.host, Account.strip(), Password.strip())


# 教师退出
@TeacherRouter.post('/Teacher/Sign/Out')
async def TeacherSignOut(
        request: Request,
        Token: str = Form(''),
):
    return teacherLogic.TeacherSignOut(request.client.host, Token.strip())


# 教师详情
@TeacherRouter.post('/Check/Teacher/Info')
async def CheckTeacherInfo(
        request: Request,
        Token: str = Form(''),
):
    return teacherLogic.CheckTeacherInfo(Token.strip())


# 更新教师信息
@TeacherRouter.post('/Teacher/Update')
async def TeacherUpdate(
        request: Request,
        Token: str = Form(''),
        Name: str = Form(''),
):
    return teacherLogic.TeacherUpdate(request.client.host, Token.strip(), Name.strip())


# 教师修改密码
@TeacherRouter.post('/Teacher/Change/Password')
async def TeacherChangePassword(
        request: Request,
        Token: str = Form(''),
        NewPassword: str = Form(''),
):
    return teacherLogic.TeacherChangePassword(request.client.host, Token.strip(), NewPassword.strip())


# 教师所在班级列表
@TeacherRouter.post('/The/Teacher/Class')
async def TheTeacherClass(
        request: Request,
        Token: str = Form(''),
):
    return teacherLogic.TheTeacherClass(Token.strip())


# 班级考生列表
@TeacherRouter.post('/Teacher/Examinee/List')
async def TeacherExamineeList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        Stext: str = Form(''),
        ClassID: int = Form(0),
):
    return teacherLogic.TeacherExamineeList(Token.strip(), Page, PageSize, Stext.strip(), ClassID)


# 教师添加考生
@TeacherRouter.post('/Teacher/New/Examinee')
async def TeacherNewExaminee(
        request: Request,
        Token: str = Form(''),
        ExamineeNo: str = Form(''),
        Name: str = Form(''),
        ClassID: int = Form(0),
        Contact: str = Form(''),
):
    return teacherLogic.TeacherNewExaminee(request.client.host, Token.strip(), ExamineeNo.strip(), Name.strip(), ClassID, Contact.strip())


# 更新考生信息
@TeacherRouter.post('/Teacher/Update/Examinee')
async def TeacherUpdateExaminee(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
        Name: str = Form(''),
        Contact: str = Form(''),
        ClassID: int = Form(0),
):
    return teacherLogic.TeacherUpdateExaminee(request.client.host, Token.strip(), ID, Name.strip(), Contact.strip(), ClassID)


# 班级下考生报名列表
@TeacherRouter.post('/Teacher/ExamInfo/List')
async def TeacherExamInfoList(
        request: Request,
        Token: str = Form(''),
        Type: int = Form(0),
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
    return teacherLogic.TeacherExamInfoList(Token.strip(), Type, Page, PageSize, Stext.strip(), ExamState, ExamType, Pass, StartState, SuspendedState, ExamineeID)


# 考生答题卡列表
@TeacherRouter.post('/Teacher/Scantron/List')
async def TeacherScantronList(
        request: Request,
        Token: str = Form(''),
        Type: int = Form(0),
        Page: int = Form(1),
        PageSize: int = Form(10),
        ExamID: int = Form(0),
):
    return teacherLogic.TeacherScantronList(Token.strip(), Type, Page, PageSize, ExamID)


# 教师查看答题卡附件
@TeacherRouter.post('/Teacher/Scantron/View/Attachments')
async def TeacherScantronViewAttachments(
        request: Request,
        Token: str = Form(''),
        FilePath: str = Form(''),
):
    return teacherLogic.TeacherScantronViewAttachments(Token.strip(), FilePath)


# 考生答题卡选项列表
@TeacherRouter.post('/Teacher/Scantron/Solution/List')
async def TeacherScantronSolutionList(
        request: Request,
        Token: str = Form(''),
        Type: int = Form(0),
        Page: int = Form(1),
        PageSize: int = Form(10),
        ScantronID: int = Form(0),
        Position: int = Form(0),
):
    return teacherLogic.TeacherScantronSolutionList(Token.strip(), Type, Page, PageSize, ScantronID, Position)


# 考生答题卡附件查看
@TeacherRouter.post('/Teacher/Scantron/Solution/View/Attachments')
async def TeacherScantronSolutionViewAttachments(
        request: Request,
        Token: str = Form(''),
        OptionAttachment: str = Form(''),
):
    return teacherLogic.TeacherScantronSolutionViewAttachments(Token.strip(), OptionAttachment)


# 教师获取全部科目
@TeacherRouter.post('/Teacher/Subjects')
async def TeacherSubjects(
        request: Request,
        Token: str = Form(''),
):
    return teacherLogic.TeacherSubjects(Token.strip())


# 教师新建报名
@TeacherRouter.post('/Teacher/New/ExamInfo')
async def TeacherNewExamInfo(
        request: Request,
        Token: str = Form(''),
        SubjectName: str = Form(''),
        ExamNo: str = Form(''),
        ExamineeNo: str = Form(''),
        ExamType: int = Form(0),
):
    return teacherLogic.TeacherNewExamInfo(request.client.host, Token.strip(), SubjectName.strip(), ExamNo.strip(), ExamineeNo, ExamType)