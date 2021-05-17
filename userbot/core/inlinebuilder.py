import hashlib

from telethon import functions, types, utils


class InlineBuilder:
    def __init__(self, client):
        self._client = client

    async def cat_article(
        self,
        title,
        description=None,
        file=None,
        *,
        url=None,
        thumb=None,
        content=None,
        id=None,
        text=None,
        parse_mode=(),
        link_preview=True,
        include_media=True,
        geo=None,
        period=60,
        contact=None,
        game=False,
        buttons=None
    ):
        if file is not None:
            try:
                utils.get_input_photo(file)
            except TypeError:
                _, media, _ = await self._client._file_to_media(
                    file, allow_cache=True, as_image=True
                )
                if isinstance(media, types.InputPhoto):
                    pass
                else:
                    r = await self._client(
                        functions.messages.UploadMediaRequest(
                            types.InputPeerSelf(), media=media
                        )
                    )
                    utils.get_input_photo(r.photo)
        if file is not None:
            send_message = await self._message(
                text=text or "",
                parse_mode=parse_mode,
                link_preview=link_preview,
                media=include_media,
                geo=geo,
                period=period,
                contact=contact,
                game=game,
                buttons=buttons,
            )
        else:
            send_message = (
                await self._message(
                    text=text,
                    parse_mode=parse_mode,
                    link_preview=link_preview,
                    geo=geo,
                    period=period,
                    contact=contact,
                    game=game,
                    buttons=buttons,
                ),
            )
        result = types.InputBotInlineResult(
            id=id or "",
            type="article",
            send_message=send_message,
            title=title,
            description=description,
            url=url,
            thumb=thumb,
            content=content,
        )
        if id is None:
            result.id = hashlib.sha256(bytes(result)).hexdigest()
        return result

    async def _message(
        self,
        *,
        text=None,
        parse_mode=(),
        link_preview=True,
        media=False,
        geo=None,
        period=60,
        contact=None,
        game=False,
        buttons=None
    ):
        # Empty strings are valid but false-y; if they're empty use dummy '\0'
        args = ("\0" if text == "" else text, geo, contact, game)
        if sum(x is not None and x is not False for x in args) != 1:
            raise ValueError(
                "Must set exactly one of text, geo, contact or game (set {})".format(
                    ", ".join(
                        x[0] for x in zip("text geo contact game".split(), args) if x[1]
                    )
                    or "none"
                )
            )

        markup = self._client.build_reply_markup(buttons, inline_only=True)
        if text is not None:
            text, msg_entities = await self._client._parse_message_text(
                text, parse_mode
            )
            if media:
                return types.InputBotInlineMessageMediaAuto(
                    message=text, entities=msg_entities, reply_markup=markup
                )
            else:
                return types.InputBotInlineMessageText(
                    message=text,
                    no_webpage=not link_preview,
                    entities=msg_entities,
                    reply_markup=markup,
                )
        elif isinstance(geo, (types.InputGeoPoint, types.GeoPoint)):
            return types.InputBotInlineMessageMediaGeo(
                geo_point=utils.get_input_geo(geo), period=period, reply_markup=markup
            )
        elif isinstance(geo, (types.InputMediaVenue, types.MessageMediaVenue)):
            if isinstance(geo, types.InputMediaVenue):
                geo_point = geo.geo_point
            else:
                geo_point = geo.geo

            return types.InputBotInlineMessageMediaVenue(
                geo_point=geo_point,
                title=geo.title,
                address=geo.address,
                provider=geo.provider,
                venue_id=geo.venue_id,
                venue_type=geo.venue_type,
                reply_markup=markup,
            )
        elif isinstance(contact, (types.InputMediaContact, types.MessageMediaContact)):
            return types.InputBotInlineMessageMediaContact(
                phone_number=contact.phone_number,
                first_name=contact.first_name,
                last_name=contact.last_name,
                vcard=contact.vcard,
                reply_markup=markup,
            )
        elif game:
            return types.InputBotInlineMessageGame(reply_markup=markup)
        else:
            raise ValueError("No text, game or valid geo or contact given")
