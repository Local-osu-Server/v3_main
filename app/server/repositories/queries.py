from __future__ import annotations

from datetime import datetime
from typing import cast
from uuid import UUID

from sqlmodel import Session, select

from app.server.actions import Action
from app.server.database import ENGINE, Accounts, Sessions, Stats
from app.server.dtos import AccountDTO, SessionDTO, StatsDTO
from app.server.gamemodes import GameMode

# TODO!!! break up into seperate repos

# Accounts
def create_account(username: str) -> AccountDTO:
    try:
        with Session(ENGINE) as session:
            new_account = Accounts(username=username)
            session.add(new_account)

    except Exception as e:
        print(f"ERROR CREATING ACCOUNT: {e}")

    return cast(AccountDTO, new_account)


def fetch_account_by_username(username: str) -> AccountDTO | None:
    try:
        with Session(ENGINE) as session:
            query = select(Accounts).where(Accounts.username == username)
            account = session.exec(query)

    except Exception as e:
        print(f"ERROR FETCHING ACCOUNT: {e}")

    return cast(AccountDTO, account) if account is not None else None


# Stats
def create_stats(user_id: int):
    game_modes = {mode_name: mode for mode_name, mode in vars(GameMode).items()}

    try:
        with Session(ENGINE) as session:
            for mode_name, mode in game_modes:
                if mode_name.startswith("__"):
                    continue

                new_stats = Stats(user_id=user_id, mode_name=mode_name, mode=int(mode))
                session.add(new_stats)

    except Exception as e:
        print(f"ERROR CREATING STATS: {e}")


def fetch_stats(user_id: int) -> StatsDTO | None:
    try:
        with Session(ENGINE) as session:
            query = select(Stats).where(Stats.user_id == user_id)
            stats = session.exec(query)

    except Exception as e:
        print(f"ERROR FETCHING STATS: {e}")

    return cast(StatsDTO, stats) if stats is not None else None


# Session
def create_session(
    session_id: UUID,
    user_id: int,
    username: str,
    action: Action,
    rank: int,
    country: int,
    mods: int,
    gamemode: GameMode,
    longitude: float,
    latitude: float,
    timezone: int,
    info_text: str,
    beatmap_md5: str,
    beatmap_id: int,
) -> SessionDTO:
    try:
        with Session(ENGINE) as session:
            new_session = Sessions(
                session_id=str(session_id),
                user_id=user_id,
                username=username,
                action=int(action),
                rank=rank,
                country=country,
                mods=mods,
                gamemode=int(gamemode),
                longitude=longitude,
                latitude=latitude,
                timezone=timezone,
                info_text=info_text,
                beatmap_md5=beatmap_md5,
                beatmap_id=beatmap_id,
            )
            session.add(new_session)
            session.commit()

    except Exception as e:
        print(f"ERROR CREATING SESSION: {e}")

    return cast(SessionDTO, new_session)
