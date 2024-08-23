from starlette.websockets import WebSocketDisconnect, WebSocket
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db, redis_client, redis_get_value
from models import Room, RedisRoom, Moves
from room.schemas import Response, Move, GameRoom
from game import check_winner
from room.websockets_manager import manager

router = APIRouter(
    prefix="/room",
    tags=["Room"]
)


async def create_response(response: Response, websocket: WebSocket, key: int):
    if response.result == 'Warning':
        await manager.send_personal_message(response.model_dump(), websocket)
    else:
        await manager.broadcast(key, response.model_dump())


def check_game_start(game: RedisRoom):
    players = game.players
    total_players = game.total_players
    empty_slots = total_players - len(players)

    if empty_slots > 0:
        return Response(result='Warning', result_msg=f"Waiting for {empty_slots} players")


def check_game_end(status: str, game: RedisRoom):
    winner = game.player_win
    game_data = GameRoom(floor=game.floor)

    if winner:
        if winner == 'Draw':
            return Response(result=status, result_msg="The game is completed. It's a draw", data=game_data.model_dump())
        return Response(result=status, result_msg=f"The game is completed. {winner} wins", data=game_data.model_dump())


def determine_next_move(moves: list, players: list, first_player_index: int):
    if moves:
        next_player = players[(players.index(moves[-1].player) + 1) % len(players)]
    else:
        next_player = players[first_player_index - 1]

    return next_player


def move(key, request: Move, db: Session = Depends(get_db)):
    player = request.player_name
    col = request.cell_col
    row = request.cell_row

    game_data = RedisRoom.model_validate_json(redis_get_value(key))
    players = game_data.players

    result = check_game_start(game_data)
    if result:
        return result

    result = check_game_end("Warning", game_data)
    if result:
        return result

    next_player = determine_next_move(game_data.moves, players, game_data.player_first)
    if  next_player != player:
        return Response(result="Warning", result_msg="It's not your turn")

    game_state = GameRoom(floor=game_data.floor, now_move=next_player)

    if game_data.floor[row][col]:
        return Response(result="Warning", result_msg="This cell is already occupied")


    game_data.floor[row][col] = players.index(next_player) + 1
    game_state.floor = game_data.floor
    game_data.moves.append(Moves(player=player, col=col, row=row))

    winner = check_winner(game_data.floor, game_data.size_x, game_data.size_y, game_data.condition_win)

    if not winner:
        next_player = determine_next_move(game_data.moves, players, game_data.player_first)
        game_state.now_move = next_player

        redis_client.set(f'game:{key}', game_data.model_dump_json())
        return Response(result="Success", rsult_msg="The game continues", data=game_state.model_dump())
    else:
        game_data.player_win = 'Draw' if winner == 'Draw' else players[winner - 1]
        redis_client.set(f'game:{key}', game_data.model_dump_json())
        redis_client.expire(f'game:{key}', 30)

        db_game_record = Room(key=key, data=game_data.model_dump_json())
        db.add(db_game_record)
        db.commit()

        return check_game_end("Success", game_data)

@router.websocket("/ws/{game_key}")
async def websocket_endpoint(websocket: WebSocket, game_key: int):
    await manager.connect(game_key, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            item = Move.model_validate_json(data)
            response = move(game_key, item)
            await create_response(response, websocket, game_key)
    except WebSocketDisconnect:
        await manager.disconnect(game_key, websocket)
        await manager.broadcast(game_key, f"Player left the game.")
