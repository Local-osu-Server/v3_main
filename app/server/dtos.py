from typing import TypedDict
from datetime import datetime
from uuid import UUID

class AccountDTO(TypedDict):
    user_id: int
    username: str
    # password: str
    created_at: datetime
    updated_at: datetime


class SessionDTO(TypedDict):
    session_id: UUID
    user_id: int
    username: str
    action: int
    rank: int
    country: int
    mods: int
    gamemode: int
    longitude: float
    latitude: float
    timezone: int
    info_text: int
    beatmap_md5: str
    beatmap_id: int

class StatsDTO(TypedDict):
    user_id: int
    mode_name: str
    mode: int
    performance_points: int
    ranked_score: int
    accuracy: float
    play_count: int
    total_score: int
    global_rank: int
