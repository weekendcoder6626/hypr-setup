#!/bin/bash

# -----------------------------------------------------
# Quit all running waybar instances
# -----------------------------------------------------
killall hyprpaper 2>/dev/null
pkill hyprpaper 2>/dev/null
sleep 0.5

# -----------------------------------------------------
# Launch waybar with custom config and style
# -----------------------------------------------------
CONFIG_PATH="$HOME/Desktop/working-dir/hypr-setup/dotfiles/src/hypr/hyprpaper.conf"

uwsm app -- hyprpaper -c "$CONFIG_PATH"
