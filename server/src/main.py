from fastapi import FastAPI, Request
from starlette.websockets import WebSocketDisconnect, WebSocket

from database import Base, engine
from exceptions import HTTPExceptionEx
from lobby.router import router as router_lobby
from room.router import router as router_room
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from websockets_manager import manager

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


@app.websocket("/ws/{game_key}")
async def websocket_endpoint(websocket: WebSocket, game_key: int):
    await manager.connect(game_key, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(game_key, data)
    except WebSocketDisconnect:
        await manager.disconnect(game_key, websocket)
        await manager.broadcast(game_key, f"Player left the game.")
