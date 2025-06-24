# Telegram AdBot - Back4App Deployment Guide

This guide will help you deploy your Telegram AdBot to Back4App for automated message forwarding.

## Features

- ✅ Automatically forwards messages from a specified channel to all your groups
- ✅ Runs continuously with 1-hour intervals (configurable)
- ✅ Rate limiting to avoid Telegram restrictions
- ✅ Persistent sessions for automatic reconnection
- ✅ Comprehensive logging
- ✅ Docker-based deployment

## Prerequisites

1. **Telegram API Credentials**
   - Get your API ID and API Hash from [my.telegram.org/auth](https://my.telegram.org/auth)
   - You'll need your phone number

2. **Back4App Account**
   - Your Back4App credentials (already provided):
     - App ID: `kDilA3yEbpOrsgnoVyv6NVtuPVC9hULUkYahSVsq`
     - Master Key: `SQiIu8WH7NdkfDqUr1om639FpWRQ7wSqFaIVyuvl`

3. **Source Channel**
   - The channel username you want to forward messages from (e.g., `@your_channel`)

## Step 1: Local Setup & Authentication

Before deploying to Back4App, you need to authenticate locally first:

1. **Clone your repository locally**
   ```bash
   git clone <your-repo-url>
   cd Telegram-AdBot
   ```

2. **Create your config file**
   ```bash
   cp assets/config.example.toml assets/config.toml
   ```

3. **Edit the config file** with your credentials:
   ```toml
   [telegram]
   phone_number = "+1234567890"
   api_id = 12345678
   api_hash = "your_api_hash_here"

   [forwarding]
   source_channel = "@your_channel"
   forward_interval = 3600  # 1 hour in seconds
   send_delay = 2
   ```

4. **Run the bot locally once to authenticate**
   ```bash
   python main.py
   ```
   - Follow the prompts to enter verification code
   - This will create a session file that will be used for Back4App

## Step 2: Prepare for Back4App Deployment

1. **Create a GitHub repository** (if you haven't already)
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Back4App deployment"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Make sure these files are in your repository:**
   - `auto_forward.py` (automated forwarding script)
   - `Dockerfile` (container configuration)
   - `docker-compose.yml` (optional, for local testing)
   - `requirements.txt` (Python dependencies)
   - `assets/config.toml` (with your credentials)
   - `assets/sessions/` (with your authenticated session)

## Step 3: Deploy to Back4App

### Option A: Using Back4App Dashboard

1. **Login to Back4App**
   - Go to [back4app.com](https://back4app.com)
   - Login with your account

2. **Create a new app or use existing**
   - Use your existing app with ID: `kDilA3yEbpOrsgnoVyv6NVtuPVC9hULUkYahSVsq`

3. **Connect GitHub Repository**
   - Go to "Hosting" → "GitHub"
   - Connect your GitHub account
   - Select your repository

4. **Configure Environment Variables**
   - Go to "Settings" → "Environment Variables"
   - Add these variables:
     ```
     TELEGRAM_PHONE=+1234567890
     TELEGRAM_API_ID=12345678
     TELEGRAM_API_HASH=your_api_hash_here
     SOURCE_CHANNEL=@your_channel
     FORWARD_INTERVAL=3600
     SEND_DELAY=2
     ```

5. **Deploy**
   - Click "Deploy" to start the build process
   - Wait for the deployment to complete

### Option B: Using Back4App CLI

1. **Install Back4App CLI**
   ```bash
   npm install -g back4app-cli
   ```

2. **Login to Back4App**
   ```bash
   back4app login
   ```

3. **Deploy your app**
   ```bash
   back4app deploy
   ```

## Step 4: Monitor Your Bot

1. **Check Logs**
   - Go to Back4App Dashboard → "Logs"
   - Look for your bot's logs
   - You should see messages like:
     ```
     Connected as @your_username
     Source channel: Your Channel Name
     Found 25 groups
     Bot is running. Press Ctrl+C to stop.
     ```

2. **Test the Bot**
   - Send a message to your source channel
   - Wait for the next forwarding cycle (up to 1 hour)
   - Check if the message was forwarded to your groups

## Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TELEGRAM_PHONE` | Your phone number | Required |
| `TELEGRAM_API_ID` | Telegram API ID | Required |
| `TELEGRAM_API_HASH` | Telegram API Hash | Required |
| `SOURCE_CHANNEL` | Channel to forward from | `@your_channel` |
| `FORWARD_INTERVAL` | Seconds between checks | `3600` (1 hour) |
| `SEND_DELAY` | Delay between forwards | `2` seconds |

### Customizing Forwarding Interval

To change how often the bot forwards messages:

- **Every 30 minutes**: Set `FORWARD_INTERVAL=1800`
- **Every 2 hours**: Set `FORWARD_INTERVAL=7200`
- **Every 6 hours**: Set `FORWARD_INTERVAL=21600`

## Troubleshooting

### Common Issues

1. **"Not authorized" error**
   - Run the bot locally first to authenticate
   - Make sure the session file is included in your deployment

2. **"Source channel not found" error**
   - Check that the channel username is correct
   - Make sure you're a member of the channel

3. **"No groups found" error**
   - The bot only forwards to groups, not channels
   - Make sure you're a member of the groups

4. **Rate limiting issues**
   - Increase `SEND_DELAY` to 5-10 seconds
   - Reduce the number of groups if needed

### Logs and Debugging

- Check Back4App logs for detailed error messages
- The bot logs all activities to `bot.log`
- Use Back4App's real-time logs feature for live monitoring

## Security Notes

- Never commit your `assets/config.toml` file with real credentials
- Use environment variables in production
- Keep your API credentials secure
- Regularly rotate your API keys

## Support

If you encounter issues:

1. Check the logs in Back4App dashboard
2. Verify your Telegram credentials
3. Test locally first before deploying
4. Check that your session file is properly created

## License

This project is licensed under the same license as the original Telegram-AdBot project. 