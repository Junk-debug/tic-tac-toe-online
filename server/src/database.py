import json

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from redis import Redis

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, REDIS_HOST, REDIS_PORT, REDIS_DB
from exceptions import HTTPExceptionEx

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

Base = declarative_base(metadata=metadata)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


def redis_get_value(key):
    item = redis_client.get(f'game:{key}')

    if not item:
        raise HTTPExceptionEx(424, "Error", "Not found")

    json_str = json.loads(item.decode('utf-8'))
    return json_str
