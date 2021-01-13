#!/usr/bin/env python3
# (c) https://t.me/TelethonChat/37677
# This Source Code Form is subject to the terms of the GNU
# General Public License, v.3.0. If a copy of the GPL was not distributed with this
# file, You can obtain one at https://www.gnu.org/licenses/gpl-3.0.en.html.

from telethon.sessions import StringSession
from telethon.sync import TelegramClient

print("""
Goto - my.telegram.org
Login Using Your Telegram Account
Get The AppId And AppHash !""")

APP_ID = int(input("Enter APP ID here: "))
API_HASH = input("Enter API HASH here: ")

with TelegramClient(StringSession(), APP_ID, API_HASH) as client:
    print('The Following Is The Session String\nKeep It Safe !\n\n')
    print(client.session.save())
    print('\n\n')
    client.send_message("me", client.session.save())
