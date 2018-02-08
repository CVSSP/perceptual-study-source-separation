#!/bin/bash

usage() {
    echo ""
    echo "Usage: $0 [--help]"
    echo ""
    echo "Options:"
    echo "  --help      show this help message"
    exit 0
}

issubstring() {
    echo "$2" | grep -F "$1"
    return $?
}

wav2flac() {
    # Remove unneded wav files
    for FILE in $(find $1/Artefacts.wav -type f 2>/dev/null); do
        rm "$FILE"
    done
    for FILE in $(find $1/Distortion.wav -type f 2>/dev/null); do
        rm "$FILE"
    done
    for FILE in $(find $1/*.wav -type f); do
        # Skip unnneded files
        issubstring "Artefacts" "$FILE" && continue
        issubstring "Distortion" "$FILE" && continue
        # Otherwise convert to 16bit wav and flac
        sox "$FILE" -b 16 "$FILE.wav" gain -3
        flac --silent "$FILE.wav" > /dev/null
        mv "$FILE.flac" "${FILE%.wav}.flac"
        rm "$FILE.wav"
    done
}

# Input parameter
[ "$#" -gt 0 ] && usage  # no arg required

# Exit if any command fails
set -e

wav2flac 'site/sounds/*'
wav2flac 'site/sounds_training/*'
wav2flac 'site/sounds_familiarisation'
