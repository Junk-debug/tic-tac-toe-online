from  typing import List

from pydantic import BaseModel


class Move(BaseModel):
    player_name: str
    cell_col: int
    cell_row: int


class GameRoom(BaseModel):
    floor: List[List[int]]
    now_move: str | None = None


class Response(BaseModel):
    result: str
    result_msg: str
    data: GameRoom | None = None
