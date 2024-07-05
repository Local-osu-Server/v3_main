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
from app.server.gamemodes import GameMode
import packets

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
        account: AccountDTO = queries.create_account(login_data["username"])
        queries.create_stats(account["user_id"])
    else:
        account: AccountDTO = account_query_result

    stats = queries.fetch_stats(account["user_id"])

    response = bytearray()






