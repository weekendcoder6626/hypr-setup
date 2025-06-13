#!/usr/bin/env bash

# Just use this script instead of rofi command

dir="$HOME/Desktop/working-dir/hypr-setup/dotfiles/src/rofi"
# theme='themes/image-style-horiz/orange-robot'
theme='themes/classic-types/classic-1'

## Run rofi with passed arguments and theme
rofi -theme "${dir}/${theme}.rasi" "$@"
