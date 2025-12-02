#!/usr/bin/env bash
# exit on error
set -o errexit

# Explicitly disable Poetry completely
export POETRY_VENV_PATH=""
export SKIP_POETRY_INSTALL=true
export PIP_USE_PEP517=false
unset POETRY

# Ensure we're in the right directory (autocare folder)
if [ -f "manage.py" ]; then
    echo "Already in project root"
else
    echo "Changing to autocare directory"
    cd autocare || exit 1
fi

# Install dependencies using pip (not Poetry)
echo "Installing dependencies with pip..."
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Run migrations (SQLite database - no external setup needed)
echo "Running migrations..."
python manage.py migrate

