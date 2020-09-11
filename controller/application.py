
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from middleware.access_log_middleware import AccessLogMiddleware, RequestIdMiddleware
from middleware.cors_middleware import origins

from config.application_config import ACCESS_LOG
from utils.exception.exception import exception_handlers

from controller.song.handlers import song_router
from utils.security.security import fake_users_db, UserInDB, fake_hash_password

app = FastAPI(
    title="python-api-boilerplate",
    description="This API documentation is generated from the Python FastAPI.",
    version="1.0.0",
    exception_handlers=exception_handlers
)

# TODO: add Tags to the API


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    RequestIdMiddleware,
    mode="uuid"
)

app.add_middleware(
    AccessLogMiddleware,
    log_name=ACCESS_LOG
)


app.include_router(
    prefix="/api/v1/song",
    router=song_router
)

# TODO: Error response mapping
# TODO: Pass request Id during logging


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}
