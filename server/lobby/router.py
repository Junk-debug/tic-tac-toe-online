from fastapi import APIRouter, Depends
import random
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from lobby.models import Room
from database import get_db
from lobby.schemas import RoomType, Response, GameRoom, CreateRoom, JoinTheGame

router = APIRouter(
    prefix="/lobby",
    tags=["Lobby"]
)


def make_dict(item: GameRoom) -> dict:
    return {
        'id': item.id,
        'type_room': item.type_room,
        'game_field': item.game_field,
        'key': item.key,
        'player_1': item.player_1,
        'player_2': item.player_2,
        'wins_first_user': item.wins_first_user,
        'wins_second_user': item.wins_second_user,
        'draws': item.draws,
        'game_status': item.game_status
    }


@router.post("/create_game", response_model=Response)
async def create_game(request: CreateRoom, db: Session = Depends(get_db)):
    type_room = request.type_room
    player_1 = request.player_1
    game_field = []
    if type_room == RoomType.standard:
        game_field = [0] * 9
    key = random.randint(100000000, 999999999)
    db_item = Room(type_room=type_room.value,
                   game_field=game_field,
                   key=key,
                   player_1=player_1,
                   game_status='Waiting second player')
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return JSONResponse({"result": "success", "result_msg": "Game created", "data": make_dict(db_item)}, 200)


@router.post("/join_the_game", response_model=Response)
async def join_the_game(request: JoinTheGame, db: Session = Depends(get_db)):
    key = request.key
    player_2 = request.player_2
    item = db.query(Room).filter(Room.key == key).first()
    if not item:
        return JSONResponse({"result": "error", "result_msg": "Not found", "data": None}, 404)
    item.player_2 = player_2
    item.game_status = "Game start"
    db.commit()
    db.refresh(item)
    return JSONResponse({"result": "success", "result_msg": "Joined game successfully", "data": make_dict(item)}, 200)
