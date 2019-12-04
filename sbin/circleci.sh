#!/bin/bash

set -e

BASEDIR=`dirname $0`

if [ -f "$BASEDIR/ci.sh" ]; then
    CISH="$BASEDIR/ci.sh"
elif [ ! -f /tmp/ci.sh ]; then
    curl -L https://raw.githubusercontent.com/SublimeText/UnitTesting/master/sbin/ci.sh -o /tmp/ci.sh
    CISH="/tmp/ci.sh"
fi

REPONAME="$CIRCLE_PROJECT_REPONAME"
PACKAGE=${PACKAGE:-$REPONAME}

. "$CISH"
