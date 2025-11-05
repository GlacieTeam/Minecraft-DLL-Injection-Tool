import sys
import os
from ctypes import CDLL, c_char_p, c_uint32, c_bool


def __get_native_lib() -> CDLL:
    if not hasattr(__get_native_lib, "__instance__"):
        if getattr(sys, "frozen", False):
            lib_path = os.path.join(os.path.dirname(sys.executable), "InjectionLib.dll")
        else:
            lib_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "lib/InjectionLib.dll",
            )
        setattr(__get_native_lib, "__instance__", CDLL(lib_path))
        instance = getattr(__get_native_lib, "__instance__")
        instance.get_process_id.argtypes = [c_char_p]
        instance.get_process_id.restype = c_uint32
        instance.inject_dll.argtypes = [c_uint32, c_char_p]
        instance.inject_dll.restype = c_bool
    return getattr(__get_native_lib, "__instance__")


def get_process_id(process_name: str) -> int:
    return __get_native_lib().get_process_id(process_name.encode("utf-8"))


def inject_dll(process_id: int, dll_path: str) -> bool:
    return __get_native_lib().inject_dll(process_id, dll_path.encode("utf-8"))
