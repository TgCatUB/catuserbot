#    Haruka Aya (A telegram bot project)
#    Copyright (C) 2017-2019 Paul Larsen
#    Copyright (C) 2019-2020 Akito Mizukito (Haruka Network Development)

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import html
from typing import List

from telegram import Update, Bot
from telegram import ParseMode
from telegram.error import BadRequest
from telegram.ext import CommandHandler, Filters
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import mention_html, escape_markdown

from haruka import dispatcher
from haruka.modules.disable import DisableAbleCommandHandler
from haruka.modules.helper_funcs.chat_status import bot_admin, user_admin, can_pin
from haruka.modules.helper_funcs.extraction import extract_user
from haruka.modules.log_channel import loggable
from haruka.modules.sql import admin_sql as sql
from haruka.modules.tr_engine.strings import tld

from haruka.modules.connection import connected


@run_async
@bot_admin
@user_admin
@loggable
def promote(bot: Bot, update: Update, args: List[str]) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    conn = connected(bot, update, chat, user.id)
    if conn:
        chatD = dispatcher.bot.getChat(conn)
    else:
        chatD = update.effective_chat
        if chat.type == "private":
            return

    if not chatD.get_member(bot.id).can_promote_members:
        update.effective_message.reply_text(tld(chat.id, "admin_err_no_perm"))
        return

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(tld(chat.id, "common_err_no_user"))
        return

    user_member = chatD.get_member(user_id)
    if user_member.status == 'administrator' or user_member.status == 'creator':
        message.reply_text(tld(chat.id, "admin_err_user_admin"))
        return

    if user_id == bot.id:
        message.reply_text(tld(chat.id, "admin_err_self_promote"))
        return

    # set same perms as bot - bot can't assign higher perms than itself!
    bot_member = chatD.get_member(bot.id)

    bot.promoteChatMember(chatD.id,
                          user_id,
                          can_change_info=bot_member.can_change_info,
                          can_post_messages=bot_member.can_post_messages,
                          can_edit_messages=bot_member.can_edit_messages,
                          can_delete_messages=bot_member.can_delete_messages,
                          can_invite_users=bot_member.can_invite_users,
                          can_restrict_members=bot_member.can_restrict_members,
                          can_pin_messages=bot_member.can_pin_messages,
                          can_promote_members=bot_member.can_promote_members)

    message.reply_text(tld(chat.id, "admin_promote_success").format(
        mention_html(user.id, user.first_name),
        mention_html(user_member.user.id, user_member.user.first_name),
        html.escape(chatD.title)),
                       parse_mode=ParseMode.HTML)
    return f"<b>{html.escape(chatD.title)}:</b>" \
            "\n#PROMOTED" \
           f"\n<b>Admin:</b> {mention_html(user.id, user.first_name)}" \
           f"\n<b>User:</b> {mention_html(user_member.user.id, user_member.user.first_name)}"


