from Controller.BaseController import *

ExamineeRouter = APIRouter()
ExamineePrefix = ''


# 添加考生
@ExamineeRouter.post('/new/examinee')
async def NewExaminee(request: Request, Name: str = Form(''), ExamineeNo: str = Form(''), Contact: str = Form('')) -> Result:
    return examineeLogic.NewExaminee(Name, ExamineeNo, Contact)


# 删除考生
@ExamineeRouter.post('/delete/examinee')
async def DeleteExaminee(request: Request, ID: int = Form(0)) -> Result:
    return examineeLogic.DeleteExaminee(ID)


# 更新考生信息
@ExamineeRouter.post('/update/examinee')
async def UpdateExaminee(request: Request, ID: int = Form(0), Name: str = Form(''), ExamineeNo: str = Form(''), Contact: str = Form('')) -> Result:
    return examineeLogic.UpdateExaminee(ID, Name, ExamineeNo, Contact)


# 查询考生
@ExamineeRouter.post('/find/examinee')
async def FindExaminee(request: Request, ID: int = Form(0)) -> Result:
    return examineeLogic.FindExaminee(ID)


# 考生列表
@ExamineeRouter.post('/list/examinee')
async def ListExaminee(request: Request, Page: int = Form(1), PageSize: int = Form(10), Stext: str = Form('')) -> Result:
    return examineeLogic.ListExaminee(Page, PageSize, Stext)