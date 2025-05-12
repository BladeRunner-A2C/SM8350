#!/usr/bin/env bash

audio="snippets/audio.xml"
camera="snippets/camera.xml"
cv="snippets/cv.xml"
display="snippets/display.xml"
graphics="snippets/graphics.xml"
qssi="qssi.xml"
kernel="snippets/kernel.xml"
vendor="snippets/vendor.xml"
video="snippets/video.xml"
output="target.xml"

# Remove the output file
rm -f "$output"

# Extract content between <manifest> tags and merge them
{
    echo '<?xml version="1.0" encoding="UTF-8"?>'
    echo "<manifest>"
    xmlstarlet sel -t -c "//manifest/node()" "$qssi"
    xmlstarlet sel -t -c "//manifest/node()" "$kernel"
    xmlstarlet sel -t -c "//manifest/node()" "$audio"
    xmlstarlet sel -t -c "//manifest/node()" "$camera"
    xmlstarlet sel -t -c "//manifest/node()" "$cv"
    xmlstarlet sel -t -c "//manifest/node()" "$display"
    xmlstarlet sel -t -c "//manifest/node()" "$graphics"
    xmlstarlet sel -t -c "//manifest/node()" "$vendor"
    xmlstarlet sel -t -c "//manifest/node()" "$video"
    echo "</manifest>"
} | xmlstarlet fo | xmlstarlet ed \
    -d "//manifest/remote[position() > 1]" \
    -d "//manifest/default[position() > 1]" \
    -d "//manifest/refs" \
    -d "//manifest/project/@remote" \
    -i "//manifest/default" -t attr -n "sync-c" -v "true" \
    -i "//manifest/default" -t attr -n "sync-tags" -v "false" \
    > "$output"
