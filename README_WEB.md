# Telegram AdBot Web Panel

A modern web-based Telegram bot for forwarding messages from channels to groups with an easy-to-use dashboard.

## Features

- 🌐 **Web Dashboard** - Beautiful, responsive web interface
- 📱 **Telegram Integration** - Connect and authenticate via web
- 📤 **Message Forwarding** - Forward messages from channels to groups
- 🔄 **Auto Forwarding** - Set up automatic forwarding with configurable intervals
- 👥 **Group Management** - View and manage your groups
- 📊 **Statistics** - Real-time statistics and monitoring
- 🚀 **Easy Deployment** - Docker support for easy deployment

## Quick Start

### 1. Prerequisites

- Python 3.8+ or Docker
- Telegram API credentials (get from https://my.telegram.org/apps)

### 2. Local Development

```bash
# Clone the repository
git clone <your-repo-url>
cd Telegram-AdBot

# Install dependencies
pip install -r requirements_web.txt

# Copy environment file
cp env.example .env

# Edit .env with your credentials
nano .env

# Run the web bot
python web_bot.py
```

### 3. Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -f Dockerfile.web -t telegram-adbot .
docker run -p 5000:5000 telegram-adbot
```

## Configuration

### Environment Variables

Copy `env.example` to `.env` and configure:

```bash
# Telegram API Credentials
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here
TELEGRAM_PHONE=your_phone_number_here

# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=production
PORT=5000

# Forwarding Configuration
SOURCE_CHANNEL=@your_source_channel
FORWARD_INTERVAL=3600  # seconds
SEND_DELAY=15  # seconds between forwards
```

### Web Interface Configuration

1. Open http://localhost:5000
2. Go to Configuration tab
3. Enter your Telegram credentials
4. Set source channel and forwarding settings
5. Save configuration

## Usage

### 1. Connect to Telegram

1. Go to the Dashboard
2. Click "Connect to Telegram"
3. Enter your phone number
4. Enter the verification code sent to your phone

### 2. Configure Forwarding

1. Go to Configuration tab
2. Set your source channel (e.g., @channel_name)
3. Configure forwarding interval and delays
4. Save configuration

### 3. Start Forwarding

1. Go to Dashboard
2. Click "Forward Message" to send once
3. Or click "Start Auto Forwarding" for continuous forwarding

### 4. Join Groups

1. Create a `groups.txt` file with group invite links
2. Go to Dashboard
3. Click "Join Groups" to automatically join

## File Structure

```
Telegram-AdBot/
├── web_bot.py              # Main web application
├── requirements_web.txt     # Python dependencies
├── Dockerfile.web          # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── templates/              # HTML templates
│   ├── base.html
│   ├── index.html
│   └── config.html
├── static/                 # Static assets
│   ├── css/style.css
│   └── js/app.js
├── assets/                 # Data directory
│   ├── sessions/           # Telegram sessions
│   ├── config.json         # Configuration file
│   └── groups.txt          # Group invite links
└── README_WEB.md          # This file
```

## API Endpoints

- `GET /` - Main dashboard
- `GET /config` - Configuration page
- `POST /api/connect` - Connect to Telegram
- `POST /api/authenticate` - Authenticate with code
- `GET /api/groups` - Get user's groups
- `GET /api/channels` - Get user's channels
- `POST /api/forward` - Forward message manually
- `POST /api/join-groups` - Join groups from file
- `POST /api/start-forwarding` - Start auto forwarding
- `POST /api/stop-forwarding` - Stop auto forwarding
- `GET /api/stats` - Get statistics

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install -r requirements_web.txt
   ```

2. **Telegram Connection Issues**
   - Verify API credentials
   - Check phone number format (+1234567890)
   - Ensure you're not rate limited

3. **Permission Errors**
   ```bash
   chmod 755 assets/
   chmod 644 config.json
   ```

4. **Docker Issues**
   ```bash
   docker-compose down
   docker-compose up --build
   ```

5. **Port Already in Use**
   ```bash
   # Change port in .env
   PORT=5001
   ```

### Logs

Check logs for debugging:

```bash
# Local
python web_bot.py

# Docker
docker-compose logs -f telegram-adbot
```

### Health Check

The application includes a health check endpoint:

```bash
curl http://localhost:5000/api/stats
```

## Security Considerations

1. **Change Default Secret Key**
   ```bash
   SECRET_KEY=your-very-secure-random-key
   ```

2. **Use HTTPS in Production**
   - Set up reverse proxy (nginx)
   - Use SSL certificates

3. **Environment Variables**
   - Never commit `.env` files
   - Use secure secret management

4. **File Permissions**
   - Restrict access to sensitive files
   - Use non-root user in Docker

## Production Deployment

### Using Docker Compose

```bash
# Production deployment
docker-compose -f docker-compose.yml up -d

# With custom environment
SECRET_KEY=your-secret docker-compose up -d
```

### Using Gunicorn (Alternative)

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -k gevent -b 0.0.0.0:5000 web_bot:app
```

### Reverse Proxy Setup (Nginx)

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs
3. Create an issue on GitHub 