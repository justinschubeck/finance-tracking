#!/bin/bash

# Name of virtual environment.
NAME=venv
if [ -d "$NAME" ]; then 
    echo "$NAME folder path already exists."
else
    # Create virtual environment.
    python3.11 -m venv $NAME

    # Activate virtual environment. 
    source $NAME/Scripts/activate

    # Upgrade pip.
    python3.11.exe -m pip install --upgrade pip

    # Install needed packages. 
    pip install -r requirements.txt
    
    # Deactivate virtual environment. 
    deactivate
fi

