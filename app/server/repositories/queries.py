# TODO break up into seperate repos
from __future__ import annotations

from datetime import datetime
from typing import cast

from sqlmodel import Session, select

from app.server.database import ENGINE, Accounts, Sessions, Stats
from app.server.dtos import AccountDTO, SessionDTO, StatsDTO
from app.server.gamemodes import GameMode

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
