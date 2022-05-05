'''
pip install python-multipart
pip install sqlalchemy
pip install fastapi
pip install 'uvicorn[standard]'
uvicorn main:app --host=0.0.0.0 --port=6000 --reload-exclude TEXT
'''
import time
from fastapi import FastAPI, Request, Body
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse({'Code': '200', 'Memo': exc.errors()[0]['loc'][1] + ' ' + exc.errors()[0]['type'].split('.')[1]})


# API响应时间
@app.middleware("http")
async def ProcessTimeHeader(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# 测试
@app.get('/Test')
async def Test():

    class Result:
        Status = False
        Memo = ''
        Code = 200
        Data = None

    result = Result()
    result.Status = True
    result.Memo = 'Success'
    return result  # json.dumps(result.__dict__)


from Controller.ManagerController import ManagerRouter, ManagerPrefix
from Controller.ExamineeController import ExamineeRouter, ExamineePrefix

app.include_router(ManagerRouter, prefix=ManagerPrefix)
app.include_router(ExamineeRouter, prefix=ExamineePrefix)

# from CodeExec.DockerTools import CodeExecRouter, CodeExecPrefix
# app.include_router(CodeExecRouter, prefix=CodeExecPrefix)