#!/bin/bash

# -----------------------------------------------------
# Quit all running waybar instances
# -----------------------------------------------------
killall waybar 2>/dev/null
pkill waybar 2>/dev/null
sleep 0.5

# -----------------------------------------------------
# Launch waybar with custom config and style
# -----------------------------------------------------
CONFIG_PATH="$HOME/Desktop/working-dir/hypr-setup/dotfiles/src/waybar/config.jsonc"
STYLE_PATH="$HOME/Desktop/working-dir/hypr-setup/dotfiles/src/waybar/style.css"

uwsm app -- waybar -c "$CONFIG_PATH" -s "$STYLE_PATH"
