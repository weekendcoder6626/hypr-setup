import re

class Keybinding:
    def __init__(self, key_combination: str, command: str):
        self.key_combination = [c.strip() for c in key_combination.split(",")]  # e.g., "ALT, SPACE"
        self.command = command                  # e.g., "exec, rofi -show drun"

    def __repr__(self):
        return f"Keybinding({(",").join(self.key_combination)} -> {self.command})"
    
    def format_str(self):
        return f"bind = {(",").join(self.key_combination)}, {self.command}"

class Keybindings:
    def __init__(self, keybindings: list=[], main_mod: str="", mode="custom"):
        self.keybindings = keybindings  # List of Keybinding objects
        self.main_mod = main_mod        # e.g., "SUPER"
        self.mode = mode

    def get_by_combination(self, combination: str):
        """Returns the Keybinding(s) that exactly match the given combination."""
        comb_list = [c.strip() for c in combination.split(",")]
        return [kb for kb in self.keybindings if (",").join(kb.key_combination) == (",").join(comb_list)]

    def __repr__(self):
        return f"Keybindings(main_mod={self.main_mod}, count={len(self.keybindings)})"
    
    def check_unique(self, combination):
        searchRes = self.get_by_combination(combination)
        if len(searchRes) == 0:
            return (True, [])
        return (False, searchRes)
    
    def add_keybinding(self,keybinding: Keybinding, parse: bool=False):
        if(self.mode != "custom" and not parse):
            print("Can only add to custom keybindings")
            return False
        self.keybindings.append(keybinding)

    # def format_str(self):
    #     return ("\n").join([kb.format_str() for kb in self.keybindings])


def parse_keybindings(file_path: str, mainMod: bool) -> Keybindings:
    keybindings = Keybindings(
        [], "", "default" if mainMod else "custom"
    )
    variables = {}

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()

            # Skip empty and comment lines
            if not line or line.startswith('#'):
                continue

            # Handle variable definitions
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
            
            # Handle keybinding lines (bind, bindm, bindl, bindel)
            match = re.match(r'(bind\w*)\s*=\s*(.*)', line)
            if match:
                _, rest = match.groups()
                parts = [part.strip() for part in rest.split(',')]

                # Replace variables
                # parts = [variables.get(part, part) for part in parts]

                if len(parts) >= 2:
                    key_combo = (",").join(parts[:2])
                    command = ', '.join(parts[2:]) if len(parts) > 2 else ''
                    keybindings.add_keybinding(Keybinding(key_combo, command), True)
    # print(keybindings.keybindings[0], mainMod)
    return keybindings

defaultKeybindings = parse_keybindings("default/keybindings.conf", True)

customKeybindings = parse_keybindings("custom/keybindings.conf", False)


keybind = input("Enter Keybind:").strip()

print(defaultKeybindings.check_unique(keybind), customKeybindings.check_unique(keybind))
# print(len(defaultKeybindings.keybindings), len(customKeybindings.keybindings))