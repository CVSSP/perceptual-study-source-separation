#!/bin/bash

OPTIONS="$@"
LISTEN="https://github.com/deeuu/listen.git"
TEMPLATES="_site"

function usage() {
    echo ""
}
case "$OPTIONS" in
    --nostim) STIM=false;;
    --help) usage;;
    *) STIM=true;;
esac

# Exit if any command fails
set -e

# Clean up
rm -rf "site"
rm -rf "dependencies"
mkdir "dependencies"
cd "dependencies"

# Get MUSHRA GUI (WebAudioEvaluationTool)
git clone "$LISTEN" "listen"
cd "listen"
git checkout "7fdd3d0f91662181974e99beae9e231cceb1e88c"
cd ..

# Move all the files into place
cd ..
mv "dependencies/listen/site" "site"
cp -R "$TEMPLATES"/* "site/"
rm "site/_data/menu.yml"

# Create stimuli and corresponding MUSHRA config files
if $STIM; then
    rm -rf "site/sounds"
    python "python/generate_stimuli.py"
    python "python/generate_interface_config_file.py"
fi

# Clean up
rm -rf "dependencies"
