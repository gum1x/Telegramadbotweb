# Telegram AdBot - Web Version

A simplified Telegram AdBot with a beautiful web interface for easy control and management.

## 🌟 Features

- **Web Dashboard**: Beautiful, responsive web interface
- **Easy Configuration**: Simple setup through web forms
- **Real-time Statistics**: Live updates of bot performance
- **One-click Actions**: Forward messages, join groups, start/stop automation
- **Authentication**: Built-in Telegram authentication flow
- **Group Management**: View and manage your groups and channels
- **Auto-forwarding**: Schedule automatic message forwarding
- **Mobile Friendly**: Works on all devices

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_web.txt
```

### 2. Run the Web Bot

```bash
python web_bot.py
```

### 3. Open Your Browser

Navigate to `http://localhost:5000`

## 📋 Setup Instructions

### Step 1: Get Telegram API Credentials

1. Go to [my.telegram.org/auth](https://my.telegram.org/auth)
2. Log in with your phone number
3. Click on "API development tools"
4. Create a new application
5. Copy the **API ID** and **API Hash**

### Step 2: Configure the Bot

1. Open the web interface at `http://localhost:5000`
2. Go to **Settings** tab
3. Enter your Telegram credentials:
   - Phone number
   - API ID
   - API Hash
4. Configure forwarding settings:
   - Source channel (e.g., `@your_channel`)
   - Forward interval (default: 1 hour)
   - Delay between forwards (default: 15 seconds)
5. Click **Save Configuration**

### Step 3: Authenticate

1. Go to **Dashboard**
2. Click **Connect to Telegram**
3. Enter your phone number
4. Enter the verification code sent to your phone
5. You're now connected!

### Step 4: Add Groups

Create a `groups.txt` file in the bot directory with one group invite link per line:

```
https://t.me/group1
https://t.me/group2
@group3
```

## 🎮 Using the Web Interface

### Dashboard

- **Connection Status**: Shows if you're connected to Telegram
- **Statistics**: Real-time stats of messages forwarded, groups joined, etc.
- **Quick Actions**: One-click buttons for common tasks
- **Groups & Channels**: View all your groups and available channels

### Quick Actions

- **Forward Now**: Manually forward the latest message from your source channel
- **Join Groups**: Automatically join groups from your `groups.txt` file
- **Start Auto Forward**: Begin automatic forwarding every hour
- **Stop Auto Forward**: Stop automatic forwarding

### Settings

- **Telegram Credentials**: Update your API credentials
- **Forwarding Settings**: Configure source channel and timing
- **Auto-join Settings**: Control group joining behavior

## 🔧 Configuration Options

### Forwarding Settings

| Setting | Description | Default |
|---------|-------------|---------|
| Source Channel | Channel to forward from | Required |
| Forward Interval | How often to check (seconds) | 3600 (1 hour) |
| Delay Between Forwards | Delay between groups (seconds) | 15 |

### Auto-join Settings

| Setting | Description | Default |
|---------|-------------|---------|
| Enable Auto-join | Automatically join groups | Off |
| Join Delay | Delay between joins (seconds) | 30 |

## 🐳 Docker Deployment

### Build and Run

```bash
# Build the Docker image
docker build -f Dockerfile.web -t telegram-adbot-web .

# Run the container
docker run -p 5000:5000 telegram-adbot-web
```

### Docker Compose

```yaml
version: '3.8'
services:
  telegram-adbot:
    build:
      context: .
      dockerfile: Dockerfile.web
    ports:
      - "5000:5000"
    volumes:
      - ./config.json:/app/config.json
      - ./groups.txt:/app/groups.txt
    restart: unless-stopped
```

## 🌐 Back4App Deployment

### 1. Prepare Your Repository

```bash
git add .
git commit -m "Add web interface"
git push
```

### 2. Deploy to Back4App

1. Go to [back4app.com](https://back4app.com)
2. Use your existing app: `kDilA3yEbpOrsgnoVyv6NVtuPVC9hULUkYahSVsq`
3. Connect your GitHub repository
4. Set environment variables:
   ```
   FLASK_APP=web_bot.py
   FLASK_ENV=production
   ```
5. Deploy using the Dockerfile.web

### 3. Access Your Bot

Your web interface will be available at your Back4App URL.

## 📱 Mobile Usage

The web interface is fully responsive and works great on mobile devices:

- **Dashboard**: View stats and control the bot
- **Settings**: Configure all options
- **Quick Actions**: One-tap forwarding and group joining

## 🔒 Security Features

- **Session Management**: Secure Telegram session handling
- **Input Validation**: All inputs are validated
- **Rate Limiting**: Built-in delays to avoid Telegram restrictions
- **Error Handling**: Comprehensive error handling and logging

## 🛠️ Troubleshooting

### Common Issues

1. **"Not authorized" error**
   - Make sure you've entered the correct credentials
   - Try re-authenticating through the web interface

2. **"No groups found"**
   - Join some groups manually first
   - Use the "Join Groups" button to auto-join from your list

3. **"Source channel not found"**
   - Check that the channel username is correct
   - Make sure you're a member of the channel

4. **Rate limiting issues**
   - Increase the delay between forwards
   - Reduce the number of groups

### Logs

Check the console output for detailed error messages and logs.

## 📊 Statistics

The dashboard shows real-time statistics:

- **Messages Forwarded**: Total messages sent to groups
- **Groups Joined**: Number of groups joined automatically
- **Errors**: Number of errors encountered
- **Last Forward**: When the last message was forwarded

## 🔄 API Endpoints

The web interface uses these API endpoints:

- `POST /api/connect` - Connect to Telegram
- `POST /api/authenticate` - Authenticate with code
- `GET /api/groups` - Get user's groups
- `GET /api/channels` - Get available channels
- `POST /api/forward` - Forward message manually
- `POST /api/join-groups` - Join groups from file
- `POST /api/start-forwarding` - Start auto-forwarding
- `POST /api/stop-forwarding` - Stop auto-forwarding
- `GET /api/stats` - Get statistics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the same license as the original Telegram-AdBot project.

## 🆘 Support

If you need help:

1. Check the troubleshooting section
2. Look at the console logs
3. Verify your configuration
4. Test with a simple setup first

---

**Enjoy your simplified Telegram AdBot with web interface! 🚀** 