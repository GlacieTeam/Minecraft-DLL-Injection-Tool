import sys
import json
from pathlib import Path
from typing import Dict


def __get_instance() -> Dict[str, Dict[str, str]]:
    if not hasattr(__get_instance, "__instance"):
        lang_map = {}
        if getattr(sys, "frozen", False):
            lang_dir = Path(__file__).absolute().parent.joinpath("lang")
        else:
            lang_dir = Path(__file__).absolute().parent.parent.joinpath("lang")
        for path in lang_dir.rglob("*.json"):
            with open(path, encoding="utf-8") as file:
                lang_map[path.stem] = json.load(file)
        setattr(__get_instance, "__instance", lang_map)
    return getattr(__get_instance, "__instance")


def __get_lang_code() -> str:
    if not hasattr(__get_lang_code, "__lang_code"):
        setattr(__get_lang_code, "__lang_code", "en_US")
    return getattr(__get_lang_code, "__lang_code")


def choose_language(lang_code: str) -> None:
    setattr(__get_lang_code, "__lang_code", lang_code)


def get(key: str) -> str:
    code = __get_lang_code()
    data = __get_instance()
    try:
        return data[code][key]
    except KeyError:
        return key


CODE_MAP = {
    "English": "en_US",
    "简体中文": "zh_CN",
}


def get_code(name: str):
    if name in CODE_MAP:
        return CODE_MAP[name]
    return "en_US"
