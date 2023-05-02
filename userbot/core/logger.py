# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import logging


class IgnoreSpecificMessageFilter(logging.Filter):
    def filter(self, record):
        return "Got difference for" not in record.getMessage()


logging.basicConfig(
    format="[%(levelname)s- %(asctime)s]- %(name)s- %(message)s",
    handlers=[logging.FileHandler("catub.log"), logging.StreamHandler()],
    level=logging.INFO,
    datefmt="%H:%M:%S",
    filters=[IgnoreSpecificMessageFilter()],
)
