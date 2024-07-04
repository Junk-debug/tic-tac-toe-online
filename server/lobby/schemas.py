from enum import Enum
from typing import List

from pydantic import BaseModel


class RoomType(Enum):
    standard: str = '3x3'
    big: str = '19x19'


class CreateRoom(BaseModel):
    type_room: RoomType
    player_1: str


class JoinTheGame(BaseModel):
    key: int
    player_2: str


class HttpResult(BaseModel):
    result: str
    result_msg: str


class GameRoom(BaseModel):
    id: int
    type_room: RoomType
    game_field: List[int]
    key: int
    player_1: str
    player_2: str
    wins_first_user: int
    wins_second_user: int
    draws: int
    game_status: str


class Response(HttpResult):
    data: GameRoom | None = None

