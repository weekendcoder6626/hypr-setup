# Execute this to apply your changes to the main config file(~/.config/hypr/hyprland.conf)

cp ~/.config/hypr/hyprland.conf ~/.config/hypr/hyprland.conf_bkp
cat $(dirname $0)/../hyprland.conf > ~/.config/hypr/hyprland.conf

hyprctl reload