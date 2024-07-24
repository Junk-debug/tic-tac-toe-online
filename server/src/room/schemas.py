from datetime import datetime

from pydantic import BaseModel

from models import RedisRoom


class CheckRoom(BaseModel):
    key: int


class Move(BaseModel):
    key: int
    player_name: str
    cell_col: int
    cell_row: int


class GameRoom(RedisRoom):
    key: datetime


class Response(BaseModel):
    result: str
    result_msg: str
    data: GameRoom | None = None
