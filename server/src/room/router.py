from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import get_db, redis_client, redis_get_value
from models import Room, RedisRoom, Moves
from room.schemas import Response, Move, GameRoom
from game import check_winner
from websockets_manager import manager

router = APIRouter(
    prefix="/room",
    tags=["Room"]
)


def create_response(result: str, result_msg: str, data: dict = None, key: int = None) -> JSONResponse:
    if key:
        manager.broadcast(key, data)
    return JSONResponse({"result": result, "result_msg": result_msg, "data": data})

def check_game_start(status: str, game: RedisRoom):
    players = game.players
    total_players = game.total_players
    empty_slots = total_players - len(players)
    game_data = GameRoom(floor=game.floor)

    if empty_slots > 0:
        return create_response(status, f"Waiting for {empty_slots} players", game_data.model_dump())


def check_game_end(status: str, key: int, game: RedisRoom):
    winner = game.player_win
    game_data = GameRoom(floor=game.floor)

    if winner:
        if winner == 'Draw':
            return create_response(status, "The game is completed. It's a draw", game_data.model_dump(), key)
        return create_response(status, f"The game is completed. {winner} wins", game_data.model_dump(), key)


def determine_next_move(moves: list, players: list, current_player: str, first_player_index: int):
    if moves:
        next_player = players[(players.index(moves[-1].player) + 1) % len(players)]
    else:
        next_player = players[first_player_index - 1]

    if next_player != current_player:
        return next_player, create_response("Warning", "It's not your turn")

    return next_player, None


# @router.get("/{key}", response_model=Response)
# async def check_game(key: int):
#     game_item = RedisRoom.model_validate_json(redis_get_value(key))
#
#     result = check_is_start_game("Success", game_item)
#     if result:
#         return result
#
#     result = check_is_end_game("Warning", game_item)
#     if result:
#         return result
#
#     return response("Success", "The game is go", game_item.model_dump())


@router.post("/move", response_model=Response)
async def move(request: Move, db: Session = Depends(get_db)):
    key = request.key
    player = request.player_name
    col = request.cell_col
    row = request.cell_row

    game_data = RedisRoom.model_validate_json(redis_get_value(key))
    players = game_data.players

    result = check_game_start("Warning", game_data)
    if result:
        return result

    result = check_game_end("Success", key, game_data)
    if result:
        return result

    next_player, result = determine_next_move(game_data.moves, players, player, game_data.player_first)
    if result:
        return result

    game_state = GameRoom(floor=game_data.floor, now_move=next_player)

    if game_data.floor[row][col]:
        return create_response("Warning", "This cell is already occupied", game_state.model_dump())


    game_data.floor[row][col] = players.index(next_player) + 1
    game_state.floor = game_data.floor
    game_data.moves.append(Moves(player=player, col=col, row=row))

    winner = check_winner(game_data.floor, game_data.size_x, game_data.size_y, game_data.condition_win)

    if not winner:
        next_player, _ = determine_next_move(game_data.moves, players, player, game_data.player_first)
        game_state.now_move = next_player

        redis_client.set(f'game:{key}', game_data.model_dump_json())
        return create_response("Success", "The game continues", game_state.model_dump(), key)
    else:
        game_data.player_win = 'Draw' if winner == 'Draw' else players[winner - 1]
        redis_client.set(f'game:{key}', game_data.model_dump_json())
        redis_client.expire(f'game:{key}', 30)

        db_game_record = Room(key=key, data=game_data.model_dump_json())
        db.add(db_game_record)
        db.commit()

        return check_game_end("Success", key, game_data)