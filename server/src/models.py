from typing import List

from sqlalchemy import Column, Integer, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from pydantic import BaseModel

from database import Base


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, index=True)
    key = Column(BigInteger, index=True)
    data = Column(JSONB, index=True)


class RedisRoom(BaseModel):
    all_players: int
    players: List
    player_first: int
    player_win: str
    floor: List
    size_x: int
    size_y: int
    condition_win: int
    moves: List
