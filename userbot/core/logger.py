# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


import sys
import logging

sys.stdout = open("catub.log", "a")
sys.stderr = sys.stdout

logging.basicConfig(
    format="[%(levelname)s- %(asctime)s]- %(name)s- %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    level=logging.INFO,
    datefmt="%H:%M:%S",
)
