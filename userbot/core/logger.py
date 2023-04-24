# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

"""
import logging
import sys

logging.basicConfig(
    format="[%(levelname)s - %(asctime)s] - %(name)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("catub.log", mode="w"),
        logging.StreamHandler(sys.stdout)
    ]
)
"""
import logging

logging.basicConfig(
    format="[%(levelname)s - %(asctime)s] - %(name)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("catub.log")
    ],
    datefmt="%H:%M:%S"
)