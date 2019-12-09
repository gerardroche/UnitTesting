#! /usr/bin/env bash

set -e

while [ "$#" -ne 0 ]; do
    key="$1"
    case "$key" in
        --st)
            SUBLIME_TEXT_VERSION="$2"
            shift 2
            continue
        ;;
        --arch)
            SUBLIME_TEXT_ARCH="$2"
            shift 2
            continue
        ;;
        *)
            echo "Unknown option: $1"
            exit 1
        ;;
    esac
done

if [ -z $SUBLIME_TEXT_VERSION ]; then
    echo "Missing Sublime Text version"
    exit 1
fi

if [ -z $SUBLIME_TEXT_ARCH ]; then
    SUBLIME_TEXT_ARCH=x64
fi

STWEB="https://www.sublimetext.com/$SUBLIME_TEXT_VERSION"

if [ $(uname) = 'Darwin'  ]; then
    STP="$HOME/Library/Application Support/Sublime Text $SUBLIME_TEXT_VERSION/Packages"
    if [ -z $(which subl) ]; then
        if [ $SUBLIME_TEXT_VERSION -eq 2 ]; then
            SUBLIME_TEXT="Sublime Text 2"
        elif [ $SUBLIME_TEXT_VERSION -eq 3 ]; then
            SUBLIME_TEXT="Sublime Text"
        fi
        echo "installing sublime text $SUBLIME_TEXT_VERSION"
        for i in {1..20}; do
            URL=$(curl -L -s "$STWEB" | sed -n 's/.*href="\([^"]*\.dmg\)".*/\1/p')
            [ -n "$URL" ] && break || sleep 3
        done
        if [ -z "$URL" ]; then
            echo "could not download Sublime Text binary"
            exit 1
        fi
        echo "downloading $URL"
        for i in {1..20}; do
            curl -L "$URL" -o ~/Downloads/sublimetext.dmg && break || sleep 3
        done
        hdiutil attach ~/Downloads/sublimetext.dmg
        mkdir -p "$HOME/Applications"
        cp -r "/Volumes/$SUBLIME_TEXT/$SUBLIME_TEXT.app" "$HOME/Applications/$SUBLIME_TEXT.app"
        mkdir -p $HOME/.local/bin
        ln -s "$HOME/Applications/$SUBLIME_TEXT.app/Contents/SharedSupport/bin/subl" \
            $HOME/.local/bin/subl

        if [ ! -f "$STP/User/Preferences.sublime-settings" ]; then
            echo creating sublime package directory
            mkdir -p "$STP/User"
            # make sure a new window will be opened
            echo '{"close_windows_when_empty": false }' > "$STP/User/Preferences.sublime-settings"
        fi

        # make `subl` available
        open "$HOME/Applications/$SUBLIME_TEXT.app"
        sleep 2
        pkill '[Ss]ubl' || true
        pkill 'plugin_host' || true
        sleep 2
    fi
else
    STP="$HOME/.config/sublime-text-$SUBLIME_TEXT_VERSION/Packages"
    if [ -z $(which subl) ]; then
        if [ $SUBLIME_TEXT_VERSION -eq 2 ]; then
            SUBLIME_TEXT="Sublime Text 2"
        elif [ $SUBLIME_TEXT_VERSION -eq 3 ]; then
            SUBLIME_TEXT="sublime_text_3"
        fi
        echo "installing sublime text $SUBLIME_TEXT_VERSION"
        for i in {1..20}; do
            if [ "$SUBLIME_TEXT_ARCH" = "x64" ]; then
                URL=$(curl -s "$STWEB" | sed -n 's/.*href="\([^"]*x64\.tar\.bz2\)".*/\1/p')
            else
                URL=$(curl -s "$STWEB" | sed -n 's/.*href="\([^"]*x32\.tar\.bz2\)".*/\1/p')
            fi
            [ -n "$URL" ] && break || sleep 3
        done
        if [ -z "$URL" ]; then
            echo "could not download Sublime Text binary"
            exit 1
        fi
        echo "downloading $URL"
        for i in {1..20}; do
            curl "$URL" -o ~/sublimetext.tar.bz2 && break || sleep 3
        done
        tar jxf ~/sublimetext.tar.bz2 -C ~/
        mkdir -p $HOME/.local/bin
        ln -sf "$HOME/$SUBLIME_TEXT/sublime_text" $HOME/.local/bin/subl

        # make `subl` available
        "$HOME/$SUBLIME_TEXT/sublime_text" &
        sleep 2
        pkill '[Ss]ubl' || true
        pkill 'plugin_host' || true
        sleep 2
    fi
fi
