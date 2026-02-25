# Google OAuth Setup Guide

## Overview
This guide will help you set up Google OAuth (Continue with Google) login for your FoodHub restaurant website. The setup has been partially configured in Django. Now you need to create Google OAuth credentials.

## Prerequisites
- Google Account
- Access to Google Cloud Console
- Running Django development server

## Step 1: Create Google OAuth Credentials

### 1.1 Go to Google Cloud Console
1. Visit [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project (if you don't have one):
   - Click "Select a Project" dropdown at the top
   - Click "NEW PROJECT"
   - Enter project name: "FoodHub Restaurant"
   - Click "CREATE"

### 1.2 Enable Google+ API
1. In the Google Cloud Console, search for "Google+ API"
2. Click on "Google+ API"
3. Click the "ENABLE" button

### 1.3 Create OAuth 2.0 Credentials
1. Click on "Credentials" in the left sidebar
2. Click "Create Credentials" → "OAuth client ID"
3. Select "Web application"
4. In the "Authorized JavaScript origins" section, add:
   ```
   http://127.0.0.1:8000
   http://localhost:8000
   ```
5. In the "Authorized redirect URIs" section, add:
   ```
   http://127.0.0.1:8000/accounts/google/login/callback/
   http://localhost:8000/accounts/google/login/callback/
   ```
6. Click "CREATE"
7. Copy your Client ID and Client Secret
   - You'll use these in the next steps

## Step 2: Configure Django Admin

### 2.1 Start the Development Server
If not already running, start the server:
```bash
python manage.py runserver
```

### 2.2 Access Django Admin
1. Go to `http://127.0.0.1:8000/admin/`
2. Login with:
   - Username: `admin`
   - Password: `admin123`

### 2.3 Add Google OAuth Provider
1. In Django admin, go to **Sites** (if not visible, enable it in settings)
2. Click on the existing site
3. Ensure:
   - Domain name: `127.0.0.1:8000` (for development)
   - Display name: `FoodHub Restaurant`
   - Click "SAVE"

### 2.4 Add Google Social Application
1. In Django admin, look for **Social Applications** (under Sites)
2. Click "Add Social Application"
3. Fill in the form:
   - **Provider**: Select "Google" from dropdown
   - **Name**: `Google OAuth`
   - **Client id**: Paste your Google Client ID
   - **Secret key**: Paste your Google Client Secret
   - **Sites**: Select "127.0.0.1:8000"
4. Click "SAVE"

## Step 3: Test Google Login

### 3.1 Test Login Page
1. Go to `http://127.0.0.1:8000/login/`
2. You should see the "Continue with Google" button
3. Click it - you should be redirected to Google login
4. After authentication, you should be redirected back to the website

## Step 4: Production Configuration

### 4.1 Update URLs for Production
When deploying to production, update your authorized URLs in Google Cloud Console:

For example, if your domain is `www.yourdomain.com`:
- Authorized JavaScript origins:
  ```
  https://www.yourdomain.com
  https://yourdomain.com
  ```
- Authorized redirect URIs:
  ```
  https://www.yourdomain.com/accounts/google/login/callback/
  https://yourdomain.com/accounts/google/login/callback/
  ```

### 4.2 Update Django Settings for Production
In `Respro/settings.py`, update ALLOWED_HOSTS:
```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

### 4.3 Create Social Application for Production
In Django admin, create another social application with your production domain.

## Troubleshooting

### Issue: "Redirect URI mismatch" error
**Solution**: Ensure the redirect URI in Google Cloud Console matches exactly:
- Check for trailing slashes
- Match the domain name (127.0.0.1:8000, localhost:8000, or yourdomain.com)
- Verify the path: `/accounts/google/login/callback/`

### Issue: "Social application not found" error
**Solution**: 
1. Go to Django admin → Social Applications
2. Verify a Google OAuth app is created
3. Ensure sites are properly configured in Sites section

### Issue: Users not created automatically
**Solution**: Check settings in `Respro/settings.py`:
```python
SOCIALACCOUNT_AUTO_SIGNUP = True
```
This is already set, so it should auto-create users on first Google login.

## Features

- ✅ Google OAuth 2.0 login
- ✅ Automatic user account creation
- ✅ Profile data import from Google (name, email)
- ✅ Option to link existing account with Google
- ✅ Works alongside traditional username/password login

## File Changes Made

1. **Respro/settings.py**:
   - Added allauth apps to INSTALLED_APPS
   - Added django.contrib.sites
   - Updated context processors
   - Added authentication backends
   - Configured Google OAuth provider settings

2. **Respro/urls.py**:
   - Added `path('accounts/', include('allauth.urls'))`

3. **Template/login.html**:
   - Added Google sign-in button
   - Added "OR" divider
   - Included allauth template loader

4. **requirements.txt**:
   - Added `django-allauth==0.65.3`

## Next Steps

1. Get Google OAuth credentials from Google Cloud Console
2. Configure Django admin with the credentials
3. Test the login flow
4. Deploy to production with updated URLs

For more information about django-allauth, visit: https://django-allauth.readthedocs.io/
