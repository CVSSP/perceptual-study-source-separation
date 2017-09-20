#!/bin/bash

usage() {
    echo ""
    echo "Usage: $0 --option"
    echo ""
    echo "Options:"
    echo "  --flac      update listening test to use flac"
    echo "  --wav       update listening test to use wav"
    echo "  --help      show this help message"
    exit 0
}

# Input parameter
[ "$#" -eq 1 ] || usage  # exactly one parameter required
case "$1" in
    --flac) FORMATSTR='s/.wav/.flac/g';;
    --wav)  FORMATSTR='s/.flac/.wav/g';;
    *) usage;;
esac

# Exit if any command fails
set -e

# Update config files
if $CONFIG; then
    for FILE in "interferer.yaml" "quality.yaml" "training_interferer.yaml" "training_quality.yaml" "quality_familiarisation.yaml" "interference_familiarisation.yaml"; do
        sed -i ''$FORMATSTR'' "site/_data/$FILE"
    done
fi
