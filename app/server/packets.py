import struct
from enum import IntEnum

class ServerPackets(IntEnum):
    OSU_CHANGE_ACTION = 0
    OSU_SEND_PUBLIC_MESSAGE = 1
    OSU_LOGOUT = 2
    OSU_REQUEST_STATUS_UPDATE = 3
    OSU_PING = 4
    USER_ID = 5
    SEND_MESSAGE = 7
    PONG = 8
    HANDLE_IRC_CHANGE_USERNAME = 9
    HANDLE_IRC_QUIT = 10
    USER_STATS = 11
    USER_LOGOUT = 12
    SPECTATOR_JOINED = 13
    SPECTATOR_LEFT = 14
    SPECTATE_FRAMES = 15
    OSU_START_SPECTATING = 16
    OSU_STOP_SPECTATING = 17
    OSU_SPECTATE_FRAMES = 18
    VERSION_UPDATE = 19
    OSU_ERROR_REPORT = 20
    OSU_CANT_SPECTATE = 21
    SPECTATOR_CANT_SPECTATE = 22
    GET_ATTENTION = 23
    NOTIFICATION = 24
    OSU_SEND_PRIVATE_MESSAGE = 25
    UPDATE_MATCH = 26
    NEW_MATCH = 27
    DISPOSE_MATCH = 28
    OSU_PART_LOBBY = 29
    OSU_JOIN_LOBBY = 30
    OSU_CREATE_MATCH = 31
    OSU_JOIN_MATCH = 32
    OSU_PART_MATCH = 33
    TOGGLE_BLOCK_NON_FRIEND_DMS = 34
    MATCH_JOIN_SUCCESS = 36
    MATCH_JOIN_FAIL = 37
    OSU_MATCH_CHANGE_SLOT = 38
    OSU_MATCH_READY = 39
    OSU_MATCH_LOCK = 40
    OSU_MATCH_CHANGE_SETTINGS = 41
    FELLOW_SPECTATOR_JOINED = 42
    FELLOW_SPECTATOR_LEFT = 43
    OSU_MATCH_START = 44
    ALL_PLAYERS_LOADED = 45
    MATCH_START = 46
    OSU_MATCH_SCORE_UPDATE = 47
    MATCH_SCORE_UPDATE = 48
    OSU_MATCH_COMPLETE = 49
    MATCH_TRANSFER_HOST = 50
    OSU_MATCH_CHANGE_MODS = 51
    OSU_MATCH_LOAD_COMPLETE = 52
    MATCH_ALL_PLAYERS_LOADED = 53
    OSU_MATCH_NO_BEATMAP = 54
    OSU_MATCH_NOT_READY = 55
    OSU_MATCH_FAILED = 56
    MATCH_PLAYER_FAILED = 57
    MATCH_COMPLETE = 58
    OSU_MATCH_HAS_BEATMAP = 59
    OSU_MATCH_SKIP_REQUEST = 60
    MATCH_SKIP = 61
    UNAUTHORIZED = 62  # unused
    OSU_CHANNEL_JOIN = 63
    CHANNEL_JOIN_SUCCESS = 64
    CHANNEL_INFO = 65
    CHANNEL_KICK = 66
    CHANNEL_AUTO_JOIN = 67
    OSU_BEATMAP_INFO_REQUEST = 68
    BEATMAP_INFO_REPLY = 69
    OSU_MATCH_TRANSFER_HOST = 70
    PRIVILEGES = 71
    FRIENDS_LIST = 72
    OSU_FRIEND_ADD = 73
    OSU_FRIEND_REMOVE = 74
    PROTOCOL_VERSION = 75
    MAIN_MENU_ICON = 76
    OSU_MATCH_CHANGE_TEAM = 77
    OSU_CHANNEL_PART = 78
    OSU_RECEIVE_UPDATES = 79
    MONITOR = 80  # unused
    MATCH_PLAYER_SKIPPED = 81
    OSU_SET_AWAY_MESSAGE = 82
    USER_SESSION = 83
    OSU_IRC_ONLY = 84
    OSU_USER_STATS_REQUEST = 85
    RESTART = 86
    OSU_MATCH_INVITE = 87
    MATCH_INVITE = 88
    CHANNEL_INFO_END = 89
    OSU_MATCH_CHANGE_PASSWORD = 90
    MATCH_CHANGE_PASSWORD = 91
    SILENCE_END = 92
    OSU_TOURNAMENT_MATCH_INFO_REQUEST = 93
    USER_SILENCED = 94
    USER_SESSION_SINGLE = 95
    USER_SESSION_BUNDLE = 96
    OSU_USER_SESSION_REQUEST = 97
    OSU_USER_SESSION_REQUEST_ALL = 98
    OSU_TOGGLE_BLOCK_NON_FRIEND_DMS = 99
    USER_DM_BLOCKED = 100
    TARGET_IS_SILENCED = 101
    VERSION_UPDATE_FORCED = 102
    SWITCH_SERVER = 103
    ACCOUNT_RESTRICTED = 104
    RTX = 105  # unused
    MATCH_ABORT = 106
    SWITCH_TOURNAMENT_SERVER = 107
    OSU_TOURNAMENT_JOIN_MATCH_CHANNEL = 108
    OSU_TOURNAMENT_LEAVE_MATCH_CHANNEL = 109


