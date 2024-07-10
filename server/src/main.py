from fastapi import FastAPI
import database
from lobby.router import router as router_lobby
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(swagger_ui_parameters={'defaultModelsExpandDepth': -1, "tryItOutEnabled": True})

database.Base.metadata.create_all(bind=database.engine)

app.include_router(router_lobby)

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)
