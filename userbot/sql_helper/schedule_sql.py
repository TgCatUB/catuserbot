# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import contextlib
from datetime import datetime, timedelta

from sqlalchemy import JSON, Column, DateTime, Integer, String

from userbot import catub

from . import BASE, SESSION


class CatScheduler(BASE):
    __tablename__ = "catscheduler"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    recipient = Column(JSON)
    message = Column(JSON)
    scheduled_time = Column(DateTime)
    day_of_week = Column(String)

    def __repr__(self):
        return f"Message(id={self.id}, recipient='{self.recipient}', message='{self.message}', scheduled_time='{self.scheduled_time}', day_of_week='{self.day_of_week}')"


CatScheduler.__table__.create(checkfirst=True)


def add_message_to_database(recipient, message, scheduled_time, day_of_week=None):
    SESSION.add(
        CatScheduler(
            recipient=recipient,
            message=message,
            scheduled_time=scheduled_time,
            day_of_week=day_of_week,
        )
    )
    SESSION.commit()
    SESSION.close()


def get_messages_to_send():
    current_time = datetime.now().replace(second=0, microsecond=0)
    result = (
        SESSION.query(CatScheduler)
        .filter(CatScheduler.scheduled_time == current_time)
        .all()
    )
    SESSION.close()
    return result


def get_all_messages():
    messages = SESSION.query(CatScheduler).all()
    SESSION.close()
    return messages


def reassign_message(message):
    if message.day_of_week is None:
        SESSION.delete(message)
    else:
        new_schedule, _ = get_scdule_from_day(message.day_of_week)
        message.scheduled_time = new_schedule
        SESSION.merge(message)
    SESSION.commit()
    SESSION.close()


def delete_message_by_id(id):
    message = SESSION.query(CatScheduler).filter_by(id=id).first()
    out = f"There no task active with Id : `{id}`"
    if message:
        SESSION.delete(message)
        SESSION.commit()
        out = f"The task `{id}` deleted successfully"
    SESSION.close()
    return out


def delete_all_messages():
    SESSION.query(CatScheduler).delete()
    SESSION.commit()
    SESSION.close()


# //helper functions //


async def send_message(recipient, message):
    with contextlib.suppress(Exception):
        getmsg = await catub.get_messages(
            int(message["chat"]), ids=int(message["msg_id"])
        )
        await catub.send_message(int(recipient), getmsg)


async def send_scheduled_messages():
    messages = get_messages_to_send()
    for message in messages:
        recipients = message.recipient
        text = message.message
        for recipient in recipients:
            await send_message(recipient, text)
        reassign_message(message)


def get_scdule_from_day(daytime):
    try:
        day_of_week, time_of_day = daytime.split()
        time_of_day = datetime.strptime(time_of_day.strip(), "%H:%M").time()
        day_to_num = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 6,
        }

        day_num = day_to_num[day_of_week.lower()]
        current_datetime = datetime.now()
        current_day_num = current_datetime.weekday()

        if current_datetime.time() > time_of_day:
            days_until_scheduled_day = (day_num - current_day_num + 7) % 7
        else:
            days_until_scheduled_day = (day_num - current_day_num) % 7

        scheduled_day = current_datetime.replace(
            hour=time_of_day.hour, minute=time_of_day.minute, second=0, microsecond=0
        ) + timedelta(days=days_until_scheduled_day)

        if scheduled_day < current_datetime:
            scheduled_day += timedelta(days=7)
        return scheduled_day, None
    except Exception as error:
        return None, error
