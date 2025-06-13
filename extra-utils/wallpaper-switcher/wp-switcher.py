import os, subprocess
from tkinter import Tk, Frame, Label, Scrollbar, Canvas
from PIL import Image, ImageTk
from tkinter.font import Font

# === Config ===
WALLPAPER_DIR = os.path.expanduser("~/Pictures")
THUMB_SIZE = (200, 120)
HYPERPAPER_CONF = os.path.expanduser("~/Desktop/working-dir/hypr-setup/dotfiles/src/hypr/hyprpaper.conf")

# Dark theme colors
BG_COLOR = "#1e1e1e"
FG_COLOR = "#e0e0e0"
# FOLDER_COLOR = "#ff5555"  # Change this to customize folder name tile color
FOLDER_COLOR = "#ffffff" 


def set_wallpaper(path):
    with open(HYPERPAPER_CONF, "w") as f:
        f.write(f"preload = {path}\nwallpaper = ,{path}\n")
    subprocess.run(["pkill", "hyprpaper"])
    subprocess.Popen([
        "/home/vs-horcrux/Desktop/working-dir/hypr-setup/dotfiles/src/hypr/utils/reload-hyprpaper.sh"
    ])


def get_images():
    valid_exts = (".png", ".jpg", ".jpeg")
    image_dict = {}
    for dp, _, fn in os.walk(WALLPAPER_DIR):
        images = [os.path.join(dp, f) for f in fn if f.lower().endswith(valid_exts)]
        if images:
            image_dict[dp] = images
    return image_dict


def main():
    root = Tk()
    root.geometry("1200x800")
    root.title("Wallpaper Picker")
    root.configure(bg=BG_COLOR)

    canvas = Canvas(root, bg=BG_COLOR, highlightthickness=0)
    
    scrollbar = Scrollbar(
        root,
        command=canvas.yview,
        bg=FOLDER_COLOR,               # Scrollbar background
        activebackground="#444444", # When hovering or clicking
        troughcolor="#1e1e1e",       # The track background
        highlightthickness=0,
        bd=0
    )


    frame = Frame(canvas, bg=BG_COLOR)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    thumbs = []

    image_dict = get_images()
    for folder, paths in sorted(image_dict.items()):
        # Folder name tile
        underline_font = Font(family="Arial", size=14, weight="bold", underline=1)
        folder_label = Label(
            frame,
            text=os.path.basename(folder),
            font=underline_font,
            anchor="w",
            bg=BG_COLOR,
            fg=FOLDER_COLOR,
            padx=10,
            pady=5
        )
        folder_label.pack(fill="x", padx=10, pady=(15, 5))

        folder_frame = Frame(frame, bg=BG_COLOR)
        folder_frame.pack(fill="x", padx=10, pady=(0, 10))

        for path in paths:
            try:
                img = Image.open(path)
                img.thumbnail(THUMB_SIZE)
                tkimg = ImageTk.PhotoImage(img)
                thumbs.append(tkimg)

                img_frame = Frame(folder_frame, bg=BG_COLOR)
                img_frame.pack(side="left", padx=5, pady=5)

                # Hover effect handlers
                def on_enter(e, widget):
                    widget.configure(highlightbackground=FOLDER_COLOR, highlightcolor=FOLDER_COLOR, cursor="hand2")

                def on_leave(e, widget):
                    widget.configure(highlightbackground="black", highlightcolor="black")

                lbl = Label(
                    img_frame,
                    image=tkimg,
                    bg=BG_COLOR,
                    highlightthickness=2,
                    highlightbackground="black",
                    highlightcolor="black"
                )
                lbl.bind("<Button-1>", lambda e, p=path: set_wallpaper(p))
                lbl.bind("<Enter>", lambda e, w=lbl: on_enter(e, w))
                lbl.bind("<Leave>", lambda e, w=lbl: on_leave(e, w))
                lbl.pack()

                name_label = Label(
                    img_frame,
                    text=os.path.basename(path),
                    wraplength=THUMB_SIZE[0],
                    justify="center",
                    fg=FG_COLOR,
                    bg=BG_COLOR
                )
                name_label.pack()
            except:
                continue

    def on_resize(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_resize)

    # === Mousewheel scroll support ===
    def _on_mousewheel(event):
        if os.name == "nt":
            canvas.yview_scroll(-1 * (event.delta // 120), "units")
        elif os.name == "posix":
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def _on_linux_scroll(event):
        if event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")

    if os.name == "nt":
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    elif os.name == "posix":
        canvas.bind_all("<Button-4>", _on_linux_scroll)
        canvas.bind_all("<Button-5>", _on_linux_scroll)
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    root.mainloop()


if __name__ == "__main__":
    main()
