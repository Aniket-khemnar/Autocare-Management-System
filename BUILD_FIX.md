# Fix for Build Error: Poetry Detection Issue

## Error You're Seeing
```
==> Using Poetry version 2.1.3 (default)
bash: line 1: Collecting: command not found
==> Build failed 😞
```

## Root Cause
Render is auto-detecting Poetry in your repository and trying to use it, but your project uses `requirements.txt` with pip.

## Quick Fix (Do This First!)

### Step 1: Set Environment Variable in Render Dashboard

1. Go to https://dashboard.render.com
2. Click on your web service (autocare-django)
3. Go to **"Environment"** tab
4. Click **"Add Environment Variable"**
5. Add:
   - **Key**: `POETRY_VENV_PATH`
   - **Value**: (leave it empty/blank - just press Enter)
6. Click **"Save Changes"**
7. Go to **"Events"** tab → **"Manual Deploy"** → **"Deploy latest commit"**

This will immediately disable Poetry detection.

### Step 2: Verify Build Command

In Render dashboard → Your service → Settings:
- **Build Command** should be: `./build.sh`
- **NOT** `poetry install` or any Poetry command

### Step 3: Check Repository Root

Check your GitHub repository (https://github.com/Aniket-khemnar/Autocare-Management-System) root for:
- `pyproject.toml` (Poetry config)
- `poetry.lock` (Poetry lock file)

If they exist and you don't need Poetry:

1. Delete them locally:
   ```bash
   cd autocare
   git rm pyproject.toml poetry.lock  # if they exist
   ```

2. Commit and push:
   ```bash
   git commit -m "Remove Poetry files, using requirements.txt"
   git push origin main
   ```

## Files I've Updated

I've already fixed these files:

✅ **`build.sh`** - Now explicitly disables Poetry  
✅ **`runtime.txt`** - Specifies Python version (3.11.0)  
✅ **`render.yaml`** - Cleaned up configuration  

## Verify It's Fixed

After setting the environment variable and redeploying, you should see in build logs:
```
==> Installing Python version 3.11.0...
==> Running build command './build.sh'...
[notice] A new release of pip is available...
pip install --upgrade pip
pip install -r requirements.txt
```

You should **NOT** see:
```
==> Using Poetry version...
```

## Still Not Working?

If the issue persists:

1. **Check Build Command**: Make absolutely sure it's `./build.sh` (with the `./`)
2. **Clear Build Cache**: In Render dashboard → Your service → Settings → Clear build cache
3. **Check Root Directory**: Make sure Root Directory is set correctly (probably `autocare` if your project is in a subdirectory)
4. **Try Manual Build**: Delete and recreate the service if needed

## Alternative: Use pip install directly

If `./build.sh` still doesn't work, you can set Build Command to:
```bash
pip install --upgrade pip && pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
```

But the environment variable fix should work!

## Summary

**Fastest Solution:**
1. Add `POETRY_VENV_PATH` environment variable (empty value) in Render
2. Save and redeploy
3. Done! ✅

The build should now work properly with pip instead of Poetry.

