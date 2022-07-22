# -*- coding:utf-8 -*-
from Controller.BaseController import *

SysLogRouter = APIRouter()
SysLogPrefix = ''


# 系统日志列表
@SysLogRouter.post('/Sys/Log/List')
async def SysLogList(
        request: Request,
        Token: str = Form(''),
        Page: int = Form(1),
        PageSize: int = Form(10),
        Stext: str = Form(''),
        Type: int = Form(0),
        ManagerID: int = Form(0),
) -> ResultList:
    return sysLogLogic.SysLogList(Token.strip(), Page, PageSize, Stext.strip(), Type, ManagerID)


# 日志详情
@SysLogRouter.post('/Sys/Log/Info')
async def SysLogInfo(
        request: Request,
        Token: str = Form(''),
        ID: int = Form(0),
) -> Result:
    return sysLogLogic.SysLogInfo(Token.strip(), ID)