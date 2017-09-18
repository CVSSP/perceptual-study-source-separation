#!/bin/bash

OPTIONS="$@"
LISTEN="https://github.com/deeuu/listen.git"
TEMPLATES="_site"

usage() {
    echo ""
    echo "Usage: $0 [--option]"
    echo ""
    echo "Options:"
    echo "  --nostim    don't generate audio files"
    echo "  --noenv     don't make python virtual environement"
    echo "  --help      show this help message"
    exit 0
}

STIM=true
VENV=true
case "$OPTIONS" in
    --nostim) STIM=false: VENV=false;;
    --noenv) VENV=false;;
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
git checkout "2351f936add02856b6e6f5e260d73a7ce9be79f2"
cd ..

# Move all the files into place
cd ..
mv "dependencies/listen/site" "site"
cp -R "$TEMPLATES"/* "site/"
rm "site/_data/menu.yml"
rm -rf "site/sounds"

if $VENV; then
    cd venvs
    make clean
    make
    cd ../
fi


# Create stimuli and corresponding MUSHRA config files
if $STIM; then
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
