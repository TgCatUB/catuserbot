from typing import Dict, List, Union

from ..helpers.utils.extdl import install_pip

try:
    from urlextract import URLExtract
except ModuleNotFoundError:
    install_pip("urlextract")
    from urlextract import URLExtract

from ..Config import Config

extractor = URLExtract()


def get_data(about, type):
    data = about[type]
    urls = extractor.find_urls(data)
    if len(urls) > 0:
        return data
    return data.capitalize()


def _format_about(
    about: Union[str, Dict[str, Union[str, List[str], Dict[str, str]]]]
) -> str:  # sourcery no-metrics
    if not isinstance(about, dict):
        return about
    tmp_chelp = ""
    if "header" in about and isinstance(about["header"], str):
        tmp_chelp += f"__{about['header'].title()}__"
        del about["header"]
    if "description" in about and isinstance(about["description"], str):
        tmp_chelp += (
            "\n\n✘  **Description :**\n" f"__{get_data(about , 'description')}__"
        )
        del about["description"]
    if "flags" in about:
        tmp_chelp += "\n\n✘  **Available Flags :**"
        if isinstance(about["flags"], dict):
            for f_n, f_d in about["flags"].items():
                tmp_chelp += f"\n    ▫ `{f_n}` : __{f_d.lower()}__"
        else:
            tmp_chelp += f"\n    {about['flags']}"
        del about["flags"]
    if "options" in about:
        tmp_chelp += "\n\n✘  **Available Options :**"
        if isinstance(about["options"], dict):
            for o_n, o_d in about["options"].items():
                tmp_chelp += f"\n    ▫ `{o_n}` : __{o_d.lower()}__"
        else:
            tmp_chelp += f"\n    __{about['options']}__"
        del about["options"]
    if "types" in about:
        tmp_chelp += "\n\n✘  **Supported Types :**"
        if isinstance(about["types"], list):
            for _opt in about["types"]:
                tmp_chelp += f"\n    `{_opt}` ,"
        else:
            tmp_chelp += f"\n    __{about['types']}__"
        del about["types"]
    if "usage" in about:
        tmp_chelp += "\n\n✘  **Usage :**"
        if isinstance(about["usage"], list):
            for ex_ in about["usage"]:
                tmp_chelp += f"\n    `{ex_}`"
        else:
            tmp_chelp += f"\n    `{about['usage']}`"
        del about["usage"]
    if "examples" in about:
        tmp_chelp += "\n\n✘  **Examples :**"
        if isinstance(about["examples"], list):
            for ex_ in about["examples"]:
                tmp_chelp += f"\n    `{ex_}`"
        else:
            tmp_chelp += f"\n    `{about['examples']}`"
        del about["examples"]
    if "others" in about:
        tmp_chelp += f"\n\n✘  **Others :**\n__{get_data(about , 'others')}__"
        del about["others"]
    if about:
        for t_n, t_d in about.items():
            tmp_chelp += f"\n\n✘  **{t_n.title()} :**\n"
            if isinstance(t_d, dict):
                for o_n, o_d in t_d.items():
                    tmp_chelp += f"    ▫ `{o_n}` : __{get_data(t_d , o_n)}__\n"
            elif isinstance(t_d, list):
                for _opt in t_d:
                    tmp_chelp += f"    `{_opt}` ,"
                tmp_chelp += "\n"
            else:
                tmp_chelp += f"__{get_data(about ,t_n)}__"
                tmp_chelp += "\n"
    return tmp_chelp.replace("{tr}", Config.COMMAND_HAND_LER)
