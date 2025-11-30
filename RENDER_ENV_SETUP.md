# Setting Environment Variables in Render Dashboard

## ⚠️ IMPORTANT: Database Configuration Required

Your build is failing because database environment variables are not set. You **MUST** configure these in the Render dashboard before deployment.

## Step-by-Step: Setting Environment Variables

1. **Go to your Render Dashboard**
   - Navigate to https://dashboard.render.com
   - Click on your web service (e.g., `autocare-django`)

2. **Open Environment Tab**
   - In the left sidebar, click on **"Environment"**

3. **Add Required Database Variables**
   Click **"Add Environment Variable"** for each of these:

   ### Required Database Variables:
   
   ```
   DB_HOST=<your-mysql-host>
   ```
   **⚠️ IMPORTANT: Enter ONLY the hostname, NO angle brackets!**
   
   **❌ WRONG Examples:**
   - `<127.0.0.1>`
   - `<us-east.connect.psdb.cloud>`
   - `<your-db.123456789.us-east-1.rds.amazonaws.com>`
   
   **✅ CORRECT Examples:**
   - `us-east.connect.psdb.cloud` (for PlanetScale)
   - `your-db.123456789.us-east-1.rds.amazonaws.com` (for AWS RDS)
   - `containers-us-west-123.railway.app` (for Railway)
   
   **⚠️ Note:** `127.0.0.1` or `localhost` will NOT work on Render! You need an external MySQL database.
   
   ```
   DB_NAME=<your-database-name>
   ```
   Example: `autocare_db`
   
   ```
   DB_USER=<your-database-username>
   ```
   Example: `autocare_user` or your MySQL username
   
   ```
   DB_PASSWORD=<your-database-password>
   ```
   Your MySQL database password
   
   ```
   DB_PORT=3306
   ```
   (Usually 3306 for MySQL - this may already be set)

4. **Add Other Required Variables**
   
   ```
   SECRET_KEY=<generate-a-secure-key>
   ```
   Generate one using:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   
   ```
   DEBUG=False
   ```
   
   ```
   ALLOWED_HOSTS=<your-render-domain>
   ```
   Example: `autocare-django.onrender.com`
   (Update this with your actual Render domain)
   
   ```
   CSRF_TRUSTED_ORIGINS=https://<your-render-domain>
   ```
   Example: `https://autocare-django.onrender.com`
   (Update this with your actual Render domain)
   
   ```
   CORS_ALLOW_ALL_ORIGINS=False
   ```
   
   ```
   CSRF_COOKIE_SECURE=True
   ```
   
   ```
   SESSION_COOKIE_SECURE=True
   ```
   
   ```
   CSRF_COOKIE_HTTPONLY=True
   ```

5. **Save Changes**
   - Click **"Save Changes"** at the bottom
   - Render will automatically trigger a new deployment

## Quick MySQL Database Setup Options

### Option 1: PlanetScale (Recommended - Free Tier Available)
1. Sign up at https://planetscale.com
2. Create a new database
3. Get connection details from the dashboard
4. Use the connection string values for your environment variables

### Option 2: Railway MySQL
1. Sign up at https://railway.app
2. Create a new MySQL service
3. Copy connection details from the service settings

### Option 3: AWS RDS MySQL
1. Create an RDS MySQL instance in AWS
2. Note the endpoint, database name, username, and password
3. Make sure security group allows connections from Render's IPs

## Verification

After setting environment variables:
1. Go to the **"Events"** tab in Render
2. Click **"Manual Deploy"** → **"Deploy latest commit"**
3. Check the build logs to ensure it succeeds
4. If migrations run successfully, your database is configured correctly

## Common Issues

### "Unknown server host" Error
- **Cause**: `DB_HOST` is not set or contains placeholder text
- **Fix**: Set `DB_HOST` to your actual MySQL server hostname (no `http://` or `https://`)

### "Access denied" Error
- **Cause**: Wrong username or password
- **Fix**: Double-check `DB_USER` and `DB_PASSWORD` match your database credentials

### "Unknown database" Error
- **Cause**: `DB_NAME` doesn't exist
- **Fix**: Create the database first, then set `DB_NAME` to match

### Build Still Fails
- Check that all environment variables are saved (not just typed)
- Ensure there are no extra spaces in variable values
- Verify your MySQL database is accessible from the internet (not localhost-only)

## Need Help?

If you're still having issues:
1. Check the build logs in Render for specific error messages
2. Verify your MySQL database is running and accessible
3. Test database connection locally first with the same credentials
4. Make sure your MySQL provider allows connections from Render's IP addresses

