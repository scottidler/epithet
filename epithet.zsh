#!/bin/zsh

if [ -n "$DEBUG" ]; then
    PS4=':${LINENO}+'
    set -x
fi

REAL_FILE="$0"
REAL_NAME="$(basename "$REAL_FILE")"
REAL_PATH="$(dirname "$REAL_FILE")"
if [ -L "$0" ]; then
    LINK_FILE=$REAL_FILE; REAL_FILE="$(readlink "$0")"
    LINK_NAME=$REAL_NAME; REAL_NAME="$(basename "$REAL_FILE")"
    LINK_PATH=$REAL_PATH; REAL_PATH="$(dirname "$REAL_FILE")"
fi
if [ -n "$VERBOSE" ]; then
    echo "REAL_FILE=$REAL_FILE"
    echo "REAL_NAME=$REAL_NAME"
    echo "REAL_PATH=$REAL_PATH"
    if [ -L "$0" ]; then
        echo "LINK_FILE=$LINK_FILE"
        echo "LINK_NAME=$LINK_NAME"
        echo "LINK_PATH=$LINK_PATH"
    fi
fi

# split string based on delimiter in shell https://stackoverflow.com/a/15988793
# ${VAR#*SUB}  # will drop begin of string up to first occur of `SUB`
# ${VAR##*SUB} # will drop begin of string up to last occur of `SUB`
# ${VAR%SUB*}  # will drop part of string from last occur of `SUB` to the end
# ${VAR%%SUB*} # will drop part of string from first occur of `SUB` to the end

echo "name: $0"
echo "args: $@"

