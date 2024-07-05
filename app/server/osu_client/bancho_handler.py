from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi import Request, Response
from fastapi import Header, Depends
from uuid import uuid4
from fastapi import status
from app.server.dtos import AccountDTO, SessionDTO, StatsDTO
from app.server.repositories import queries
import app.server.login as login
from app.server.login import LoginData
from app.server import database
from app.server.actions import Action
from app.server.gamemodes import GameMode
import packets
from packets import ServerPackets


bancho_handling_router = APIRouter(default_response_class=Response, prefix="/c")


@bancho_handling_router.post("/")
async def handle_request(request: Request):
    if "osu_token" not in request.headers:
        response = await handle_login(request)

    else:
        # TODO response = implement bancho request handler
        ...
    return response

async def handle_login(request: Request):

    # Creates database (move somewhere else)
    database.configure_database()

    try:
        login_data: LoginData = login.parse_login(await request.body())
    except Exception as e:
        print(f"ERROR HANDLING LOGIN: {e}")

    account_query_result = queries.fetch_account_by_username(username=login_data["username"])

    if account_query_result is None:
        user_account: AccountDTO = queries.create_account(login_data["username"])
        queries.create_stats(user_account["user_id"])
    else:
        user_account: AccountDTO = account_query_result

    user_stats = queries.fetch_stats(user_account["user_id"])

    assert user_stats is not None


    # TODO GLOBAL RANKING
    # global_ranking = rankings.fetch_ranking(
    #     account["user_id"], stats["mode"]
    # )


    user_session: SessionDTO = queries.create_session(
        session_id=uuid4(),
        user_id=user_account["user_id"],
        username=user_account["username"],
        action=Action.IDLE,
        rank=1,
        # rank=global_ranking, # might be better to run api to find exact rank (gonna hardcode it to 1 for now)
        country=1, #TODO implement countries, lat, and lon
        mods=0,
        gamemode=GameMode.VN_OSU,
        longitude=0.0,
        latitude=0.0,
        timezone=0,
        info_text="idle", #TODO OPTIONAL create info_text enums
        # TODO! Implement beatmap fetching
        beatmap_md5="",
        beatmap_id=10,
        )

    response_data = packets.write_protocol_version(ServerPackets.VERSION_UPDATE)

    response_data += packets.write_login(user_session["user_id"])

    response_data += packets.write_user_session(
        user_id=user_session["user_id"],
        username=user_session["username"],
        timezone=user_session["timezone"],
        country=user_session["country"],
        longitude=user_session["longitude"],
        latitude=user_session["latitude"],
        rank=user_session["rank"],
        gamemode=user_session["gamemode"],
    )

    response_data += packets.write_user_stats(
        user_id=user_session["user_id"],
        action=user_session["action"],
        ranked_score=user_stats["ranked_score"],
        accuracy=user_stats["accuracy"],
        play_count=user_stats["play_count"],
        total_score=user_stats["total_score"],
        #TODO performance_points=weighted_performance_points,
        # global_rank=global_ranking,
        performance_points=7272,
        global_rank=1,
        info_text=user_session["info_text"],
        beatmap_md5=user_session["beatmap_md5"],
        mods=user_session["mods"],
        mode=user_stats["mode"],
        beatmap_id=user_session["beatmap_id"],
    )

    return Response(
            content=response_data,
            headers={"cho-token": str(user_session["session_id"])},
        )






