import struct
from enum import IntEnum


class ServerPackets(IntEnum):
    OSU_CHANGE_ACTION = 0
    OSU_SEND_PUBLIC_MESSAGE = 1
    OSU_LOGOUT = 2
    OSU_REQUEST_STATUS_UPDATE = 3
    OSU_PING = 4
    CHO_USER_ID = 5
    CHO_SEND_MESSAGE = 7
    CHO_PONG = 8
    CHO_HANDLE_IRC_CHANGE_USERNAME = 9
    CHO_HANDLE_IRC_QUIT = 10
    CHO_USER_STATS = 11
    CHO_USER_LOGOUT = 12
    CHO_SPECTATOR_JOINED = 13
    CHO_SPECTATOR_LEFT = 14
    CHO_SPECTATE_FRAMES = 15
    OSU_START_SPECTATING = 16
    OSU_STOP_SPECTATING = 17
    OSU_SPECTATE_FRAMES = 18
    CHO_VERSION_UPDATE = 19
    OSU_ERROR_REPORT = 20
    OSU_CANT_SPECTATE = 21
    CHO_SPECTATOR_CANT_SPECTATE = 22
    CHO_GET_ATTENTION = 23
    CHO_NOTIFICATION = 24
    OSU_SEND_PRIVATE_MESSAGE = 25
    CHO_UPDATE_MATCH = 26
    CHO_NEW_MATCH = 27
    CHO_DISPOSE_MATCH = 28
    OSU_PART_LOBBY = 29
    OSU_JOIN_LOBBY = 30
    OSU_CREATE_MATCH = 31
    OSU_JOIN_MATCH = 32
    OSU_PART_MATCH = 33
    CHO_TOGGLE_BLOCK_NON_FRIEND_DMS = 34
    CHO_MATCH_JOIN_SUCCESS = 36
    CHO_MATCH_JOIN_FAIL = 37
    OSU_MATCH_CHANGE_SLOT = 38
    OSU_MATCH_READY = 39
    OSU_MATCH_LOCK = 40
    OSU_MATCH_CHANGE_SETTINGS = 41
    CHO_FELLOW_SPECTATOR_JOINED = 42
    CHO_FELLOW_SPECTATOR_LEFT = 43
    OSU_MATCH_START = 44
    CHO_ALL_PLAYERS_LOADED = 45
    CHO_MATCH_START = 46
    OSU_MATCH_SCORE_UPDATE = 47
    CHO_MATCH_SCORE_UPDATE = 48
    OSU_MATCH_COMPLETE = 49
    CHO_MATCH_TRANSFER_HOST = 50
    OSU_MATCH_CHANGE_MODS = 51
    OSU_MATCH_LOAD_COMPLETE = 52
    CHO_MATCH_ALL_PLAYERS_LOADED = 53
    OSU_MATCH_NO_BEATMAP = 54
    OSU_MATCH_NOT_READY = 55
    OSU_MATCH_FAILED = 56
    CHO_MATCH_PLAYER_FAILED = 57
    CHO_MATCH_COMPLETE = 58
    OSU_MATCH_HAS_BEATMAP = 59
    OSU_MATCH_SKIP_REQUEST = 60
    CHO_MATCH_SKIP = 61
    CHO_UNAUTHORIZED = 62  # unused
    OSU_CHANNEL_JOIN = 63
    CHO_CHANNEL_JOIN_SUCCESS = 64
    CHO_CHANNEL_INFO = 65
    CHO_CHANNEL_KICK = 66
    CHO_CHANNEL_AUTO_JOIN = 67
    OSU_BEATMAP_INFO_REQUEST = 68
    CHO_BEATMAP_INFO_REPLY = 69
    OSU_MATCH_TRANSFER_HOST = 70
    CHO_PRIVILEGES = 71
    CHO_FRIENDS_LIST = 72
    OSU_FRIEND_ADD = 73
    OSU_FRIEND_REMOVE = 74
    CHO_PROTOCOL_VERSION = 75
    CHO_MAIN_MENU_ICON = 76
    OSU_MATCH_CHANGE_TEAM = 77
    OSU_CHANNEL_PART = 78
    OSU_RECEIVE_UPDATES = 79
    CHO_MONITOR = 80  # unused
    CHO_MATCH_PLAYER_SKIPPED = 81
    OSU_SET_AWAY_MESSAGE = 82
    CHO_USER_PRESENCE = 83
    OSU_IRC_ONLY = 84
    OSU_USER_STATS_REQUEST = 85
    CHO_RESTART = 86
    OSU_MATCH_INVITE = 87
    CHO_MATCH_INVITE = 88
    CHO_CHANNEL_INFO_END = 89
    OSU_MATCH_CHANGE_PASSWORD = 90
    CHO_MATCH_CHANGE_PASSWORD = 91
    CHO_SILENCE_END = 92
    OSU_TOURNAMENT_MATCH_INFO_REQUEST = 93
    CHO_USER_SILENCED = 94
    CHO_USER_PRESENCE_SINGLE = 95
    CHO_USER_PRESENCE_BUNDLE = 96
    OSU_USER_PRESENCE_REQUEST = 97
    OSU_USER_PRESENCE_REQUEST_ALL = 98
    OSU_TOGGLE_BLOCK_NON_FRIEND_DMS = 99
    CHO_USER_DM_BLOCKED = 100
    CHO_TARGET_IS_SILENCED = 101
    CHO_VERSION_UPDATE_FORCED = 102
    CHO_SWITCH_SERVER = 103
    CHO_ACCOUNT_RESTRICTED = 104
    CHO_RTX = 105  # unused
    CHO_MATCH_ABORT = 106
    CHO_SWITCH_TOURNAMENT_SERVER = 107
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
        ServerPackets.CHO_USER_ID,
        (i, f"{PacketType.U_INT if i > 0 else PacketType.INTEGER}"),
    )


