#!/usr/bin/env bash
# exit on error
set -o errexit

# Disable Poetry (Render auto-detects it)
unset POETRY_VENV_PATH
export POETRY_VENV_PATH=""
export PIP_DISABLE_PIP_VERSION_CHECK=1
export PIP_NO_CACHE_DIR=1

# Install dependencies using pip directly
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations (SQLite database - no external setup needed)
python manage.py migrate

