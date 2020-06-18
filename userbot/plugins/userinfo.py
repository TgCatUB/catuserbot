# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for getting info
    about any user on Telegram(including you!). """

from telethon.events import NewMessage
from typing import Union

from userbot import CMD_HELP
from userbot.events import register

from re import findall, match
from typing import List

from telethon.events import NewMessage
from telethon.tl.custom import Message
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    MessageEntityMentionName,
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
    MessageEntityMention,
    InputPeerChannel,
    InputPeerChat)


def parse_arguments(message: str, valid: List[str]) -> (dict, str):
    options = {}

    # Handle boolean values
    for opt in findall(r'([.!]\S+)', message):
        if opt[1:] in valid:
            if opt[0] == '.':
                options[opt[1:]] = True
            elif opt[0] == '!':
                options[opt[1:]] = False
            message = message.replace(opt, '')

    # Handle key/value pairs
    for opt in findall(r'(\S+):(?:"([\S\s]+)"|(\S+))', message):
        key, val1, val2 = opt
        value = val2 or val1[1:-1]
        if key in valid:
            if value.isnumeric():
                value = int(value)
            elif match(r'[Tt]rue|[Ff]alse', value):
                match(r'[Tt]rue', value)
            options[key] = value
            message = message.replace(f"{key}:{value}", '')

    return options, message.strip()


def freeze(d):
    if isinstance(d, dict):
        return frozenset((key, freeze(value)) for key, value in d.items())
    elif isinstance(d, list):
        return tuple(freeze(value) for value in d)
    return d


def extract_urls(message):
    matches = findall(r'(https?://\S+)', str(message))
    return list(matches)


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None

    return user_obj


async def get_user_from_event(event: NewMessage.Event, **kwargs):
    """ Get the user from argument or replied message. """
    reply_msg: Message = await event.get_reply_message()
    user = kwargs.get('user', None)

    if user:
        # First check for a user id
        if user.isnumeric():
            user = int(user)

        # Then check for a user mention (@username)
        elif event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user

        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(
                GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            return None

    # Check for a forwarded message
    elif (reply_msg and
          reply_msg.forward and
          reply_msg.forward.sender_id and
          kwargs['forward']):
        forward = reply_msg.forward
        replied_user = await event.client(GetFullUserRequest(forward.sender_id))

    # Check for a replied to message
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(previous_message.from_id))

    # Last case scenario is to get the current user
    else:
        self_user = await event.client.get_me()
        replied_user = await event.client(GetFullUserRequest(self_user.id))

    return replied_user


async def get_chat_from_event(event: NewMessage.Event, **kwargs):
    reply_msg: Message = await event.get_reply_message()
    chat = kwargs.get('chat', None)

    if chat:
        try:
            input_entity = await event.client.get_input_entity(chat)
            if isinstance(input_entity, InputPeerChannel):
                return await event.client(GetFullChannelRequest(input_entity.channel_id))
            elif isinstance(input_entity, InputPeerChat):
                return await event.client(GetFullChatRequest(input_entity.chat_id))
            else:
                return None
        except(TypeError, ValueError):
            return None
    # elif reply_msg and reply_msg.forward:
    #     return None
    else:
        chat = await event.get_chat()
        return await event.client(GetFullChannelRequest(chat.id))


async def list_admins(event):
    adms = await event.client.get_participants(event.chat, filter=ChannelParticipantsAdmins)
    adms = map(lambda x: x if not x.bot else None, adms)
    adms = [i for i in list(adms) if i]
    return adms


async def list_bots(event):
    bots = await event.client.get_participants(event.chat, filter=ChannelParticipantsBots)
    return bots


def make_mention(user):
    if user.username:
        return f"@{user.username}"
    else:
        return inline_mention(user)


def inline_mention(user):
    full_name = user_full_name(user) or "No Name"
    return f"[{full_name}](tg://user?id={user.id})"


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    full_name = ' '.join(names)
    return full_name


class FormattedBase:
    text: str

    def __add__(self, other: Union[str, 'FormattedBase']) -> str:
        return str(self) + str(other)

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.text})'

    def __str__(self) -> str:
        return self.text


class String(FormattedBase):

    def __init__(self, text: Union[str, int]) -> None:
        self.text = str(text)


class Bold(FormattedBase):

    def __init__(self, text: Union[str, int]) -> None:
        self.text = f'**{text}**'


class Italic(FormattedBase):

    def __init__(self, text: Union[str, int]) -> None:
        self.text = f'__{text}__'


class Code(FormattedBase):

    def __init__(self, text: Union[str, int]) -> None:
        self.text = f'`{text}`'


class Pre(FormattedBase):

    def __init__(self, text: Union[str, int]) -> None:
        self.text = f'```{text}```'


class Link(FormattedBase):

    def __init__(self, label: String, url: str) -> None:
        self.text = f'[{label}]({url})'


class Mention(Link):

    def __init__(self, label: String, uid: int):
        super().__init__(label, f'tg://user?id={uid}')


class KeyValueItem(FormattedBase):

    def __init__(self, key: Union[str, FormattedBase],
                 value: Union[str, FormattedBase]) -> None:
        self.key = key
        self.value = value
        self.text = f'{key}: {value}'


class Item(FormattedBase):

    def __init__(self, text: Union[str, int]) -> None:
        self.text = str(text)


class Section:

    def __init__(self,
                 *args: Union[String,
                              'FormattedBase'],
                 spacing: int = 1,
                 indent: int = 4) -> None:
        self.header = args[0]
        self.items = list(args[1:])
        self.indent = indent
        self.spacing = spacing

    def __add__(self, other: Union[String, 'FormattedBase']) -> str:
        return str(self) + '\n\n' + str(other)

    def __str__(self) -> str:
        return ('\n' *
                self.spacing).join([str(self.header)] +
                                   [' ' *
                                    self.indent +
                                    str(item) for item in self.items if item is not None])


class SubSection(Section):

    def __init__(self,
                 *args: Union[String,
                              'SubSubSection'],
                 indent: int = 8) -> None:
        super().__init__(*args, indent=indent)


class SubSubSection(SubSection):

    def __init__(self, *args: String, indent: int = 12) -> None:
        super().__init__(*args, indent=indent)


class TGDoc:

    def __init__(self, *args: Union[String, 'Section']) -> None:
        self.sections = args

    def __str__(self) -> str:
        return '\n\n'.join([str(section) for section in self.sections])



@register(pattern=r"^\.u(?:ser)?(\s+[\S\s]+|$)", outgoing=True)
async def who(event: NewMessage.Event):
    """ For .user command, get info about a user. """
    if event.fwd_from:
        return

    args, user = parse_arguments(event.pattern_match.group(1), [
        'id', 'forward', 'general', 'bot', 'misc', 'all', 'mention'
    ])

    args['forward'] = args.get('forward', True)
    args['user'] = user

    replied_user = await get_user_from_event(event, **args)

    if not replied_user:
        await event.edit("**Failed to get information for user**")
        return

    user_info = await fetch_info(replied_user, **args)

    message_id_to_reply = event.message.reply_to_msg_id

    if not message_id_to_reply:
        pass

    await event.edit(str(user_info), parse_mode="markdown")


async def fetch_info(replied_user, **kwargs):
    """ Get details from the User object. """
    user = replied_user.user

    id_only = kwargs.get('id', False)
    show_general = kwargs.get('general', True)
    show_bot = kwargs.get('bot', False)
    show_misc = kwargs.get('misc', False)
    show_all = kwargs.get('all', False)
    mention_name = kwargs.get('mention', False)

    if show_all:
        show_general = True
        show_bot = True
        show_misc = True

    full_name = str(user.first_name + ' ' + (user.last_name or ''))

    if mention_name:
        title = Link(full_name, f'tg://user?id={user.id}')
    else:
        title = Bold(full_name)

    if id_only:
        return KeyValueItem(title, Code(user.id))

    general = SubSection(
        Bold('general'), KeyValueItem(
            'id', Code(
                user.id)), KeyValueItem(
            'first_name', Code(
                user.first_name)), KeyValueItem(
            'last_name', Code(
                user.last_name)), KeyValueItem(
            'username', Code(
                user.username)), KeyValueItem(
            'mutual_contact', Code(
                user.mutual_contact)), KeyValueItem(
            'common groups', Code(
                replied_user.common_chats_count)))

    bot = SubSection(Bold('bot'),
                     KeyValueItem('bot', Code(user.bot)),
                     KeyValueItem('bot_chat_history', Code(user.bot_chat_history)),
                     KeyValueItem('bot_info_version', Code(user.bot_info_version)),
                     KeyValueItem('bot_inline_geo', Code(user.bot_inline_geo)),
                     KeyValueItem('bot_inline_placeholder',
                                  Code(user.bot_inline_placeholder)),
                     KeyValueItem('bot_nochats', Code(user.bot_nochats)))

    misc = SubSection(
        Bold('misc'), KeyValueItem(
            'restricted', Code(
                user.restricted)), KeyValueItem(
            'restriction_reason', Code(
                user.restriction_reason)), KeyValueItem(
            'deleted', Code(
                user.deleted)), KeyValueItem(
            'verified', Code(
                user.verified)), KeyValueItem(
            'min', Code(
                user.min)), KeyValueItem(
            'lang_code', Code(
                user.lang_code)))

    return Section(title,
                   general if show_general else None,
                   misc if show_misc else None,
                   bot if show_bot else None)



CMD_HELP.update({
    "android":
    "`.u(ser) [options] (username|id)`" 

    "Or, in response to a message"
    "`.u(ser) [options]`"

    "Options:"
    "`.id`: Show only the user's ID"
    "`.general`: Show general user info"
    "`.bot`: Show bot related info"
    "`.misc`: Show miscelanious info"
    "`.all`: Show all info (overrides other options)"
    "`.mention`: Inline mention the user" 
    "`.forward`: Follow forwarded message"
})
