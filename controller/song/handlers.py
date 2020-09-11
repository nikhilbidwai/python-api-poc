from fastapi import APIRouter, Depends
from utils.exception.exception import error_responses
from utils.logger.logger import api_logger as logger
from utils.interfaces.interfaces import get, put

from controller.song.models.song import SongRequest, SongResponse
from config.interface_config import ADD_SONG, GET_SONG

from utils.security.security import User, get_current_active_user

song_router = APIRouter()


@song_router.get(
    "/",
    responses={**error_responses, 200: {}}
)
async def status(current_user: User = Depends(get_current_active_user)):
    logger.info("API execution started")
    response = get("/")
    return response.json()


@song_router.put(
    "/song/{song_id}",
    response_model=SongResponse,
    responses={**error_responses, 200: {}}
)
async def add_song(song_id: int, song: SongRequest):
    logger.info("API execution started")
    response = put(ADD_SONG.format(song_id), data=song.json())
    return response.json()


@song_router.get(
    "/song/{song_id}",
    responses={**error_responses, 200: {}}
)
async def get_song(song_id: int):
    logger.info("API execution started")
    response = get(GET_SONG.format(song_id))
    return response.json()