@run_async
@bot_admin
@user_admin
@loggable
def demote(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user
    conn = connected(bot, update, chat, user.id)
    if conn:
        chatD = dispatcher.bot.getChat(conn)
    else:
        chatD = update.effective_chat
        if chat.type == "private":
            return

    if not chatD.get_member(bot.id).can_promote_members:
        update.effective_message.reply_text(tld(chat.id, "admin_err_no_perm"))
        return

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(tld(chat.id, "common_err_no_user"))
        return ""

    user_member = chatD.get_member(user_id)
    if user_member.status == 'creator':
        message.reply_text(tld(chat.id, "admin_err_demote_creator"))
        return ""

    if not user_member.status == 'administrator':
        message.reply_text(tld(chat.id, "admin_err_demote_noadmin"))
        return ""

    if user_id == bot.id:
        message.reply_text(tld(chat.id, "admin_err_self_demote"))
        return ""

    try:
        bot.promoteChatMember(int(chatD.id),
                              int(user_id),
                              can_change_info=False,
                              can_post_messages=False,
                              can_edit_messages=False,
                              can_delete_messages=False,
                              can_invite_users=False,
                              can_restrict_members=False,
                              can_pin_messages=False,
                              can_promote_members=False)
        message.reply_text(tld(chat.id, "admin_demote_success").format(
            mention_html(user.id, user.first_name),
            mention_html(user_member.user.id, user_member.user.first_name),
            html.escape(chatD.title)),
                           parse_mode=ParseMode.HTML)
        return f"<b>{html.escape(chatD.title)}:</b>" \
                "\n#DEMOTED" \
               f"\n<b>Admin:</b> {mention_html(user.id, user.first_name)}" \
               f"\n<b>User:</b> {mention_html(user_member.user.id, user_member.user.first_name)}"

    except BadRequest:
        message.reply_text(tld(chat.id, "admin_err_cant_demote"))
        return ""


@run_async
@bot_admin
@can_pin
@user_admin
@loggable
def pin(bot: Bot, update: Update, args: List[str]) -> str:
    user = update.effective_user
    chat = update.effective_chat

    is_group = chat.type != "private" and chat.type != "channel"

    prev_message = update.effective_message.reply_to_message

    is_silent = True
    if len(args) >= 1:
        is_silent = not (args[0].lower() == 'notify'
                         or args[0].lower() == 'loud'
                         or args[0].lower() == 'violent')

    if prev_message and is_group:
        try:
            bot.pinChatMessage(chat.id,
                               prev_message.message_id,
                               disable_notification=is_silent)
        except BadRequest as excp:
            if excp.message == "Chat_not_modified":
                pass
            else:
                raise
        return f"<b>{html.escape(chat.title)}:</b>" \
                "\n#PINNED" \
               f"\n<b>Admin:</b> {mention_html(user.id, user.first_name)}"

    return ""


@run_async
@bot_admin
@can_pin
@user_admin
@loggable
def unpin(bot: Bot, update: Update) -> str:
    chat = update.effective_chat
    user = update.effective_user

    try:
        bot.unpinChatMessage(chat.id)
    except BadRequest as excp:
        if excp.message == "Chat_not_modified":
            pass
        else:
            raise

    return f"<b>{html.escape(chat.title)}:</b>" \
           "\n#UNPINNED" \
           f"\n<b>Admin:</b> {mention_html(user.id, user.first_name)}"


@run_async
@bot_admin
@user_admin
def invite(bot: Bot, update: Update):
    chat = update.effective_chat
    user = update.effective_user
    conn = connected(bot, update, chat, user.id, need_admin=False)
    if conn:
        chatP = dispatcher.bot.getChat(conn)
    else:
        chatP = update.effective_chat
        if chat.type == "private":
            return

    if chatP.username:
        update.effective_message.reply_text(chatP.username)
    elif chatP.type == chatP.SUPERGROUP or chatP.type == chatP.CHANNEL:
        bot_member = chatP.get_member(bot.id)
        if bot_member.can_invite_users:
            invitelink = chatP.invite_link
            #print(invitelink)
            if not invitelink:
                invitelink = bot.exportChatInviteLink(chatP.id)

            update.effective_message.reply_text(invitelink)
        else:
            update.effective_message.reply_text(
                tld(chat.id, "admin_err_no_perm_invitelink"))
    else:
        update.effective_message.reply_text(
            tld(chat.id, "admin_chat_no_invitelink"))


@run_async
def adminlist(bot: Bot, update: Update):
    chat = update.effective_chat
    administrators = update.effective_chat.get_administrators()
    text = tld(chat.id, "admin_list").format(
        update.effective_chat.title
        or tld(chat.id, "common_this_chat").lower())
    for admin in administrators:
        user = admin.user
        name = "[{}](tg://user?id={})".format(user.first_name, user.id)
        if user.username:
            esc = escape_markdown("@" + user.username)
            name = "[{}](tg://user?id={})".format(esc, user.id)
        text += "\n - {}".format(name)

    update.effective_message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


# TODO: Finalize this command, add automatic message deleting
@user_admin
@run_async
def reaction(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat
    if len(args) >= 1:
        var = args[0]
        print(var)
        if var == "False":
            sql.set_command_reaction(chat.id, False)
            update.effective_message.reply_text(
                tld(chat.id, "admin_disable_reaction"))
        elif var == "True":
            sql.set_command_reaction(chat.id, True)
            update.effective_message.reply_text(
                tld(chat.id, "admin_enable_reaction"))
        else:
            update.effective_message.reply_text(tld(chat.id,
                                                    "admin_err_wrong_arg"),
                                                parse_mode=ParseMode.MARKDOWN)
    else:
        status = sql.command_reaction(chat.id)
        update.effective_message.reply_text(tld(
            chat.id, "admin_reaction_status").format('enabled' if status ==
                                                     True else 'disabled'),
                                            parse_mode=ParseMode.MARKDOWN)


__help__ = True

PIN_HANDLER = DisableAbleCommandHandler("pin",
                                        pin,
                                        pass_args=True,
                                        filters=Filters.group)
UNPIN_HANDLER = DisableAbleCommandHandler("unpin",
                                          unpin,
                                          filters=Filters.group)

INVITE_HANDLER = CommandHandler("invitelink", invite)

PROMOTE_HANDLER = DisableAbleCommandHandler("promote", promote, pass_args=True)
DEMOTE_HANDLER = DisableAbleCommandHandler("demote", demote, pass_args=True)

REACT_HANDLER = DisableAbleCommandHandler("reaction",
                                          reaction,
                                          pass_args=True,
                                          filters=Filters.group)

ADMINLIST_HANDLER = DisableAbleCommandHandler(["adminlist", "admins"],
                                              adminlist)

dispatcher.add_handler(PIN_HANDLER)
dispatcher.add_handler(UNPIN_HANDLER)
dispatcher.add_handler(INVITE_HANDLER)
dispatcher.add_handler(PROMOTE_HANDLER)
dispatcher.add_handler(DEMOTE_HANDLER)
dispatcher.add_handler(ADMINLIST_HANDLER)
dispatcher.add_handler(REACT_HANDLER)