def write_uleb128(num: int) -> bytes:
    if num == 0:
        return bytearray(b"\x00")

    ret = bytearray()
    length = 0

    while num > 0:
        ret.append(num & 0b01111111)
        num >>= 7
        if num != 0:
            ret[length] |= 0b10000000
        length += 1

    return bytes(ret)


def write_string(string: str) -> bytes:
    s = string.encode()
    return b"\x0b" + write_uleb128(len(s)) + s


def write_int(i: int) -> bytes:
    return struct.pack("<i", i)


def write_unsigned_int(i: int) -> bytes:
    return struct.pack("<I", i)


def write_float(f: float) -> bytes:
    return struct.pack("<f", f)


def write_byte(b: int) -> bytes:
    return struct.pack("<b", b)


def write_unsigned_byte(b: int) -> bytes:
    return struct.pack("<B", b)


def write_short(s: int) -> bytes:
    return struct.pack("<h", s)


def write_long_long(l: int) -> bytes:
    return struct.pack("<q", l)


def write_list32(l: tuple[int]) -> bytes:
    ret = bytearray(write_short(len(l)))

    for item in l:
        ret += write_int(item)

    return bytes(ret)


from enum import StrEnum


class PacketType(StrEnum):
    STRING = "str"
    INTEGER = "int"
    U_INT = "u_int"
    SHORT = "short"
    FLOAT = "float"
    LONG = "long"
    BYTE = "byte"
    U_BYTE = "u_byte"
    LIST_32 = "list_32"


def write(packet_id: int, *args) -> bytes:
    p = bytearray(struct.pack("<Hx", packet_id))

    for ctx, _type in args:
        if _type == PacketType.STRING:
            p += write_string(ctx)
        elif _type == PacketType.INTEGER:
            p += write_int(ctx)
        elif _type == PacketType.U_INT:
            p += write_unsigned_int(ctx)
        elif _type == PacketType.SHORT:
            p += write_short(ctx)
        elif _type == PacketType.FLOAT:
            p += write_float(ctx)
        elif _type == PacketType.LONG:
            p += write_long_long(ctx)
        elif _type == PacketType.BYTE:
            p += write_byte(ctx)
        elif _type == PacketType.U_BYTE:
            p += write_unsigned_byte(ctx)
        elif _type == PacketType.LIST_32:
            p += write_list32(ctx)
        else:
            p += struct.pack(f"<{_type}", ctx)

    p[3:3] = struct.pack("<I", len(p) - 3)
    return bytes(p)


def write_user_id(i: int) -> bytes:
    return write(
        ServerPackets.USER_ID,
        (i, f"{PacketType.U_INT if i > 0 else PacketType.INTEGER}"),
    )


