#    X-tra-Telegram (userbot for telegram)
#    Copyright (C) 2019-2019 The Authors

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

from xtrabot import loader, utils
from xtrabot.xtrautil import Module

class LogMod(loader.Module):
    def __init__(self):
        self.name="log"
        super().__init__(self.log)

    async def log(self, event):
        rep = await utils.answer(event, "Fetching last log...", call="respond")
        with open("log.txt", "r") as file1:
            logs = file1.read()
        await utils.answer(rep, f"`{logs}`")

Module(LogMod)
