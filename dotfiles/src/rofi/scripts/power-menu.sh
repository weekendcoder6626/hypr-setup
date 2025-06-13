#!/bin/bash

options="  Lock\n󰍃  Logout\n󰜉  Reboot\n  Shutdown"
choice=$(echo -e "$options" | /home/vs-horcrux/Desktop/working-dir/hypr-setup/dotfiles/src/rofi/launcher.sh -dmenu -p "Power Menu" -i)

case "$choice" in
    "  Lock")
        hyprlock
        ;;
    "󰍃  Logout")
        hyprctl dispatch exit
        ;;
    "󰜉  Reboot")
        systemctl reboot
        ;;
    "  Shutdown")
        systemctl poweroff
        ;;
esac
