# Deployment Guide for Render with SQLite

This guide will help you deploy the AutoCare Django project on Render using SQLite database.

## ⚠️ Important Note About SQLite on Render

**SQLite works on Render, but with limitations:**
- ✅ **Works great for:** Development, testing, small apps, demos
- ⚠️ **Limitations:** On Render's free tier, the database file is **ephemeral**
  - Data is lost when the service restarts or redeploys
  - Each deployment creates a fresh database
  - Fine for testing/demos, but not for production with persistent data

**For production with persistent data, consider:**
- Upgrading to Render's paid tier with persistent disk
- Using an external database (PostgreSQL, MySQL)
- Using Render's PostgreSQL database service

## Prerequisites

1. A Render account (sign up at https://render.com)
2. Your project pushed to a Git repository (GitHub, GitLab, or Bitbucket)

## Step 1: Prepare Your Repository

Make sure all files are committed and pushed to your Git repository:
- `requirements.txt` (no mysqlclient, uses SQLite)
- `build.sh` (build script)
- `render.yaml` (optional, for automated setup)
- Updated `settings.py` (configured for SQLite)

## Step 2: Create a Web Service on Render

1. Go to your Render dashboard: https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your Git repository
4. Configure the service:
   - **Name**: `autocare-django` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn autocare.wsgi:application`
   - **Root Directory**: `autocare` (if your project is in a subdirectory)

## Step 3: Configure Environment Variables

In your Render web service, go to **"Environment"** tab and add these variables:

### Required Variables:

```
SECRET_KEY=<generate-a-secure-random-key>
```
Generate one using:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

```
DEBUG=False
```

```
ALLOWED_HOSTS=your-app-name.onrender.com
```
Replace `your-app-name` with your actual Render service name.

```
CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com
```
Replace with your actual Render domain (include `https://`).

```
CORS_ALLOW_ALL_ORIGINS=False
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_HTTPONLY=True
```

### ✅ No Database Configuration Needed!
Since we're using SQLite, you don't need to configure any database credentials. SQLite will create `db.sqlite3` automatically.

## Step 4: Deploy

1. Click **"Create Web Service"** or **"Save Changes"**
2. Render will automatically:
   - Install dependencies from `requirements.txt`
   - Run `build.sh` (collects static files and runs migrations)
   - Create the SQLite database and run migrations
   - Start the application with gunicorn

## Step 5: Verify Deployment

1. Check the logs in Render dashboard for any errors
2. Visit your app URL (e.g., `https://your-app-name.onrender.com`)
3. Test the application functionality
4. Create a superuser if needed (via Render shell)

### Creating a Superuser

To create a Django admin superuser:

1. In Render dashboard, go to your service
2. Click on **"Shell"** tab
3. Run:
   ```bash
   python manage.py createsuperuser
   ```
4. Follow the prompts to create your admin user

## Using render.yaml (Alternative Method)

If you prefer automated setup:

1. Ensure `render.yaml` is in your repository root
2. In Render dashboard, click **"New +"** → **"Blueprint"**
3. Connect your repository
4. Render will automatically create services based on `render.yaml`

**Note:** You'll still need to manually set `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` with your actual domain after deployment.

## Troubleshooting

### Poetry Detection Error (Build Fails)

If you see errors about Poetry or "Collecting: command not found":

**Quick Fix:**
1. Go to Render dashboard → Your service → Environment tab
2. Add environment variable:
   - Key: `POETRY_VENV_PATH`
   - Value: (leave blank/empty)
3. Save and redeploy

**Alternative:**
Check your GitHub repository root for `pyproject.toml` or `poetry.lock` files. If they exist and you don't need Poetry:
- Delete them from your repository
- Commit and push the changes

See `POETRY_FIX.md` for detailed instructions.

### Static Files Not Loading
- ✅ WhiteNoise is already configured in `settings.py`
- Ensure `build.sh` runs `collectstatic`
- Check that `STATIC_ROOT` is set correctly

### Database Errors
- SQLite database is created automatically - no configuration needed
- If migrations fail, check the build logs
- Try running migrations manually via Render shell

### Build Failures
- Check that `build.sh` has execute permissions
- Verify all dependencies are in `requirements.txt`
- Check Python version compatibility (3.11.0 in render.yaml)

### Service Restarts
- Remember: SQLite database resets on service restarts (free tier)
- This is normal behavior - data is not persisted between restarts

## Migration from MySQL to SQLite

If you were previously using MySQL and want to migrate data:

1. Export data from MySQL:
   ```bash
   python manage.py dumpdata > data.json
   ```

2. Deploy with SQLite on Render

3. Load data into SQLite (via Render shell):
   ```bash
   python manage.py loaddata data.json
   ```

**Note:** Some MySQL-specific features might not work in SQLite. Test your app thoroughly.

## Best Practices

1. **For Development/Testing:** SQLite on Render free tier is perfect
2. **For Production:** Consider upgrading or using PostgreSQL
3. **Backup Strategy:** If using SQLite, regularly backup `db.sqlite3` file
4. **Environment Variables:** Never commit `SECRET_KEY` to Git
5. **Static Files:** WhiteNoise handles static files automatically

## Support

For Render-specific issues, check:
- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com
- Django SQLite Documentation: https://docs.djangoproject.com/en/stable/ref/databases/#sqlite-notes

---

**Enjoy your deployed Django app! 🚀**

