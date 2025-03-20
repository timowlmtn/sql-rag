#!/bin/bash

# Define paths
export HOME_PATH="/Users/timburns/PycharmProjects/OwlMountain/azrius-analytics"
export LOG_PATH=$HOME_PATH
export VENV_PATH="${HOME_PATH}/azrius"
export SCRIPT_PATH="${HOME_PATH}/agent/server/query_server.py"

# Activate the virtual environment
source "${VENV_PATH}/bin/activate"
source ${VENV_PATH}/../setenv.sh

export PYTHONPATH="${HOME_PATH}/agent"

# Run the script
python "$SCRIPT_PATH"

# Deactivate the virtual environment
deactivate
