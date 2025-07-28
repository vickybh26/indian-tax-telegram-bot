# Railway Connection Guide

## Step 1: Sign Up for Railway

1. **Go to https://railway.app**
2. **Click "Login"** in the top-right corner
3. **Sign up with GitHub** (recommended) - this makes connecting repositories easier
4. **Verify your account** if required

## Step 2: Create New Project

1. **Click "New Project"** on Railway dashboard
2. **Select "Deploy from GitHub repo"**
3. **Choose your repository:** `indian-tax-telegram-bot`
4. **Click "Deploy Now"**

Railway will automatically:
- Detect it's a Python project
- Install dependencies from `requirements.txt`
- Use the start command from `railway.json`

## Step 3: Configure Environment Variables

**CRITICAL STEP** - Your bot won't work without these:

1. **In Railway dashboard, click on your project**
2. **Click "Variables" tab**
3. **Add these two variables:**

```
Variable Name: TELEGRAM_BOT_TOKEN
Value: [Paste your Telegram bot token here]

Variable Name: GEMINI_API_KEY  
Value: [Paste your Gemini API key here]
```

4. **Click "Add" for each variable**

## Step 4: Monitor Deployment

1. **Click "Deployments" tab** to see build progress
2. **Watch the logs** - you should see:
   ```
   Installing dependencies...
   Starting application...
   Bot is running. Press Ctrl+C to stop.
   ```
3. **Success!** Your bot is now live 24/7

## Step 5: Get Your Railway URL (Optional)

Railway will provide a URL for your service, but since this is a Telegram bot (not a web app), you don't need the URL. The bot communicates directly with Telegram's servers.

## Troubleshooting

**Build Failed:**
- Check if all files uploaded correctly to GitHub
- Verify `requirements.txt` exists and is valid

**Bot Not Responding:**
- Make sure environment variables are set correctly
- Check deployment logs for error messages
- Verify your Telegram bot token is valid

**Need to Update Code:**
- Push changes to your GitHub repository
- Railway will automatically redeploy

## Usage Monitoring

- **Check Railway dashboard** for resource usage
- **Monitor costs** - should stay within $5 free tier
- **View logs** for debugging and monitoring user interactions

Your bot is now running 24/7 on Railway!