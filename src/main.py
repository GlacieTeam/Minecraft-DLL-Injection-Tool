import os
import sys
import webbrowser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import win64_process_toolkit as injector


def try_launch_minecraft() -> int:
    webbrowser.open("minecraft:")
    return injector.get_process_id("Minecraft.Windows.exe")


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Minecraft DLL 注入工具")
        self.resizable(False, False)
        if getattr(sys, "frozen", False):
            icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
        else:
            icon = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "assets/icon.ico",
            )
        self.iconbitmap(icon)

        self.process_name = tk.StringVar()
        self.dll_path = tk.StringVar()

        pad = {"padx": 5, "pady": 5, "sticky": "ew"}

        ttk.Label(self, text="请选择需要注入的 DLL 文件：").grid(row=1, column=0, **pad)
        ttk.Entry(self, textvariable=self.dll_path, state="readonly", width=30).grid(
            row=1, column=1, **pad
        )
        ttk.Button(self, text="浏览…", command=self.browse_dll).grid(
            row=1, column=2, **pad
        )

        ttk.Button(self, text="注入 DLL", command=self.on_inject).grid(
            row=2, column=0, columnspan=3, pady=10
        )

    def browse_dll(self):
        filetypes = [("DLL 文件", "*.dll"), ("所有文件", "*.*")]
        path = filedialog.askopenfilename(title="选择要注入的 DLL", filetypes=filetypes)
        if path:
            self.dll_path.set(os.path.normpath(path))

    def on_inject(self):
        dll = self.dll_path.get().strip()
        if not dll:
            messagebox.showerror("错误", "请先选择需要注入的 DLL 文件")
            return

        proc = injector.get_process_id("Minecraft.Windows.exe")
        if proc == 0:
            proc = try_launch_minecraft()

        if proc == 0:
            messagebox.showerror("错误", "无法启动 Minecraft！")

        if injector.inject_dll(proc, dll):
            messagebox.showinfo("成功", "DLL 注入成功！")
        else:
            messagebox.showerror("失败", "DLL 注入失败！")


if __name__ == "__main__":
    MainWindow().mainloop()
