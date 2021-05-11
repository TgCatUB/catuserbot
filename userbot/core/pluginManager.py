import asyncio
import configparser
import dataclasses
import importlib
import inspect
import logging
import os
import os.path
import pathlib
import re
import shutil
import sys
import types
from typing import Dict, List, Tuple, Union

import requests
from telethon import TelegramClient, events

LOGGER = logging.getLogger(__name__)
package_patern = re.compile(r"([\w-]+)(?:=|<|>|!)")
github_patern = re.compile(r"(?:https?)?(?:www.)?(?:github.com/)?([\w\-.]+/[\w\-.]+)/?")
github_raw_pattern = re.compile(
    r"(?:https?)?(?:raw.)?(?:githubusercontent.com/)?([\w\-.]+/[\w\-.]+)/?"
)
trees_pattern = "https://api.github.com/repos/{}/git/trees/master"
raw_pattern = "https://raw.githubusercontent.com/{}/master/{}"
root = pathlib.Path(__file__).parent.parent.parent


@dataclasses.dataclass
class Callback:
    name: str
    callback: callable


@dataclasses.dataclass
class Plugin:
    name: str
    callbacks: List[Callback]
    path: str
    module: types.ModuleType


class SourcelessPluginLoader(importlib.abc.SourceLoader):
    """Loader for (byte) strings which don't have a source."""

    def __init__(self, name, data, path: str = "<string>"):
        self.data = data
        self.path = path
        self.name = name

    def get_code(self, path):
        """Return the code object if it exists."""
        source = self.get_source(path)
        if source is None:
            # There is no code object
            # (as would be the case, for example, for a built-in module)
            return None
        return compile(source, path, "exec", dont_inherit=True)

    def get_filename(self, fullname):
        """Return the origin (GitHub's raw URL)."""
        return self.path

    def get_data(self, path):
        """The data isn't stored locally, return the (bytes) string."""
        return self.data


