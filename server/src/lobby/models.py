from sqlalchemy import Column, ARRAY, Integer, String
from database import Base


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, index=True)
    type_room = Column(String, index=True)
    game_field = Column(ARRAY(Integer), index=True)
    key = Column(Integer, index=True)
    player_1 = Column(String, index=True)
    player_2 = Column(String, index=True, default='-')
    wins_first_user = Column(Integer, index=True, default=0)
    wins_second_user = Column(Integer, index=True, default=0)
    draws = Column(Integer, index=True, default=0)
    game_status = Column(String, index=True)

