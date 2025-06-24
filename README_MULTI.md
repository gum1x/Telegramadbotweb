# Telegram Multi-Account Bot System

A powerful multi-account Telegram bot system that can run multiple bots simultaneously with advanced hosting capabilities.

## 🚀 Features

### Multi-Account Management
- **Multiple Bots**: Run unlimited Telegram accounts simultaneously
- **Central Dashboard**: Manage all bots from one interface
- **Individual Control**: Start/stop bots individually or all at once
- **Account Management**: Add, remove, enable/disable accounts easily

### Advanced Hosting
- **Service Mode**: Run as a system service with auto-restart
- **Docker Support**: Containerized deployment
- **Process Monitoring**: Automatic restart of failed bots
- **Logging**: Comprehensive logging for all operations

### All Original Features
- **Message Forwarding**: Forward messages to multiple groups
- **Auto Group Joining**: Join groups with health checking
- **Rate Limiting**: Advanced rate limiting to avoid bans
- **Session Persistence**: Save login sessions
- **Health Checking**: Validate groups before joining

## 📁 File Structure

```
Telegram-AdBot/
├── main.py              # Single bot application
├── multi_bot.py         # Multi-account manager
├── host.py              # Hosting script
├── setup.py             # Setup script
├── requirements.txt     # Dependencies
├── README.md           # Original README
├── README_MULTI.md     # This file
└── assets/
    ├── config.toml     # Single bot config
    ├── accounts.json   # Multi-account config
    ├── groups.txt      # Groups to join
    └── sessions/       # Saved sessions
```

## 🎯 Usage Options

### 1. Single Bot (Original)
```bash
python main.py
```

### 2. Multi-Account Dashboard
```bash
python multi_bot.py
```

### 3. Hosting Mode
```bash
python host.py
```

## 🛠️ Setup

### Quick Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run setup
python setup.py

# Start multi-account system
python multi_bot.py
```

### Manual Account Setup
1. **Create accounts.json**:
```json
[
  {
    "phone": "+1234567890",
    "api_id": "12345678",
    "api_hash": "your_api_hash_here",
    "name": "Bot 1",
    "enabled": true,
    "created_at": "2024-01-01T00:00:00"
  },
  {
    "phone": "+0987654321",
    "api_id": "87654321",
    "api_hash": "another_api_hash",
    "name": "Bot 2",
    "enabled": true,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

2. **Add groups to groups.txt**:
```
https://t.me/group1
https://t.me/group2
@group3
```

## 🏠 Hosting Options

### 1. Direct Hosting
```bash
python host.py
```

### 2. Systemd Service (Linux)
```bash
# Create service file
python host.py systemd

# Edit the service file with your paths
sudo cp telegram-bot-host.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot-host
sudo systemctl start telegram-bot-host

# Check status
sudo systemctl status telegram-bot-host
sudo journalctl -u telegram-bot-host -f
```

### 3. Docker Deployment
```bash
# Create Docker files
python host.py docker

# Build and run
docker-compose up -d

# View logs
docker-compose logs -f
```

## 📊 Multi-Account Dashboard

The dashboard provides:

- **Account Status**: See which bots are running
- **Start/Stop Controls**: Manage all bots at once
- **Account Management**: Add/remove/enable accounts
- **Settings**: Configure global settings

### Dashboard Features:
- Real-time status monitoring
- Individual bot control
- Account management
- Settings configuration
- Session management

## 🔧 Configuration

### Global Settings (config.toml)
```toml
[sending]
send_interval = 2
loop_interval = 300

[rate_limiting]
max_requests = 20
time_window = 60
max_backoff = 300

[auto_join]
join_delay = 5
max_groups_per_session = 50

[health_check]
min_members = 10
max_members = 100000
max_inactive_days = 30
skip_channels = true
check_activity = true
```

### Account Settings (accounts.json)
Each account can have individual settings:
- Phone number
- API credentials
- Bot name
- Enabled/disabled status

## 🛡️ Safety Features

### Multi-Account Safety
- **Isolated Sessions**: Each bot has its own session
- **Independent Rate Limiting**: Each bot has separate rate limits
- **Error Isolation**: One bot's failure doesn't affect others
- **Graceful Shutdown**: Proper cleanup on exit

### Hosting Safety
- **Auto-restart**: Failed bots restart automatically
- **Process Monitoring**: Continuous health checking
- **Signal Handling**: Proper shutdown on system signals
- **Logging**: Comprehensive error tracking

## 📈 Scaling

### Performance Tips
1. **Start Small**: Begin with 2-3 accounts
2. **Monitor Resources**: Watch CPU/memory usage
3. **Gradual Scaling**: Add accounts gradually
4. **Use Hosting Mode**: For production deployment

### Resource Requirements
- **Per Bot**: ~50MB RAM, minimal CPU
- **10 Bots**: ~500MB RAM, moderate CPU
- **50+ Bots**: Consider dedicated server

## 🔍 Monitoring

### Logs
- **bot_host.log**: Hosting script logs
- **Console Output**: Real-time status
- **System Logs**: Service logs (systemd)

### Health Checks
- **Process Status**: Monitor running bots
- **Error Tracking**: Log all errors
- **Performance**: Track resource usage

## 🚨 Troubleshooting

### Common Issues

1. **Bot Not Starting**
   - Check API credentials
   - Verify phone number format
   - Check session files

2. **Rate Limiting**
   - Increase delays in config
   - Reduce max_requests
   - Use fewer accounts

3. **Hosting Issues**
   - Check file permissions
   - Verify Python path
   - Check system resources

### Debug Mode
```bash
# Run with verbose logging
python -u host.py 2>&1 | tee debug.log
```

## 📝 API Limits

### Telegram Limits
- **Messages**: 20 messages per minute
- **Joining**: 50 groups per day
- **Sessions**: Unlimited (with proper delays)

### Recommended Settings
- **Send Interval**: 3-5 seconds
- **Join Delay**: 5-10 seconds
- **Max Accounts**: 10-20 per IP

## 🔐 Security

### Best Practices
1. **Use Different IPs**: Avoid running too many bots on one IP
2. **Rotate Accounts**: Use different accounts for different purposes
3. **Monitor Activity**: Watch for unusual behavior
4. **Backup Sessions**: Keep session files safe

### Session Management
- Sessions are stored in `assets/sessions/`
- Each account has its own session file
- Sessions persist between restarts
- Can be cleared via settings

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.

## ⚠️ Disclaimer

This bot is for educational purposes. Please:
- Respect Telegram's Terms of Service
- Don't spam or abuse groups
- Use reasonable delays between messages
- Be mindful of group rules and guidelines
- Monitor your bots' behavior 