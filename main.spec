# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_dynamic_libs

# 排除系统 DLL, 正常都有的
EXCLUDE_DLLS = [
    "VCRUNTIME140.dll",
    "VCRUNTIME140_1.dll",
    "ucrtbase.dll",
    "MSVCP140.dll",
]
EXCLUDE_DLL_PREFIX = ("api-ms-win-crt-", "api-ms-win-core-")

# 打包 win64_process_toolkit 运行时
BINARIES = [
    ("./assets/icon.ico", "assets"),
    ("./assets/lang/*", "assets/lang"),
]
BINARIES += collect_dynamic_libs("win64_process_toolkit")


# 修复默认打包大量无用 DLL 的问题
def _fix_binaries(binaries):
    return [
        binary
        for binary in binaries
        if not binary[0] in EXCLUDE_DLLS
        and not binary[0].startswith(EXCLUDE_DLL_PREFIX)
    ]


a = Analysis(
    ["src/main.py"],
    pathex=["."],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    binaries=BINARIES,
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "email",
        "random",
        "logging",
        "urllib",
        "socket",
        "base64",
        "selectors",
        "textwrap",
        "tarfile",
        "argparse",
        "py_compile",
        "calendar",
        "copy",
        "csv",
        "dataclasses",
        "bz2",
        "gettext",
        "getopt",
        "pickle",
        "lzma",
        "quopri",
        "string",
        "stringprep",
        "tracemalloc",
        "inspect",
        "ast",
        "token",
        "tokenize",
        "unicodedata",
        "_socket",
        "_colorize",
        "_py_abc",
        "_strptime",
        # Base Libraires
        "abc",
        "codecs",
        "genericpath",
        "heapq",
        "io",
        "linecache",
        "ntpath",
        "posixpath",
        "traceback",
        "_collections_abc",
        "stat",
        "sre_compile",
        "sre_constants",
        "sre_parse",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
    optimize=2,
)

a.binaries = _fix_binaries(a.binaries)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="Minecraft DLL Injection Tool",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon="assets/icon.ico",
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version="Version.txt",
)
