#!/bin/bash

options="󱎫  Pomodoro\n󰀠  Alarm"
choice=$(echo -e "$options" | /home/vs-horcrux/Desktop/working-dir/hypr-setup/dotfiles/src/rofi/launcher.sh -dmenu -p "Time Tools" -i)

case "$choice" in
    "󱎫  Pomodoro")
        pomatez --app_id float
        ;;
    "󰀠  Alarm")
        alarm-clock-applet
        ;;
esac
