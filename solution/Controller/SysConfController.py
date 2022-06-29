# -*- coding:utf-8 -*-
from Controller.BaseController import *

SysConfRouter = APIRouter()
SysConfPrefix = ''


# 获取系统配置详情
@SysConfRouter.post('/Config/Info')
async def ConfigInfo(
        request: Request,
        Token: str = Form(''),
        Key: str = Form(''),
) -> Result:
    return sysConfLogic.ConfigInfo(Token.strip(), Key.strip())