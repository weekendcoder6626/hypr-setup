#!/bin/sh

CACHE_FILE="${XDG_RUNTIME_DIR:-/tmp}/waybar_media_state.json"

if [ ! -f "$CACHE_FILE" ]; then
    echo "No media cache found."
    echo "No known player in focus cache: $alt"
    notify-send "Opening Terminal" -t 500 && uwsm app -- kitty
    exit 0
fi

# Extract alt from cache
alt=$(grep -oP '"alt": *"\K[^"]+' "$CACHE_FILE")

# Map alt to app class/window title
case "$alt" in
    spotify)
        app_class="Spotify"
        ;;
    browser)
        app_class="Brave-browser"
        ;;
    *)
        echo "No known player in focus cache: $alt"
        # notify-send "Opening Terminal" -t 500 && uwsm app -- kitty
        exit 0
        ;;
esac

# Try Hyprland
if command -v hyprctl >/dev/null 2>&1; then
    hyprctl dispatch focuswindow class:"$app_class"
    exit 0
fi

echo "No supported Wayland compositor focus command found."
exit 1
