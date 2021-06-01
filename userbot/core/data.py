from ..sql_helper.global_collectionjson import get_collection
from ..sql_helper.global_list import get_collection_list


def _sudousers_list():
    try:
        sudousers = get_collection("sudousers_list").json
    except AttributeError:
        sudousers = {}
    ulist = sudousers.keys()
    return [int(chat) for chat in ulist]


def _users_list():
    try:
        sudousers = get_collection("sudousers_list").json
    except AttributeError:
        sudousers = {}
    ulist = sudousers.keys()
    ulist = [int(chat) for chat in ulist]
    ulist.append("me")
    return list(ulist)


def blacklist_chats_list():
    try:
        blacklistchats = get_collection("blacklist_chats_list").json
    except AttributeError:
        blacklistchats = {}
    blacklist = blacklistchats.keys()
    return [int(chat) for chat in blacklist]


def sudo_enabled_cmds():
    listcmds = get_collection_list("sudo_enabled_cmds")
    return list(listcmds)
