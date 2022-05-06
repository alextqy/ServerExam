'''
pip install python-multipart
pip install sqlalchemy
pip install fastapi
pip install 'uvicorn[standard]'
uvicorn main:app --host=0.0.0.0 --port=6000 --reload-exclude TEXT
'''
from Service.Common import *

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
async def Test(request: Request, Param: str):
    result = Result()
    # common = Common()
    result.Status = True
    result.Memo = 'Success'
    # result.Data = common.UserPWD('123456')
    # 5f1d7a84db00d2fce00b31a7fc73224f
    return result  # json.dumps(result.__dict__)


from Controller.ManagerController import ManagerRouter, ManagerPrefix
from Controller.ExamineeController import ExamineeRouter, ExamineePrefix

app.include_router(ManagerRouter, prefix=ManagerPrefix)
app.include_router(ExamineeRouter, prefix=ExamineePrefix)

# from CodeExec.DockerTools import CodeExecRouter, CodeExecPrefix
# app.include_router(CodeExecRouter, prefix=CodeExecPrefix)