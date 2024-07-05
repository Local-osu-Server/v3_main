from typing import TypedDict

class LoginData(TypedDict):
    username: str
    # password_md5: str NOT USED
    client_version: str
    timezone: int
    location: int
    client_hash: str
    block_pm: int


def parse_login(data: bytes) -> LoginData:

    username, password_md5, remainder = data.decode().split("\n", maxsplit=2)

    client_version, timezone, location, client_hash, block_pm = remainder.split("|", maxsplit=4)

    login_data: LoginData = {
        "username": username,
        "client_version": client_version,
        "timezone": int(timezone),
        "location": int(location),
        "client_hash": client_hash,
        "block_pm": int(block_pm),
    }

    return login_data
