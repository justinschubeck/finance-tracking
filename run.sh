#!/bin/bash

activate_virtualenv() {
    if [ "$VIRTUAL_ENV" == "" ]; then
        source venv/Scripts/activate
    fi
}

activate_virtualenv
python3.11 main.py