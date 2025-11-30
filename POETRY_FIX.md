# Fixing Poetry Detection Issue on Render

## Problem
Render is detecting Poetry and trying to use it, but your project uses `requirements.txt` with pip.

## Solution

### Option 1: Set Environment Variable in Render Dashboard (Recommended)

1. Go to your Render dashboard
2. Navigate to your web service
3. Go to **"Environment"** tab
4. Add a new environment variable:
   - **Key**: `POETRY_VENV_PATH`
   - **Value**: (leave empty or set to empty string)
5. Save changes and redeploy

This tells Render not to use Poetry.

### Option 2: Remove Poetry Files from Repository (If Any)

Check your GitHub repository root for:
- `pyproject.toml` (Poetry config file)
- `poetry.lock` (Poetry lock file)

If these exist and you don't need Poetry, delete them:
```bash
git rm pyproject.toml poetry.lock
git commit -m "Remove Poetry files, using requirements.txt instead"
git push origin main
```

### Option 3: Ensure build.sh is Used

Make sure in Render dashboard:
- **Build Command**: `./build.sh`
- NOT `poetry install` or any Poetry command

## Verify

After making changes, check the build logs:
- Should see: "Installing Python version..."
- Should see: "pip install -r requirements.txt"
- Should NOT see: "Using Poetry version..."

## Updated Files

I've already updated:
- ✅ `build.sh` - Explicitly disables Poetry
- ✅ `runtime.txt` - Specifies Python version (3.11.0)
- ✅ `render.yaml` - Removed Poetry-related config

## Quick Fix in Render Dashboard

**Fastest solution:** Add this environment variable in Render:
- Name: `POETRY_VENV_PATH`
- Value: (empty/blank)

This will disable Poetry detection immediately.

