import ctypes
import locale
import sys
import json
from pathlib import Path
from typing import Dict, List


LANGUAGES = {
    "en_US": "English",
    "zh_CN": "简体中文",
}


def system_lang_code() -> str:
    if sys.platform == "win32":
        kernel32 = ctypes.windll.kernel32
        lang_id = kernel32.GetUserDefaultUILanguage()
        buffer = ctypes.create_unicode_buffer(85)
        if kernel32.LCIDToLocaleName(lang_id, buffer, 85, 0):
            return buffer.value.replace("-", "_")
        return "en_US"
    return locale.getlocale(locale.LC_CTYPE)[0]


def choose_language(code: str) -> None:
    setattr(__get_lang_code, "__lang_code", code)


def get(key: str) -> str:
    code = __get_lang_code()
    data = __get_instance()
    try:
        return data[code][key]
    except KeyError:
        return key


def lang_names() -> List[str]:
    return list(LANGUAGES.values())


def lang_name(code: str) -> str:
    return LANGUAGES.get(code, "English")


def lang_code(name: str) -> str:
    return next((k for k, v in LANGUAGES.items() if v == name), "en_US")


def __get_instance() -> Dict[str, Dict[str, str]]:
    if not hasattr(__get_instance, "__instance"):
        lang_map = {}
        if getattr(sys, "frozen", False):
            lang_dir = Path(__file__).absolute().parent.joinpath("assets/lang")
        else:
            lang_dir = Path(__file__).absolute().parent.parent.joinpath("assets/lang")
        for path in lang_dir.rglob("*.json"):
            with open(path, encoding="utf-8") as file:
                lang_map[path.stem] = json.load(file)
        setattr(__get_instance, "__instance", lang_map)
    return getattr(__get_instance, "__instance")


def __get_lang_code() -> str:
    if not hasattr(__get_lang_code, "__lang_code"):
        setattr(__get_lang_code, "__lang_code", "en_US")
    return getattr(__get_lang_code, "__lang_code")