class PluginManager:
    active_plugins: List[Plugin] = []
    inactive_plugins: List[Plugin] = []

    def __init__(self, client: TelegramClient):
        if "plugins" not in client.config:
            client.config["plugins"] = {}

        self.auth: Union[Tuple[str, str], bool] = None
        self.requirements: List[str] = run_async(get_pip_packages())
        self.new_requirements: List[str] = []
        self.require_restart: bool = False

        self.client: TelegramClient = client
        self.config = client.config["plugins"]
        self.plugin_path: pathlib.Path = pathlib.Path(
            self.config.setdefault("root", "./userbot/plugins")
        )

        self.include: list = _split_plugins(self.config.get("include", []))
        self.exclude: list = _split_plugins(self.config.get("exclude", []))
        access_token = self.config.get("token", None)
        user = self.config.get("user", None)
        if user and access_token:
            self.auth = (user, access_token)
        if not self.plugin_path.exists():
            LOGGER.error("Invalid plugins root! Exiting the script")
            sys.exit(1)

    def import_all(self) -> None:
        """Import all the (enabled) plugins and skip the rest."""
        importlib.invalidate_caches()
        to_import: Dict[str, Tuple[str, str, Union[bool, str]]] = {}

        for plugin_name, path in self._list_plugins():
            to_import[plugin_name] = (plugin_name, path, False)

        repo_plugins, repo_helpers = self._resolve_repo()
        for name, raw in repo_plugins.items():
            url, path = raw
            resp = requests.get(url, auth=self.auth)
            if not resp.ok:
                continue
            path = path[:-3].replace("\\", ".").replace("/", ".")
            if name in to_import:
                _, oldurl, _ = to_import[name]
                to_import.pop(name)
                LOGGER.debug(f"Overwrote {oldurl} with {url}")
            to_import.update({name: (path, url, resp.content)})

        for name, raw in repo_helpers.items():
            url, path = raw
            resp = requests.get(url, auth=self.auth)
            if not resp.ok:
                continue
            path = path[:-3].replace("\\", ".").replace("/", ".")
            self._import_helper(path, url, resp.content)

        if self.new_requirements:
            LOGGER.warning("Installing missing requirements.")
            run_async(install_pip_packages(self.new_requirements))
            self.client.reconnect = False
            restart_script()

        for _, info in to_import.items():
            name, path, content = info
            if (
                self.include
                and not self.exclude
                and plugin_name not in self.include
                or not self.include
                and self.exclude
                and plugin_name in self.exclude
            ):
                self.inactive_plugins.append(Plugin(plugin_name, [], path, None))
                LOGGER.debug("Skipped importing %s", plugin_name)
                continue
            self._import_plugin(name, path, content)

    def add_handlers(self) -> None:
        """Apply event handlers to all the found callbacks."""
        for plugin in self.active_plugins:
            for callback in plugin.callbacks:
                self.client.add_event_handler(callback.callback)
                LOGGER.debug("Added event handler for %s.", callback.callback.__name__)

    def remove_handlers(self) -> None:
        """Remove event handlers to all the found callbacks."""
        for plugin in self.active_plugins:
            for callback in plugin.callbacks:
                self.client.remove_event_handler(callback.callback)
                LOGGER.debug(
                    "Removed event handlers for %s.", callback.callback.__name__
                )

    def _list_plugins(self) -> List[Union[Tuple[str, str], None]]:
        """Get all the files from the local plugins dir."""
        LOGGER.info("Fetching all the local plugins.")
        plugins: List[Tuple[str, str]] = []
        if self.config.getboolean("enabled", True):
            for f in pathlib.Path(self.plugin_path).glob("**/*.py"):
                if (
                    f.name != "__init__.py"
                    and not f.name.startswith("_")
                    and f.name.endswith(".py")
                ):
                    name = f.name[:-3]
                    path = os.path.relpath(f)[:-3]
                    path = path.replace("\\", ".").replace("/", ".")
                    plugins.append((name, path))
        return plugins

    def _resolve_repo(self) -> Tuple[Dict[str, str], Dict[str, str]]:
        """Fetch all the files from a repository recusrively."""
        LOGGER.info("Fetching all the external plugins from git repos")
        plugins: Dict[str, str] = {}
        helpers: Dict[str, str] = {}
        repos: List[str] = []
        resources = root / "resources"
        rconfig_path = resources / "config.ini"
        tmp = self.config.get("repos", None)

        rconfig = configparser.ConfigParser()
        resources.mkdir(exist_ok=True)
        rconfig_path.touch()
        rconfig.read(rconfig_path)
        if "sha" not in rconfig:
            rconfig["sha"] = {}
        if "size" not in rconfig:
            rconfig["size"] = {}

        if tmp:
            tmp = _split_plugins(tmp)
            for url in tmp:
                match = github_patern.search(url)
                if match:
                    repos.append(match.group(1))
        for repo in repos:
            tree = requests.get(
                trees_pattern.format(repo), params={"recursive": "True"}, auth=self.auth
            )
            if not tree.ok:
                LOGGER.warning(f"Couldn't fetch plugins from {repo}")
                continue

            for f in tree.json().get("tree", ()):
                filen = f.get("path", "_")
                sha = f.get("sha", None)
                size = f.get("size", None)
                if not (filen and sha and size):
                    continue
                size = str(size)
                if filen == "requirements.txt":
                    try:
                        resp = requests.get(
                            raw_pattern.format(repo, filen), auth=self.auth, stream=True
                        )
                    except requests.exceptions.ConnectionError:
                        LOGGER.error(f"Failed to open {resp.url}, skipping {repo}")
                        break  # The plugins wouldn't load without the reqs
                    if resp.ok:
                        raw = resp.content.decode("utf-8")
                        req = run_async(get_pip_packages(raw))
                        self.new_requirements.extend(
                            [x for x in req if x not in self.requirements]
                        )
                    continue
                elif filen.startswith("resources/"):
                    rfilen = filen.rsplit("/", maxsplit=1)[1]
                    fsize = rconfig["size"].get(rfilen, None)
                    fsha = rconfig["sha"].get(rfilen, None)
                    if size == fsize and sha == fsha:
                        continue
                    url = raw_pattern.format(repo, filen)
                    LOGGER.info(f"Downloading resource {rfilen} from {repo}")
                    resp = requests.get(url, auth=self.auth, stream=True)
                    if resp.ok:
                        resp.raw.decode_content = True
                        newResource = resources / rfilen
                        with open(newResource, "wb") as f:
                            shutil.copyfileobj(resp.raw, f)
                        rconfig["size"][rfilen] = size
                        rconfig["sha"][rfilen] = sha
                    else:
                        LOGGER.warning(f"Failed to download {url}")
                    continue
                elif filen.startswith("helper_funcs/"):
                    mod = filen.split("/", maxsplit=1)[1]
                    if mod[0] not in (".", "_") and mod[-3:] == ".py":
                        splat = filen[:-3].rsplit("/", maxsplit=1)
                        mod_name = splat[0] if len(splat) == 1 else splat[1]
                        if mod_name in helpers:
                            LOGGER.debug(f"Overwrote {mod_name} from {repo}/{filen}")
                        helpers.update(
                            {mod_name: (raw_pattern.format(repo, filen), filen)}
                        )
                        LOGGER.debug(f"Found {mod_name} in {repo}/{filen}!")
                    continue

                splat = filen.rsplit("/", maxsplit=1)
                plugin = splat[0] if len(splat) == 1 else splat[1]
                if plugin[0] not in (".", "_") and plugin[-3:] == ".py":
                    splat = filen[:-3].rsplit("/", maxsplit=1)
                    plugin_name = splat[0] if len(splat) == 1 else splat[1]
                    if plugin_name == "builtin":
                        LOGGER.info("Ignoring the builtin plugin, cannot overwrite it.")
                        continue
                    elif plugin_name in plugins:
                        LOGGER.debug(f"Overwrote {plugin_name} from {repo}/{filen}")
                    plugins.update(
                        {plugin_name: (raw_pattern.format(repo, filen), filen)}
                    )
                    LOGGER.debug(f"Found {plugin} in {repo}/{filen}!")

        with open(rconfig_path, "w") as configfile:
            rconfig.write(configfile)

        return plugins, helpers

    def _import_plugin(self, name: str, path: str, content: str) -> None:
        """Import file and bytecode plugins."""
        to_overwrite: Union[None, str] = None
        callbacks: List[Callback] = []
        ppath = self.plugin_path.absolute() / name.replace(".", "/") / ".py"
        ubotpath = "userbot.plugins." + name
        log = "Successfully imported {}".format(name)

        for plugin in self.active_plugins:
            if plugin.name == name:
                LOGGER.info("Overwritting %s with %s.", plugin.path, path)
                to_overwrite = plugin
        if to_overwrite:
            self.active_plugins.remove(to_overwrite)

        try:
            if content:
                spec = importlib.machinery.ModuleSpec(
                    path, SourcelessPluginLoader(ubotpath, content, path), origin=path
                )
                match = github_raw_pattern.search(path)
                log += " from {}".format(match.group(1))
            else:
                # Local files use SourceFileLoader
                spec = importlib.util.find_spec(path)

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            # To make plugins impoartable use "sys.modules[path] = module".
            sys.modules[ubotpath] = module

            for n, cb in vars(module).items():
                if (
                    inspect.iscoroutinefunction(cb)
                    and not n.startswith("_")
                    and events._get_handlers(cb)
                ):
                    callbacks.append(Callback(n, cb))

            self.active_plugins.append(Plugin(name, callbacks, ppath, module))
            LOGGER.info(log)
        except Exception as e:
            self.client.failed_imports.append(path)
            LOGGER.error("Failed to import %s due to the error(s) below.", path)
            LOGGER.exception(e)

    def _import_helper(self, name: str, path: str, content: str) -> None:
        """Import file and bytecode plugins."""
        ubotpath = "userbot." + name
        ppath = root / (ubotpath.replace(".", "/") + ".py")
        match = github_raw_pattern.search(path).group(1)
        log = "Successfully imported helper {} from {}".format(name, match)
        if ppath.exists():
            LOGGER.info("Cannot overwrite %s helper from %s", ubotpath, match)
            return

        try:
            spec = importlib.machinery.ModuleSpec(
                path, SourcelessPluginLoader(ubotpath, content, path), origin=path
            )

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            # To make plugins impoartable use "sys.modules[path] = module".
            sys.modules[ubotpath] = module
            LOGGER.info(log)
        except Exception as e:
            self.client.failed_imports.append(path)
            LOGGER.error("Failed to import %s due to the error(s) below.", path)
            LOGGER.exception(e)


