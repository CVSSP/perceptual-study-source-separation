#!/bin/bash

OPTIONS="$@"
LISTEN="https://github.com/deeuu/listen.git"
TEMPLATES="_site"

function usage() {
    echo ""
}
STIM=true
VENV=true
case "$OPTIONS" in
    --nostim) STIM=false;;
    --novenv) VENV=false;;
    --help) usage;;
esac

# Exit if any command fails
set -e

# Clean up
rm -rf "site"
rm -rf "dependencies"
mkdir "dependencies"
cd "dependencies"

# Get MUSHRA GUI
git clone "$LISTEN" "listen"
cd "listen"
git checkout "e1de2a08a0f6b434d32c114d72997da80c79ace4"
cd ..

# Move all the files into place
cd ..
mv "dependencies/listen/site" "site"
cp -R "$TEMPLATES"/* "site/"
rm "site/_data/menu.yml"

if $VENV; then
    cd venvs
    make
    cd ../
fi


# Create stimuli and corresponding MUSHRA config files
if $STIM; then
    rm -rf "site/sounds"
    cd venvs
    source ./py3/bin/activate
    cd ../
    python "python/generate_stimuli.py"
    python "python/generate_interface_config_file.py"
    python "python/generate_familarisation_stimuli.py"
    deactivate
fi

# Clean up
rm -rf "dependencies"
