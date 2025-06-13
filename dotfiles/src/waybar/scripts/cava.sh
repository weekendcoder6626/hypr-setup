#!/bin/bash

# Unicode characters: lower to higher
bar=" ▁▂▃▄▅▆▇█"

dict="s/;//g;"
i=0
while [ $i -lt ${#bar} ]; do
    dict="${dict}s/$i/${bar:$i:1}/g;"
    i=$((i+1))
done

# Symmetric cava config
config_file="/tmp/waybar_cava_config"
cat << EOF > $config_file
[general]
bars = 20

[output]
method = raw
raw_target = /dev/stdout
data_format = ascii
ascii_max_range = 7
EOF

cava -p $config_file | while read -r line; do
    # Replace numbers with glyphs
    visual=$(echo "$line" | sed "$dict")

    # Create symmetrical line:
    echo "$visual"
done
