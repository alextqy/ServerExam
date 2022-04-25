from fastapi import FastAPI, Request, Body
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# pip install requests
# pip 
# pip install fastapi
# pip install 'uvicorn[standard]'
# uvicorn main:app --host=0.0.0.0 --port=8080 --reload
app = FastAPI()


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse({'Code': '200', 'Memo': exc.errors()[0]['loc'][1] + ' ' + exc.errors()[0]['type'].split('.')[1]})


# app.include_router(, prefix=)