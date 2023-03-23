# -*- coding:utf-8 -*-
'''
pip install python-multipart
pip install pymysql
pip install sqlalchemy
pip install redis
pip install xlrd
pip install fastapi
pip install 'uvicorn[standard]'
pip install requests
uvicorn main:app --host=0.0.0.0 --port=60000 --reload-exclude TEXT
'''
from Service.Common import *
from Service.UDPTool import *
from Service.RedisHelper import *

import warnings

warnings.filterwarnings("ignore")

app = FastAPI()


# 异常输出
@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse({'Code': '200', 'Memo': exc.errors()[0]['loc'][1] + ' ' + exc.errors()[0]['type'].split('.')[1]})


# API响应时间
@app.middleware('http')
async def ProcessTimeHeader(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    process_time = time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response


# 测试
@app.get('/Test')
async def Test(request: Request, Param1: str, Param2: str, Param3: str):
    result = Result()
    # c = Common()
    # r = RedisHelper()
    result.State = True
    result.Memo = 'Success'
    result.Data = Param1 + Param2 + Param3
    return result  # json.dumps(result.__dict__)


from Controller.SysLogController import SysLogRouter, SysLogPrefix
from Controller.ExamLogController import ExamLogRouter, ExamLogPrefix
from Controller.ManagerController import ManagerRouter, ManagerPrefix
from Controller.SubjectController import SubjectRouter, SubjectPrefix
from Controller.PaperController import PaperRouter, PaperPrefix
from Controller.PaperRuleController import PaperRuleRouter, PaperRulePrefix
from Controller.KnowledgeController import KnowledgeRouter, KnowledgePrefix
from Controller.HeadlineController import HeadlineRouter, HeadlinePrefix
from Controller.QuestionController import QuestionRouter, QuestionPrefix
from Controller.QuestionSolutionController import QuestionSolutionRouter, QuestionSolutionPrefix
from Controller.ClassController import ClassRouter, ClassPrefix
from Controller.TeacherController import TeacherRouter, TeacherPrefix
from Controller.ExamineeController import ExamineeRouter, ExamineePrefix
from Controller.ExamineeTokenController import ExamineeTokenRouter, ExamineeTokenPrefix
from Controller.ExamInfoController import ExamInfoRouter, ExamInfoPrefix
from Controller.ExamInfoHistoryController import ExamInfoHistoryRouter, ExamInfoHistoryPrefix
from Controller.ScantronController import ScantronRouter, ScantronPrefix
from Controller.ScantronHistoryController import ScantronHistoryRouter, ScantronHistoryPrefix
from Controller.ScantronSolutionController import ScantronSolutionRouter, ScantronSolutionPrefix
from Controller.ScantronSolutionHistoryController import ScantronSolutionHistoryRouter, ScantronSolutionHistoryPrefix
from Controller.SysConfController import SysConfRouter, SysConfPrefix
from Controller.PracticeController import PracticeRouter, PracticePrefix
from Controller.TeacherClassController import TeacherClassRouter, TeacherClassPrefix

from CodeExec.DockerTools import CodeExecRouter, CodeExecPrefix

app.include_router(SysLogRouter, prefix=SysLogPrefix)
app.include_router(ExamLogRouter, prefix=ExamLogPrefix)
app.include_router(ManagerRouter, prefix=ManagerPrefix)
app.include_router(SubjectRouter, prefix=SubjectPrefix)
app.include_router(PaperRouter, prefix=PaperPrefix)
app.include_router(PaperRuleRouter, prefix=PaperRulePrefix)
app.include_router(KnowledgeRouter, prefix=KnowledgePrefix)
app.include_router(HeadlineRouter, prefix=HeadlinePrefix)
app.include_router(QuestionRouter, prefix=QuestionPrefix)
app.include_router(QuestionSolutionRouter, prefix=QuestionSolutionPrefix)
app.include_router(ClassRouter, prefix=ClassPrefix)
app.include_router(TeacherRouter, prefix=TeacherPrefix)
app.include_router(ExamineeRouter, prefix=ExamineePrefix)
app.include_router(ExamineeTokenRouter, prefix=ExamineeTokenPrefix)
app.include_router(ExamInfoRouter, prefix=ExamInfoPrefix)
app.include_router(ExamInfoHistoryRouter, prefix=ExamInfoHistoryPrefix)
app.include_router(ScantronRouter, prefix=ScantronPrefix)
app.include_router(ScantronHistoryRouter, prefix=ScantronHistoryPrefix)
app.include_router(ScantronSolutionRouter, prefix=ScantronSolutionPrefix)
app.include_router(ScantronSolutionHistoryRouter, prefix=ScantronSolutionHistoryPrefix)
app.include_router(SysConfRouter, prefix=SysConfPrefix)
app.include_router(PracticeRouter, prefix=PracticePrefix)
app.include_router(TeacherClassRouter, prefix=TeacherClassPrefix)

app.include_router(CodeExecRouter, prefix=CodeExecPrefix)

UDPTool = UDPTool()

import sched

s = sched.scheduler(time, sleep)


# 使劲池
def EventPool(sc):
    # print(Common().TimeMS()) # test
    UDPTool.SendBroadcast()  # 发送UDP信息
    sc.enter(3, 1, EventPool, (sc, ))


# 运行事件池
def EventScheduler():
    s.enter(5, 1, EventPool, (s, ))
    s.run()


# 系统启动时执行
@app.on_event('startup')
async def StartupEvent():
    thread = Thread(target=EventScheduler)
    thread.start()


def run():
    StartupEvent()
    _common = Common()
    ConfigObj: dict = _common.ReadJsonFile(path[0] + '/config.json')
    uvicorn.run('main:app', host='192.168.0.29', port=int(ConfigObj['UDPPort']), reload=True)  # Common().LocalIP()


import uvicorn
if __name__ == '__main__':
    run()