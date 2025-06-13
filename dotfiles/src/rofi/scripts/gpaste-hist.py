#!/usr/bin/env python3

import subprocess
import re

class ClipHist:
    def __init__(self, uuid: str, text: str):
        self.uuid = uuid
        self.text = text

    def preview(self, newline_repr="⏎") -> str:
        """Return a single-line preview replacing newlines with a symbol."""
        return self.text.replace('\n', newline_repr)

class ClipHistManager:
    UUID_PATTERN = re.compile(r'^[0-9a-fA-F-]{36}:')

    def __init__(self):
        self.entries = []

    def load_history(self):
        """Load clipboard history from gpaste-client."""
        try:
            output = subprocess.check_output(['gpaste-client', 'history'], text=True)
        except subprocess.CalledProcessError:
            self.entries = []
            return

        current_uuid = None
        current_text_lines = []

        for line in output.splitlines():
            if self.UUID_PATTERN.match(line):
                # Save previous entry
                if current_uuid is not None:
                    self.entries.append(ClipHist(current_uuid, "\n".join(current_text_lines)))
                # Start new entry
                current_uuid, content = line.split(": ", 1)
                current_text_lines = [content]
            else:
                current_text_lines.append(line)

        # Save last entry
        if current_uuid is not None:
            self.entries.append(ClipHist(current_uuid, "\n".join(current_text_lines)))

    def show_rofi_menu(self) -> int | None:
        preview_limit = 20
        # Prepare preview lines (limit to preview_limit)
        indexed_previews = [entry.preview() for entry in self.entries[:preview_limit]]

        # Path to your external rofi script
        rofi_script = "/home/vs-horcrux/Desktop/working-dir/hypr-setup/dotfiles/src/rofi/launcher.sh"

        # Run the script with rofi arguments, pass clipboard previews via stdin
        proc = subprocess.run(
            [rofi_script, "-dmenu", "-i", "-no-icon-theme", "-p", "Clipboard"],
            input="\n".join(indexed_previews),
            text=True,
            capture_output=True,
        )

        selection = proc.stdout.strip()
        if not selection:
            return None

        # Since the script now only prints preview lines, find index by matching preview text
        # (or better: show previews with indexes, but here matching preview string)
        try:
            return indexed_previews.index(selection)
        except ValueError:
            return None


    def select_entry(self, index: int):
        """Select clipboard entry by index using gpaste-client."""
        if 0 <= index < len(self.entries):
            uuid = self.entries[index].uuid
            subprocess.run(['gpaste-client', 'select', uuid])
            subprocess.run(['notify-send', 'GPaste', f"Selected: {self.entries[index].preview()}"])
        else:
            subprocess.run(['notify-send', 'GPaste', 'Selection failed'])

def main():
    manager = ClipHistManager()
    manager.load_history()

    print(manager.entries[0].text)

    if not manager.entries:
        subprocess.run(['notify-send', 'GPaste', 'Clipboard history is empty'])
        return

    selected_index = manager.show_rofi_menu()
    if selected_index is None:
        return

    manager.select_entry(selected_index)

if __name__ == "__main__":
    main()