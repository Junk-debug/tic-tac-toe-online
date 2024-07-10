from fastapi import FastAPI
import database
from lobby.router import router as router_lobby
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(swagger_ui_parameters={'defaultModelsExpandDepth': -1, "tryItOutEnabled": True})

database.Base.metadata.create_all(bind=database.engine)

app.include_router(router_lobby)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
