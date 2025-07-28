# Railway.app Deployment Guide

Follow these steps to deploy your Indian Income Tax Telegram Bot on Railway.app:

## Prerequisites

1. **GitHub Account** - Railway deploys from GitHub repositories
2. **Railway Account** - Sign up at https://railway.app
3. **API Keys Ready** - Your TELEGRAM_BOT_TOKEN and GEMINI_API_KEY

## Step-by-Step Deployment

### 1. Push Code to GitHub

1. Create a new repository on GitHub
2. Upload all your project files to the repository
3. Make sure these files are included:
   - `main.py` (entry point)
   - `requirements.txt` (dependencies)
   - `railway.json` (Railway configuration)
   - `Procfile` (process definition)
   - All your `bot/`, `services/`, `utils/`, `config/` folders

### 2. Deploy on Railway

1. Go to https://railway.app and sign in
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will automatically detect it's a Python project

### 3. Set Environment Variables

In Railway dashboard:
1. Go to your project
2. Click on "Variables" tab
3. Add these environment variables:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

### 4. Configure Deployment

Railway will automatically:
- Install dependencies from `requirements.txt`
- Use the start command from `railway.json`: `python main.py`
- Restart on failure (configured in `railway.json`)

### 5. Monitor Deployment

1. Check the "Deployments" tab for build logs
2. Look for "Bot is running" message in logs
3. Your bot should now be live 24/7!

## Troubleshooting

**Build Fails:**
- Check requirements.txt for correct dependencies
- Verify Python version compatibility

**Bot Not Responding:**
- Verify environment variables are set correctly
- Check deployment logs for errors
- Ensure TELEGRAM_BOT_TOKEN is valid

**Resource Usage:**
- Monitor usage in Railway dashboard
- Should stay well within $5 free tier for <1000 users/month

## Alternative: One-Click Deploy

You can also create a "Deploy to Railway" button by adding this to your GitHub README:

```markdown
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/YOUR_TEMPLATE_ID)
```

## Support

- Railway Documentation: https://docs.railway.app
- Railway Community: https://help.railway.app
- Check deployment logs for detailed error messages

Your bot will be accessible 24/7 once deployed successfully!