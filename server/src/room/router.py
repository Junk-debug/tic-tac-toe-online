from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import get_db, redis_client, redis_get_value
from models import Room, RedisRoom, Moves
from room.schemas import Response, CheckRoom, Move
from game import check_winner

router = APIRouter(
    prefix="/room",
    tags=["Room"]
)


def response(result: str, result_msg: str, data: dict = None) -> JSONResponse:
    return JSONResponse({"result": result, "result_msg": result_msg, "data": data})


def check_is_start_game(item: RedisRoom):
    players = item.players
    all_players = item.all_players
    empty_places = all_players - len(players)

    if empty_places:
        return response("Success", f"Waiting for {empty_places}", item.dict())


def check_is_end_game(item: RedisRoom):
    player_win = item.player_win

    if player_win:
        if player_win == 'Draw':
            return response("Success", "The game is completed. Draw", item.dict())
        return response("Success", f"The game is completed. Win {player_win}", item.dict())


def check_who_move(moves: list, players: list, player: str, player_first: int):
    if moves:
        who_move = players[(players.index(moves[-1].player) + 1) % len(players)]
    else:
        who_move = players[player_first - 1]

    if who_move != player:
        return who_move, response("Success", f"Now is not your move")

    return who_move, None


@router.post("/check_game", response_model=Response)
async def check_game(request: CheckRoom):
    key = request.key
    game_item = RedisRoom.parse_raw(redis_get_value(key))

    result = check_is_start_game(game_item)
    if result:
        return result

    result = check_is_end_game(game_item)
    if result:
        return result

    return response("Success", "The game is go", game_item.dict())


@router.post("/move", response_model=Response)
async def move(request: Move, db: Session = Depends(get_db)):
    key = request.key
    player = request.player_name
    col = request.cell_col
    row = request.cell_row
    game_item = RedisRoom.parse_raw(redis_get_value(key))
    players = game_item.players

    result = check_is_start_game(game_item)
    if result:
        return result

    result = check_is_end_game(game_item)
    if result:
        return result

    who_move, result = check_who_move(game_item.moves, players, player, game_item.player_first)
    if result:
        return result

    floor = game_item.floor
    if floor[row][col]:
        return response("Success", 'This cell is already busy', game_item.dict())

    floor[row][col] = players.index(who_move) + 1
    game_item.floor = floor
    game_item.moves.append(Moves(player=player, col=col, row=row))

    winner = check_winner(floor, game_item.size_x, game_item.size_y, game_item.condition_win)

    if not winner:
        redis_client.set(f'game:{key}', game_item.json())
        return response("Success", "The game is go", game_item.dict())
    else:
        game_item.player_win = 'Draw' if winner == 'Draw' else players[winner-1]
        redis_client.set(f'game:{key}', game_item.json())
        redis_client.expire(f'game:{key}', 30)

        db_item = Room(
            key=key,
            data=game_item.json()
        )
        db.add(db_item)
        db.commit()

        return check_is_end_game(game_item)
