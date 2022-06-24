from Controller.BaseController import *

PracticeRouter = APIRouter()
PracticePrefix = ''


# 刷题登陆
@PracticeRouter.post('/Sign/In/Practice')
async def SignInPractice(
        request: Request,
        ExamineeNo: str = Form(''),
) -> Result:
    return practiceLogic.SignInPractice(ExamineeNo)


# 随机抽取一道指定类型的试题
@PracticeRouter.post('/New/Practice')
async def NewPractice(
        request: Request,
        Token: str = Form(''),
        QuestionType: int = Form(0),
) -> Result:
    return practiceLogic.NewPractice(Token, QuestionType)


# 获取试题信息
@PracticeRouter.post('/Practice/Info')
async def PracticeInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return practiceLogic.PracticeInfo(Token, ID)
