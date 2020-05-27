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

from haruka import LOAD, NO_LOAD, LOGGER


def __list_all_modules():
    from os.path import dirname, basename, isfile
    import glob
    # This generates a list of modules in this folder for the * in __main__ to work.
    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_modules = [
        basename(f)[:-3] for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith('__init__.py')
    ]

    if LOAD or NO_LOAD:
        to_load = LOAD
        if to_load:
            if not all(
                    any(mod == module_name for module_name in all_modules)
                    for mod in to_load):
                LOGGER.error("Invalid load order names. Quitting.")
                quit(1)

        else:
            to_load = all_modules

        if NO_LOAD:
            LOGGER.info("Not loading: {}".format(NO_LOAD))
            return [item for item in to_load if item not in NO_LOAD]

        return to_load

    return all_modules


ALL_MODULES = sorted(__list_all_modules())
LOGGER.info("Modules to load: %s", str(ALL_MODULES))
__all__ = ALL_MODULES + ["ALL_MODULES"]
