
# TODO implement base configuration and aggregator HERE
from sqlmodel import Field, SQLModel, create_engine
from uuid import UUID, uuid4
import settings
from datetime import datetime
from app.server.gamemodes import GameMode

class Accounts(SQLModel, table=True):
    user_id: int | None = Field(primary_key=True, default=None)
    username: str = Field(unique=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())

class Sessions(SQLModel, table=True):
    user_id: int = Field(primary_key=True, index=True)
    session_id: str # casted UUID
    username: str
    action: int
    rank: int
    country: int
    mods: int
    gamemode: int = Field(default=GameMode.VN_OSU)
    longitude: float
    latitude: float
    timezone: int
    info_text: str
    beatmap_md5: str
    beatmap_id: int

class Stats(SQLModel, table=True):
    user_id: int = Field(primary_key=True, index=True)
    mode_name: str
    mode: int
    performance_points: int = Field(default=0)
    ranked_score: int = Field(default=0)
    accuracy: float = Field(default=None)
    play_count: int = Field(default=0)
    total_score: int = Field(default=0)
    global_rank: int = Field(default=None)



assert not settings.SQLLITE_FILE_NAME.endswith(".db")

sqlite_file_name = f"{settings.SQLLITE_FILE_NAME}.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

ENGINE = create_engine(sqlite_url, echo=True)

def configure_database():
    SQLModel.metadata.create_all(ENGINE)

# SQLModel.metadata.create_all(ENGINE)