def _split_plugins(to_split: str or list) -> None:
    """Split the config's value for plugin keys."""
    if isinstance(to_split, str):
        return re.split(r"(?:\r\n|\n|, ?|\t| )", to_split)
    else:
        return to_split


async def get_pip_packages(requirements: str = None) -> list:
    """Get a list of all the pacakage's names."""
    if requirements:
        packages = requirements
    else:
        cmd = await asyncio.create_subprocess_exec(
            sys.executable.replace(" ", "\\ "),
            "-m",
            "pip",
            "freeze",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await cmd.communicate()
        packages = stdout.decode("utf-8")
    tmp = package_patern.findall(packages)
    return [package.lower() for package in tmp]


async def install_pip_packages(packages: List[str]) -> bool:
    """Install pip packages."""
    args = ["-m", "pip", "install", "--upgrade", "--user"]
    cmd = await asyncio.create_subprocess_exec(
        sys.executable.replace(" ", "\\ "),
        *args,
        *packages,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await cmd.communicate()
    return cmd.returncode == 0


def run_async(func: callable):
    """Run async functions with the right event loop."""
    if sys.platform.startswith("win"):
        loop = asyncio.ProactorEventLoop()
    else:
        loop = asyncio.get_event_loop()
    return loop.run_until_complete(func)


def restart_script() -> None:
    """Restart the current script."""
    executable = sys.executable.replace(" ", "\\ ")
    args = [executable, "-m", "userbot"]
    if sys.platform.startswith("win"):
        os.spawnle(os.P_NOWAIT, executable, *args, os.environ)
    else:
        os.execle(executable, *args, os.environ)
    sys.exit(0)
