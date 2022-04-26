'''
pip install fastapi
pip install 'uvicorn[standard]'
uvicorn main:app --host=0.0.0.0 --port=6000 --reload-exclude TEXT
'''
from fastapi import FastAPI, Request, Body
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse({'Code': '200', 'Memo': exc.errors()[0]['loc'][1] + ' ' + exc.errors()[0]['type'].split('.')[1]})


@app.get('/test')
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


from Controller.ExamineeController import ExamineeRouter, ExamineePrefix

app.include_router(ExamineeRouter, prefix=ExamineePrefix)