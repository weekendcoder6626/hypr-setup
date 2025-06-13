#!/bin/sh

CACHE_DIR="${XDG_RUNTIME_DIR:-/tmp}"
CACHE_FILE="$CACHE_DIR/waybar_media_state.json"

players=$(playerctl -l 2>/dev/null)

player_exists() {
    local p=$1
    echo "$players" | grep -iq "$p"
    return $?
}

chosen_player=""
status=""

for player in $players; do
    current_status=$(playerctl --player="$player" status 2>/dev/null)
    if [ "$current_status" = "Playing" ]; then
        chosen_player="$player"
        status="$current_status"
        break
    fi
done

get_cached_alt() {
    if [ -f "$CACHE_FILE" ]; then
        grep -oP '"alt": *"\K[^"]+' "$CACHE_FILE"
    else
        echo ""
    fi
}

cached_alt=$(get_cached_alt)

if [ -n "$chosen_player" ]; then
    artist=$(playerctl --player="$chosen_player" metadata artist 2>/dev/null)
    title=$(playerctl --player="$chosen_player" metadata title 2>/dev/null)

    maxlen=30
    if [ ${#title} -gt $maxlen ]; then
        title="${title:0:$maxlen}..."
    fi

    if echo "$chosen_player" | grep -qi "brave"; then
        alt="browser"   # Changed here
    elif echo "$chosen_player" | grep -qi "spotify"; then
        alt="spotify"
    else
        alt="media"
    fi

    output="{\"text\": \"$artist - $title\", \"alt\": \"$alt\"}"

    echo "$output" > "$CACHE_FILE"
    echo "$output"
else
    # Cache invalidation checks still for "brave"
    if [ "$cached_alt" = "browser" ] && ! player_exists "brave"; then
        rm -f "$CACHE_FILE"
        echo '{"text": "", "alt": "arch"}'
        exit 0
    fi

    if [ "$cached_alt" = "spotify" ] && ! player_exists "spotify"; then
        rm -f "$CACHE_FILE"
        echo '{"text": "", "alt": "arch"}'
        exit 0
    fi

    if [ -f "$CACHE_FILE" ]; then
        cat "$CACHE_FILE"
    else
        echo '{"text": "", "alt": "arch"}'
    fi
fi
