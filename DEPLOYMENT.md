# Deployment Guide for Render

⚠️ **This project is now configured to use SQLite database.**

For SQLite deployment instructions, see **[DEPLOYMENT_SQLITE.md](DEPLOYMENT_SQLITE.md)** - it's much simpler!

If you need MySQL instead, you'll need to:
1. Add mysqlclient back to requirements.txt
2. Update settings.py to use MySQL
3. Set up an external MySQL database

---

# Legacy MySQL Deployment Guide (Deprecated - Using SQLite Now)

This guide is kept for reference but the project now uses SQLite by default.

## Prerequisites

1. A Render account (sign up at https://render.com)
2. Your project pushed to a Git repository (GitHub, GitLab, or Bitbucket)

## Step 1: Prepare Your Repository

Make sure all files are committed and pushed to your Git repository:
- `requirements.txt` (includes gunicorn and whitenoise)
- `build.sh` (build script)
- `render.yaml` (optional, for automated setup)
- Updated `settings.py` (uses environment variables)

## Step 2: Set Up MySQL Database

Since this project uses MySQL, you have a few options:

### Option A: External MySQL Service (Recommended)
Use an external MySQL provider such as:
- **PlanetScale** (https://planetscale.com) - Free tier available
- **AWS RDS MySQL** - Pay-as-you-go
- **DigitalOcean Managed MySQL** - Starting at $15/month
- **Railway MySQL** - Free tier available
- **Aiven MySQL** - Free tier available

After creating your MySQL database, note down:
- Database name
- Username
- Password
- Host (connection URL)
- Port (usually 3306)

### Option B: Convert to PostgreSQL (Alternative)
If you want to use Render's native PostgreSQL:
1. Install `psycopg2-binary` instead of `mysqlclient` in requirements.txt
2. Update `settings.py` to use PostgreSQL backend
3. Create a PostgreSQL database on Render

**For this guide, we'll assume you're using an external MySQL service (Option A).**

## Step 3: Create a Web Service

1. In Render dashboard, click "New +" → "Web Service"
2. Connect your Git repository
3. Configure the service:
   - **Name**: `autocare-django` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn autocare.wsgi:application`
   - **Root Directory**: `autocare` (if your project is in a subdirectory)

## Step 4: Configure Environment Variables

⚠️ **CRITICAL**: You MUST set these environment variables in the Render dashboard before deployment. The build will fail if database credentials are missing.

In your Render web service, go to **"Environment"** tab and click **"Add Environment Variable"** for each:

### Required Database Variables (MUST BE SET):
```
DB_HOST=<your-actual-mysql-host>
```
**Example**: `us-east.connect.psdb.cloud` (PlanetScale) or `your-db.123456789.us-east-1.rds.amazonaws.com` (AWS RDS)
**⚠️ DO NOT use placeholders like `<from-database-credentials>` - use actual values!**

```
DB_NAME=autocare_db
```
Your MySQL database name

```
DB_USER=<your-mysql-username>
```
Your MySQL username

```
DB_PASSWORD=<your-mysql-password>
```
Your MySQL password

```
DB_PORT=3306
```
MySQL port (usually 3306)

### Other Required Variables:
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
Replace with your actual Render domain

```
CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com
```
Replace with your actual Render domain (include `https://`)

```
CORS_ALLOW_ALL_ORIGINS=False
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_HTTPONLY=True
```

**See `RENDER_ENV_SETUP.md` for detailed step-by-step instructions with screenshots guidance.**

## Step 5: Link Database to Web Service

1. In your web service settings, go to "Connections"
2. Link your PostgreSQL database
3. Render will automatically set `DATABASE_URL` environment variable

## Step 6: Deploy

1. Click "Create Web Service" or "Save Changes"
2. Render will automatically:
   - Install dependencies from `requirements.txt`
   - Run `build.sh` (collects static files and runs migrations)
   - Start the application with gunicorn

## Step 7: Verify Deployment

1. Check the logs in Render dashboard for any errors
2. Visit your app URL (e.g., `https://your-app-name.onrender.com`)
3. Test the application functionality

## Troubleshooting

### Static Files Not Loading
- Ensure `whitenoise` is in `requirements.txt`
- Check that `STATIC_ROOT` is set in settings.py
- Verify `build.sh` runs `collectstatic`

### Database Connection Issues
- Verify database credentials in environment variables
- Check that database is in the same region as web service
- Ensure database is running

### Migration Errors
- Check logs for specific migration errors
- You may need to run migrations manually via Render shell

### Build Failures
- Check that `build.sh` has execute permissions
- Verify all dependencies are in `requirements.txt`
- Check Python version compatibility

## Using render.yaml (Alternative Method)

If you prefer automated setup:
1. Ensure `render.yaml` is in your repository root
2. In Render dashboard, click "New +" → "Blueprint"
3. Connect your repository
4. Render will automatically create services based on `render.yaml`

**Note:** You'll still need to manually configure database credentials in environment variables.

## Additional Notes

- Free tier services spin down after 15 minutes of inactivity
- Consider upgrading to paid tier for production use
- Set up automatic deployments from your main branch
- Monitor logs regularly for errors
- Keep your `SECRET_KEY` secure and never commit it to Git

## Support

For Render-specific issues, check:
- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com

