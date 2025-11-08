import os
import sys
import webbrowser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import win64_process_toolkit as injector
import i18n


def try_launch_minecraft() -> int:
    webbrowser.open("minecraft:")
    return injector.get_process_id("Minecraft.Windows.exe")


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        if getattr(sys, "frozen", False):
            icon = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "assets/icon.ico"
            )
        else:
            icon = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "assets/icon.ico",
            )
        self.iconbitmap(icon)

        self.language = tk.StringVar(value=i18n.lang_name(i18n.system_lang_code()))
        self.dll_path = tk.StringVar()

        pad = {
            "padx": 5,
            "pady": 5,
            "sticky": "ew",
        }

        self.ui_title = tk.Label(
            self,
            fg="black",
            font=("Microsoft YaHei", 18, "bold"),
        )
        self.ui_title.grid(row=0, column=0, columnspan=3, pady=(10, 15))

        lang_cb = ttk.Combobox(
            self,
            textvariable=self.language,
            values=i18n.lang_names(),
            state="readonly",
            width=9,
        )
        lang_cb.grid(row=0, column=2, sticky="ne", padx=6, pady=4)
        lang_cb.bind("<<ComboboxSelected>>", self.on_lang_change)

        self.columnconfigure(1, weight=1)

        self.dll_lable = ttk.Label(self)
        self.dll_lable.grid(row=1, column=0, **pad)

        self.dll_entry = ttk.Entry(
            self, textvariable=self.dll_path, state="readonly", width=32
        )
        self.dll_entry.grid(row=1, column=1, **pad)

        self.dll_button = ttk.Button(self, command=self.browse_dll)
        self.dll_button.grid(row=1, column=2, **pad)

        ttk.Style().configure(
            "Big.TButton", font=("Microsoft YaHei", 12, "bold"), padding=(10, 5)
        )
        self.inject_button = ttk.Button(
            self, command=self.on_inject, style="Big.TButton"
        )
        self.inject_button.grid(row=2, column=0, columnspan=3, pady=10)

        self.on_lang_change()

    def browse_dll(self):
        filetypes = [(i18n.get("DLL File"), "*.dll"), (i18n.get("All Files"), "*.*")]
        path = filedialog.askopenfilename(
            title=i18n.get("Select File"), filetypes=filetypes
        )
        if path:
            self.dll_path.set(os.path.normpath(path).strip())

    def on_inject(self):
        dll = self.dll_path.get()
        if not dll:
            messagebox.showerror(
                i18n.get("ERROR"),
                i18n.get("Please select the DLL file to inject first!"),
            )
            return

        proc = injector.get_process_id("Minecraft.Windows.exe")
        if proc == 0:
            proc = try_launch_minecraft()

        if proc == 0:
            messagebox.showerror(
                i18n.get("ERROR"), i18n.get("Failed to launch Minecraft!")
            )

        if injector.inject_dll(proc, dll):
            messagebox.showinfo(
                i18n.get("Success"), i18n.get("DLL successfully injected!")
            )
        else:
            messagebox.showerror(i18n.get("ERROR"), i18n.get("DLL injection failed!"))

    def on_lang_change(self, _=None):
        i18n.choose_language(i18n.lang_code(self.language.get()))
        self.title(i18n.get("Minecraft DLL Injection Tool"))
        self.ui_title.config(text=i18n.get("Minecraft DLL Injection Tool"))
        self.dll_lable.config(text=i18n.get("Please select the DLL file to inject:"))
        self.dll_button.config(text=i18n.get("Browse..."))
        self.inject_button.config(text=i18n.get("Inject DLL"))


if __name__ == "__main__":
    MainWindow().mainloop()
