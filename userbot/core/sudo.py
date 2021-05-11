def _sudousers_list():
    from ..sql_helper.global_collection import get_item_collectionlist

    sudousers = get_item_collectionlist("sudousers")
    ulist = [user_d[0] for user_d in sudousers]
    return list(ulist)


def _users_list():
    from ..sql_helper.global_collection import get_item_collectionlist

    sudousers = get_item_collectionlist("sudousers")
    ulist = [user_d[0] for user_d in sudousers]
    ulist.append("me")
    return list(ulist)
