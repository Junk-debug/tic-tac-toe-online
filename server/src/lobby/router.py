from time import time
import random

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from exceptions import HTTPExceptionEx
from game import checking_the_created_field
from lobby.schemas import Response, CreateRoom, JoinTheGame
from database import redis_client, redis_get_value
from models import RedisRoom

router = APIRouter(
    prefix="/lobby",
    tags=["Lobby"]
)


def response(result: str, result_msg: str, data: dict = None) -> JSONResponse:
    return JSONResponse({"result": result, "result_msg": result_msg, "data": data})


def generate_key_playerfirst_and_floor(player_first: int, size_x: int, size_y: int, all_players: int):
    player_first = random.randint(1, all_players) if player_first == 0 else player_first
    game_floor = [[0] * size_x for _ in range(size_y)]
    key = int(time() * 1000)
    return key, player_first, game_floor


@router.post("/create_game", response_model=Response)
async def create_game(request: CreateRoom):
    all_players = request.all_players
    player_name = request.player_name
    size_x = request.size_x
    size_y = request.size_y
    condition_win = request.condition_win
    first = request.player_first

    result = checking_the_created_field(all_players, size_x, size_y, condition_win)
    if result:
        raise HTTPExceptionEx(422, "Error", result)

    key, player_first, game_floor = generate_key_playerfirst_and_floor(first, size_x, size_y, all_players)

    item_redis = RedisRoom(all_players=all_players,
                           players=[player_name],
                           player_first=player_first,
                           player_win='',
                           floor=game_floor,
                           size_x=size_x,
                           size_y=size_y,
                           condition_win=condition_win,
                           moves=[])
    redis_client.set(f'game:{key}', item_redis.json())

    item_room = item_redis.dict()
    item_room['key'] = key
    return response("Success", "Game created", item_room)


@router.post("/join_the_game", response_model=Response)
async def join_the_game(request: JoinTheGame):
    key = request.key
    player_name = request.player_name
    game_item = RedisRoom.parse_raw(redis_get_value(key))
    all_players = game_item.all_players
    players = len(game_item.players)

    if players == all_players:
        return response("Warning", "In the game already the maximum number of players")

    game_item.players.append(player_name)
    redis_client.set(f'game:{key}', game_item.json())

    empty_places = all_players - players - 1

    item_room = game_item.dict()
    item_room['key'] = key
    if empty_places:
        return response("Success", f"Joined room successfully. Waiting for {empty_places}", item_room)

    return response("Success", f"Joined room successfully. Game started", item_room)