def write_notification(msg: str) -> bytes:
    return write(ServerPackets.CHO_NOTIFICATION, (msg, PacketType.STRING))


def write_protocol_version(i: int = 19):
    return write(ServerPackets.CHO_PROTOCOL_VERSION, (i, PacketType.INTEGER))


# TODO implement "Player" typedict
def write_bancho_orivs(**kwargs) -> bytes:
    return write(ServerPackets.CHO_PRIVILEGES,
                (kwargs["bancho_privs"], PacketType.INTEGER))


def write_user_presence(**kwargs) -> bytes:
    return write(
        ServerPackets.CHO_USER_PRESENCE,
        (kwargs["userid"], PacketType.INTEGER),
        (kwargs["name"], PacketType.STRING),
        (kwargs["utc_offset"] + 24, PacketType.U_BYTE),
        (kwargs["country"], PacketType.U_BYTE),
        (kwargs["bancho_privs"] | kwargs["mode"] << 5, PacketType.U_BYTE),
        (kwargs["location"][0], PacketType.FLOAT),
        (kwargs["location"][1], PacketType.FLOAT),
        (kwargs["rank"], PacketType.INTEGER),
    )


def write_user_stats(**kwargs) -> bytes:
    return write(
        ServerPackets.CHO_USER_STATS,
        (kwargs["userid"], PacketType.INTEGER),
        (kwargs["action"], PacketType.BYTE),
        (kwargs["info_text"], PacketType.STRING),
        (kwargs["map_md5"], PacketType.STRING),
        (kwargs["mods"], PacketType.INTEGER),
        (kwargs["mode"], PacketType.U_BYTE),
        (kwargs["map_id"], PacketType.INTEGER),
        (kwargs["ranked_score"], PacketType.LONG),
        (kwargs["acc"] / 100.0, PacketType.FLOAT),
        (kwargs["playcount"], PacketType.INTEGER),
        (kwargs["total_score"], PacketType.LONG),
        (kwargs["rank"], PacketType.INTEGER),
        (kwargs["pp"], PacketType.SHORT),
    )


def write_menu_icon(menu_icon: tuple[str, str]) -> bytes:
    return write(ServerPackets.CHO_MAIN_MENU_ICON, ("|".join(menu_icon), PacketType.STRING))


def write_friends_list(*friends: int) -> bytes:
    return write(ServerPackets.CHO_FRIENDS_LIST, (friends, PacketType.LIST_32))


def write_channel_info_end() -> bytes:
    return write(ServerPackets.CHO_CHANNEL_INFO_END)


def write_channelJoin(channel_name: str) -> bytes:
    return write(ServerPackets.CHO_CHANNEL_JOIN_SUCCESS, (channel_name, PacketType.STRING))


def write_channel_info(
    channel_name: str, channel_description: str, channel_player_count: int
) -> bytes:
    return write(
        ServerPackets.CHO_CHANNEL_INFO,
        (channel_name, PacketType.STRING),
        (channel_description, PacketType.STRING),
        (channel_player_count, PacketType.SHORT),
    )


def write_system_restart(ms: int = 0) -> bytes:
    return write(ServerPackets.CHO_RESTART, (ms, PacketType.INTEGER))


def write_login(user_id: int) -> bytes:
    return write(
        ServerPackets.CHO_USER_ID,
        (PacketType.INTEGER, user_id)
    )


from uuid import UUID
def write_logout(uuid: UUID) -> bytes:
    return write(
        ServerPackets.CHO_USER_LOGOUT, (uuid, PacketType.INTEGER), (0, PacketType.U_BYTE)
    )


def write_send_message(client: str, msg: str, target: str, userid: int):
    return write(
        ServerPackets.CHO_SEND_MESSAGE,
        (client, PacketType.STRING),
        (msg, PacketType.STRING),
        (target, PacketType.STRING),
        (userid, PacketType.INTEGER),
    )


def write_user_silenced(userid: int) -> bytes:
    return write(ServerPackets.CHO_USER_SILENCED, (userid, PacketType.INTEGER))
