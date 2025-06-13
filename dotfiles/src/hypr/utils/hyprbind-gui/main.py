import re
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple, Dict


class Keybinding:
    def __init__(self, key_combination: str, command: str) -> None:
        self.key_combination: List[str] = [c.strip() for c in key_combination.split(",")]
        self.command: str = command

    def __repr__(self) -> str:
        return f"Keybinding({(',').join(self.key_combination)} -> {self.command})"

    def format_str(self) -> str:
        return f"bind = {(',').join(self.key_combination)}, {self.command}"


class Keybindings:
    def __init__(self, keybindings: List[Keybinding] = [], main_mod: str = "", mode: str = "custom") -> None:
        self.keybindings: List[Keybinding] = keybindings
        self.main_mod: str = main_mod
        self.mode: str = mode

    def get_by_combination(self, combination: str) -> List[Keybinding]:
        comb_list: List[str] = [c.strip() for c in combination.split(",")]
        return [kb for kb in self.keybindings if (",").join(kb.key_combination) == (",").join(comb_list)]

    def __repr__(self) -> str:
        return f"Keybindings(main_mod={self.main_mod}, count={len(self.keybindings)})"

    def check_unique(self, combination: str) -> Tuple[bool, List[Keybinding]]:
        searchRes: List[Keybinding] = self.get_by_combination(combination)
        return (len(searchRes) == 0, searchRes)

    def add_keybinding(self, keybinding: Keybinding, parse: bool = False) -> bool:
        if self.mode != "custom" and not parse:
            print("Can only add to custom keybindings")
            return False
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
                        keybindings.mode = "default"
                        keybindings.main_mod = value
                    else:
                        keybindings.mode = "custom"
                continue

            match = re.match(r'(bind\w*)\s*=\s*(.*)', line)
            if match:
                _, rest = match.groups()
                parts: List[str] = [part.strip() for part in rest.split(',')]
                if len(parts) >= 2:
                    key_combo: str = (",").join(parts[:2])
                    command: str = ', '.join(parts[2:]) if len(parts) > 2 else ''
                    keybindings.add_keybinding(Keybinding(key_combo, command), True)
    return keybindings


class KeybindingGUI:
    def __init__(self, master: tk.Tk, default_keybindings: Keybindings, custom_keybindings: Keybindings) -> None:
        self.master: tk.Tk = master
        self.default_keybindings: Keybindings = default_keybindings
        self.custom_keybindings: Keybindings = custom_keybindings

        self.delimiters: Dict[str, str] = {
            ",": ",",
            "+": "+"
        }

        master.title("Keybindings Viewer & Checker")

        self.tree: ttk.Treeview = ttk.Treeview(master, columns=("Key Combination", "Command", "Mode"), show="headings")
        self.tree.heading("Key Combination", text="Key Combination")
        self.tree.heading("Command", text="Command")
        self.tree.heading("Mode", text="Mode")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.populate_tree()

        input_frame: ttk.Frame = ttk.Frame(master)
        input_frame.pack(pady=5)

        ttk.Label(input_frame, text="Enter Key Combination:").grid(row=0, column=0, padx=5, pady=5)

        self.combo_entry: ttk.Entry = ttk.Entry(input_frame, width=35)
        self.combo_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Delimiter:").grid(row=0, column=2, padx=5, pady=5)

        self.delim_var: tk.StringVar = tk.StringVar(value=",")
        self.delim_dropdown: ttk.Combobox = ttk.Combobox(
            input_frame,
            textvariable=self.delim_var,
            values=list(self.delimiters.keys()),
            state="readonly",
            width=5
        )
        self.delim_dropdown.grid(row=0, column=3, padx=5, pady=5)

        # Centered check button
        button_frame: ttk.Frame = ttk.Frame(master)
        button_frame.pack()
        check_btn: ttk.Button = ttk.Button(button_frame, text="Check Uniqueness", command=self.check_uniqueness)
        check_btn.pack(pady=8)

        self.result_label: ttk.Label = ttk.Label(master, text="")
        self.result_label.pack(pady=5)

    def populate_tree(self) -> None:
        for kb in self.default_keybindings.keybindings:
            self.tree.insert("", tk.END, values=(" + ".join(kb.key_combination), kb.command, "Default"))
        for kb in self.custom_keybindings.keybindings:
            self.tree.insert("", tk.END, values=(" + ".join(kb.key_combination), kb.command, "Custom"))

    def check_uniqueness(self) -> None:
        combination_input: str = self.combo_entry.get().strip()
        delimiter: str = self.delim_var.get()

        combination: str = ",".join([c.strip() for c in combination_input.split(delimiter)])

        is_unique_def, conflicts_def = self.default_keybindings.check_unique(combination)
        is_unique_cus, conflicts_cus = self.custom_keybindings.check_unique(combination)

        conflicts: List[Tuple[str, Keybinding]] = [("Default", kb) for kb in conflicts_def] + [("Custom", kb) for kb in conflicts_cus]

        if conflicts:
            self.result_label.config(text="Conflict found! See details below.", foreground="red")
            conflict_text: str = "\n".join([f"[{mode}] {','.join(kb.key_combination)} -> {kb.command}" for mode, kb in conflicts])
            messagebox.showerror("Conflict", f"Key combination already used:\n{conflict_text}")
        else:
            self.result_label.config(text="Key combination is unique!", foreground="green")


if __name__ == '__main__':
    defaultKeybindingsPath: str = "/home/vs-horcrux/Desktop/working-dir/hypr-setup/dotfiles/src/hypr/default/keybindings.conf"
    customKeybindingsPath: str = "/home/vs-horcrux/Desktop/working-dir/hypr-setup/dotfiles/src/hypr/custom/keybindings.conf"

    defaultKeybindings: Keybindings = parse_keybindings(defaultKeybindingsPath, True)
    customKeybindings: Keybindings = parse_keybindings(customKeybindingsPath, False)

    root: tk.Tk = tk.Tk()
    app: KeybindingGUI = KeybindingGUI(root, defaultKeybindings, customKeybindings)
    root.mainloop()
