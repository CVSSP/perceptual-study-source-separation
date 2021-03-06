#!/bin/bash

OPTIONS="$1"

usage() {
    echo ""
    echo "Usage: $0 [--option]"
    echo ""
    echo "Options:"
    echo "  --noenv     don't make python virtual environement"
    echo "  --help      show this help message"
    exit 0
}

VENV=true
case "$OPTIONS" in
    --noenv) VENV=false;;
    --help) usage;;
esac

# Exit if any command fails
set -e

# Delete all wav files
rm -rf "site/sounds/*"


if $VENV; then
    cd venvs
    make clean
    make
    cd ../
elif ! [ -d "venvs/py3" ]; then
    echo     ""
    echo >&2 "py3 env is not existing, you can't use --noenv"
    exit 1
fi

# Create stimuli and corresponding MUSHRA config files
cd venvs
source ./py3/bin/activate
cd ../
python "python/generate_stimuli.py"
python "python/generate_interface_config_file.py"
python "python/generate_familarisation_stimuli.py"
deactivate
