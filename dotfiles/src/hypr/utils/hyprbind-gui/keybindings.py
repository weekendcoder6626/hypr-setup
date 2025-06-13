import re
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from typing import List, Tuple, Dict

# === Dark Theme Colors ===
BG_COLOR = "#1e1e1e"
FG_COLOR = "#e0e0e0"
HIGHLIGHT_COLOR = "#ffffff"
ENTRY_BG = "#2e2e2e"
ENTRY_FG = FG_COLOR


class Keybinding:
    def __init__(self, key_combination: str, command: str, description: str = "") -> None:
        self.key_combination: List[str] = [c.strip() for c in key_combination.split(",")]
        self.command: str = command
        self.description: str = description

    def __repr__(self) -> str:
        return f"Keybinding({(',').join(self.key_combination)} -> {self.command} | {self.description})"

    def format_str(self) -> str:
        desc = f" # {self.description}" if self.description else ""
        return f"bind = {(',').join(self.key_combination)}, {self.command}{desc}"


class Keybindings:
    def __init__(self, keybindings: List[Keybinding] = [], main_mod: str = "", mode: str = "custom") -> None:
        self.keybindings: List[Keybinding] = keybindings
        self.main_mod: str = main_mod
        self.mode: str = mode

    def get_by_combination(self, combination: str) -> List[Keybinding]:
        comb_list: List[str] = [c.strip() for c in combination.split(",")]
        return [kb for kb in self.keybindings if (",").join(kb.key_combination) == (",").join(comb_list)]

    def check_unique(self, combination: str) -> Tuple[bool, List[Keybinding]]:
        searchRes: List[Keybinding] = self.get_by_combination(combination)
        return (len(searchRes) == 0, searchRes)

    def add_keybinding(self, keybinding: Keybinding, parse: bool = False) -> bool:
        self.keybindings.append(keybinding)
        return True



def parse_keybindings(file_path: str, mainMod: bool) -> Keybindings:
    keybindings: Keybindings = Keybindings([], "", "default" if mainMod else "custom")
    variables: Dict[str, str] = {}

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if line.startswith('$'):
                key, value = map(str.strip, line.split('=', 1))
                variables[key] = value
                if key == "$mainMod":
                    if mainMod:
                        keybindings.main_mod = value
                continue

            match = re.match(r'(bind\w*)\s*=\s*(.*)', line)
            if match:
                _, rest = match.groups()
                if '#' in rest:
                    rest, comment = rest.split('#', 1)
                    description = comment.strip()
                else:
                    description = ""
                parts: List[str] = [part.strip() for part in rest.split(',')]
                if len(parts) >= 2:
                    key_combo: str = (",").join(parts[:2])
                    command: str = ', '.join(parts[2:]) if len(parts) > 2 else ''
                    keybindings.add_keybinding(Keybinding(key_combo, command, description), True)
    return keybindings


class KeybindingGUI:
    def __init__(self, master: tk.Tk, default_keybindings: Keybindings, custom_keybindings: Keybindings) -> None:
        self.master = master
        self.default_keybindings = default_keybindings
        self.custom_keybindings = custom_keybindings

        master.title("Keybindings Viewer & Checker")
        master.configure(bg=BG_COLOR)

        # Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background=BG_COLOR,
                        foreground=FG_COLOR,
                        fieldbackground=BG_COLOR,
                        rowheight=25)
        style.configure("Treeview.Heading", background=BG_COLOR, foreground=HIGHLIGHT_COLOR)

        self.tree = ttk.Treeview(master, columns=("Key Combination", "Command", "Mode", "Description"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.populate_tree()

        input_frame = tk.Frame(master, bg=BG_COLOR)
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Enter Key Combination:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, padx=5, pady=5)
        self.combo_entry = tk.Entry(input_frame, width=35, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR)
        self.combo_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Delimiter:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=2, padx=5, pady=5)
        self.delim_var = tk.StringVar(value=",")
        self.delim_menu = ttk.Combobox(input_frame, textvariable=self.delim_var, values=[",", "+"], state="readonly", width=5)
        self.delim_menu.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="Search Description:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(input_frame, width=35, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR)
        self.search_entry.grid(row=1, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(master, bg=BG_COLOR)
        btn_frame.pack(pady=8)

        tk.Button(btn_frame, text="Check Uniqueness", command=self.check_uniqueness, bg=HIGHLIGHT_COLOR).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Search", command=self.search_description, bg=HIGHLIGHT_COLOR).pack(side="left", padx=10)

        self.result_label = tk.Label(master, text="", bg=BG_COLOR, fg=FG_COLOR)
        self.result_label.pack(pady=5)

    def populate_tree(self, filtered=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        records = filtered if filtered else self.default_keybindings.keybindings + self.custom_keybindings.keybindings
        for kb in records:
            mode = "Default" if kb in self.default_keybindings.keybindings else "Custom"
            self.tree.insert("", tk.END, values=(" + ".join(kb.key_combination), kb.command, mode, kb.description))

    def check_uniqueness(self):
        combo = self.combo_entry.get().strip()
        delim = self.delim_var.get()
        normalized = ",".join([c.strip() for c in combo.split(delim)])

        is_unique_def, def_conflicts = self.default_keybindings.check_unique(normalized)
        is_unique_cus, cus_conflicts = self.custom_keybindings.check_unique(normalized)

        all_conflicts = [("Default", kb) for kb in def_conflicts] + [("Custom", kb) for kb in cus_conflicts]
        if all_conflicts:
            self.result_label.config(text="Conflict found!", fg="red")
            text = "\n".join([f"[{mode}] {','.join(kb.key_combination)} -> {kb.command} ({kb.description})" for mode, kb in all_conflicts])
            messagebox.showerror("Conflict", f"Key combination already used:\n{text}")
        else:
            self.result_label.config(text="Key combination is unique!", fg="green")

    def search_description(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            self.populate_tree()
            return
        matches = [kb for kb in self.default_keybindings.keybindings + self.custom_keybindings.keybindings if query in kb.description.lower()]
        self.populate_tree(filtered=matches)


if __name__ == '__main__':
    default_path = os.path.expanduser("~/Desktop/working-dir/hypr-setup/dotfiles/src/hypr/default/keybindings.conf")
    custom_path = os.path.expanduser("~/Desktop/working-dir/hypr-setup/dotfiles/src/hypr/custom/keybindings.conf")

    defaultKeybindings = parse_keybindings(default_path, True)
    customKeybindings = parse_keybindings(custom_path, False)

    root = tk.Tk()
    app = KeybindingGUI(root, defaultKeybindings, customKeybindings)
    root.mainloop()
