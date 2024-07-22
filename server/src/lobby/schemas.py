from pydantic import BaseModel, Field
from models import RedisRoom
from datetime import datetime


class CreateRoom(BaseModel):
    all_players: int = Field(..., ge=2, le=5)
    player_name: str
    player_first: int
    size_x: int = Field(..., ge=3, le=20)
    size_y: int = Field(..., ge=3, le=20)
    condition_win: int = Field(..., ge=3, le=20)


class JoinTheGame(BaseModel):
    key: int
    player_name: str


class GameRoom(RedisRoom):
    key: datetime


class Response(BaseModel):
    result: str
    result_msg: str
    data: GameRoom | None = None