def write_notification(msg: str) -> bytes:
    return write(ServerPackets.NOTIFICATION, (msg, PacketType.STRING))


def write_protocol_version(i: int = 19):
    return write(ServerPackets.PROTOCOL_VERSION, (i, PacketType.INTEGER))


# TODO implement "Player" typedict
def write_bancho_privs(**kwargs) -> bytes:
    return write(ServerPackets.PRIVILEGES,
                (kwargs["bancho_privs"], PacketType.INTEGER))


def write_user_stats(
    user_id: int,
    action: int,
    ranked_score: int,
    accuracy: float,
    play_count: int,
    total_score: int,
    global_rank: int,
    performance_points: int,
    info_text: str,
    beatmap_md5: str,
    mods: int,
    mode: int,
    beatmap_id: int,) -> bytes:
    return write(
        ServerPackets.USER_SESSION,
            (user_id, PacketType.INTEGER),
            (action, PacketType.U_INT),
            (ranked_score, PacketType.STRING),
            (info_text, PacketType.STRING),
            (beatmap_md5, PacketType.STRING),
            (mods, PacketType.INTEGER),
            (mode, PacketType.U_INT),
            (beatmap_id, PacketType.INTEGER),
            (bytes(0), PacketType.U_INT), #skip ranked_score
            ((accuracy / 100), PacketType.FLOAT),
            (play_count, PacketType.INTEGER),
            (total_score, PacketType.U_INT),
            (global_rank, PacketType.INTEGER),
            (performance_points, PacketType.INTEGER),
    )


def write_user_session(
        user_id: int,
        username: str,
        timezone: int,
        country: int,
        longitude: float,
        latitude: float,
        rank: int,
        gamemode: int,
) -> bytes:
    return write(
        ServerPackets.USER_STATS,
        (user_id, PacketType.INTEGER),
        (username, PacketType.STRING),
        ((timezone + 24), PacketType.U_INT),
        (country, PacketType.U_INT),
        ((0 & 0x1F) | ((gamemode & 0x7) << 5), PacketType.U_INT), # skip privileges packet
        (longitude, PacketType.FLOAT),
        (latitude, PacketType.FLOAT),
        (rank, PacketType.INTEGER),
    )


def write_menu_icon(menu_icon: tuple[str, str]) -> bytes:
    return write(ServerPackets.MAIN_MENU_ICON, ("|".join(menu_icon), PacketType.STRING))


def write_friends_list(*friends: int) -> bytes:
    return write(ServerPackets.FRIENDS_LIST, (friends, PacketType.LIST_32))


def write_channel_info_end() -> bytes:
    return write(ServerPackets.CHANNEL_INFO_END)


def write_channelJoin(channel_name: str) -> bytes:
    return write(ServerPackets.CHANNEL_JOIN_SUCCESS, (channel_name, PacketType.STRING))


def write_channel_info(
    channel_name: str, channel_description: str, channel_player_count: int
) -> bytes:
    return write(
        ServerPackets.CHANNEL_INFO,
        (channel_name, PacketType.STRING),
        (channel_description, PacketType.STRING),
        (channel_player_count, PacketType.SHORT),
    )


def write_system_restart(ms: int = 0) -> bytes:
    return write(ServerPackets.RESTART, (ms, PacketType.INTEGER))


def write_login(user_id: int) -> bytes:
    return write(
        ServerPackets.USER_ID,
        (PacketType.INTEGER, user_id)
    )


from uuid import UUID
def write_logout(uuid: UUID) -> bytes:
    return write(
        ServerPackets.USER_LOGOUT, (uuid, PacketType.INTEGER), (0, PacketType.U_BYTE)
    )


def write_send_message(client: str, msg: str, target: str, user_id: int):
    return write(
        ServerPackets.SEND_MESSAGE,
        (client, PacketType.STRING),
        (msg, PacketType.STRING),
        (target, PacketType.STRING),
        (user_id, PacketType.INTEGER),
    )


def write_user_silenced(user_id: int) -> bytes:
    return write(ServerPackets.USER_SILENCED, (user_id, PacketType.INTEGER))
