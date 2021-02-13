#!/bin/zsh

REAL_FILE="$0"
REAL_NAME="$(basename "$REAL_FILE")"
REAL_PATH="$(dirname "$REAL_FILE")"
if [ -L "$0" ]; then
    LINK_FILE=$REAL_FILE; REAL_FILE="$(readlink "$0")"
    LINK_NAME=$REAL_NAME; REAL_NAME="$(basename "$REAL_FILE")"
    LINK_PATH=$REAL_PATH; REAL_PATH="$(dirname "$REAL_FILE")"
fi
EPITHET_PY=$(realpath "$REAL_PATH/epithet.py")
if [ -n "$VERBOSE" ]; then
    echo "REAL_FILE=$REAL_FILE"
    echo "REAL_NAME=$REAL_NAME"
    echo "REAL_PATH=$REAL_PATH"
    if [ -L "$0" ]; then
        echo "LINK_FILE=$LINK_FILE"
        echo "LINK_NAME=$LINK_NAME"
        echo "LINK_PATH=$LINK_PATH"
    fi
    echo "EPITHET_PY=$EPITHET_PY"
fi

epithet-space() {
    if [ -n "$DEBUG" ]; then
        PS4=':${LINENO}+'
        set -x
    fi
    BUFFER="$(python3 $EPITHET_PY "$BUFFER")"
    zle end-of-line
    zle expand-word
    zle magic-space
}

epithet-accept-line() {
    if [ -n "$DEBUG" ]; then
        PS4=':${LINENO}+'
        set -x
    fi
    BUFFER="$(python3 $EPITHET_PY "$BUFFER")"
    zle .accept-line
}

zle -N epithet-space
zle -N accept-line epithet-accept-line

bindkey " " epithet-space
bindkey -M isearch " " magic-space
