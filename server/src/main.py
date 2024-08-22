from fastapi import FastAPI, Request

from database import Base, engine
from exceptions import HTTPExceptionEx
from lobby.router import router as router_lobby
from server.save.router import router as router_room
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title='Tic Tac Toe', swagger_ui_parameters={'defaultModelsExpandDepth': -1, "tryItOutEnabled": True})

Base.metadata.create_all(bind=engine)

app.include_router(router_lobby)
app.include_router(router_room)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.exception_handler(HTTPExceptionEx)
async def unicorn_exception_handler(request: Request, exc: HTTPExceptionEx):
    content = {'result': exc.result, "result_msg": exc.result_msg, "data": None}
    return JSONResponse(status_code=exc.status_code, content=content, headers=exc.headers)
