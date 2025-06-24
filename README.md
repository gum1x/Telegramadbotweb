# Telegram Ad Bot 🚀

<div align="center">

![Telegram Ad Bot](https://img.shields.io/badge/Telegram-Ad%20Bot-blue?style=for-the-badge&logo=telegram)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-2.0-blue?style=for-the-badge)

**Advanced Telegram Bot for Automated Message Forwarding and Group Management**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Support](#-support)

</div>

---

## ✨ Features

### 🎯 Core Features
- **📱 Single & Multi-Account Support** - Run one bot or manage multiple accounts simultaneously
- **🔄 Message Forwarding** - Automatically forward messages to multiple groups
- **🔗 Auto Group Joining** - Join groups with intelligent health checking
- **🛡️ Advanced Rate Limiting** - Smart rate limiting with exponential backoff
- **💾 Session Persistence** - Save login sessions for automatic reconnection
- **🎨 Beautiful Interface** - Rich terminal UI with panels and progress bars

### 🚀 Advanced Features
- **🏠 Hosting Mode** - Run as a service with auto-restart capabilities
- **📊 Real-time Statistics** - Track messages sent, groups joined, and errors
- **🔍 Health Checking** - Validate groups before joining (avoid banned/inactive groups)
- **⚙️ Easy Configuration** - Simple setup wizard and configuration management
- **🐳 Docker Support** - Containerized deployment options
- **📱 Systemd Integration** - Linux service management

### 🛡️ Safety Features
- **Rate Limiting** - Prevents getting banned by limiting requests
- **Error Recovery** - Handles network errors and retries automatically
- **Duplicate Prevention** - Skips groups where you recently sent messages
- **Session Management** - Secure session handling with StringSession

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/telegram-ad-bot.git
cd telegram-ad-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Launcher
```bash
python launcher.py
```

### 4. Follow the Setup Wizard
- Choose your bot mode (Single/Multi-Account)
- Configure your Telegram accounts
- Add groups to join
- Start using your bot!

## 📁 Project Structure

```
telegram-ad-bot/
├── launcher.py              # 🚀 Main launcher (start here!)
├── main.py                  # 📱 Single account bot
├── multi_bot.py             # 🤖 Multi-account manager
├── host.py                  # 🏠 Hosting script
├── test_bot.py              # 🧪 Test suite
├── setup.py                 # ⚙️ Setup script
├── requirements.txt         # 📦 Dependencies
├── README.md               # 📖 This file
├── README_MULTI.md         # 📚 Multi-account guide
├── LICENSE                 # 📄 MIT License
├── .gitignore              # 🚫 Git ignore rules
└── assets/
    ├── config.toml         # ⚙️ Single bot config
    ├── accounts.json       # 👥 Multi-account config
    ├── groups.txt          # 📋 Groups to join
    └── sessions/           # 💾 Saved sessions
```

## 🎯 Usage Modes

### 📱 Single Account Mode
Perfect for beginners or single account usage:
```bash
python launcher.py
# Choose option 1: Single Account Bot
```

### 🤖 Multi-Account Mode
Run multiple bots simultaneously:
```bash
python launcher.py
# Choose option 2: Multi-Account Bot Manager
```

### 🏠 Hosting Mode
Production deployment with auto-restart:
```bash
python launcher.py
# Choose option 3: Hosting Mode
```

## ⚙️ Configuration

### Single Bot Configuration (`assets/config.toml`)
```toml
[telegram]
phone_number = "+1234567890"
api_id = 12345678
api_hash = "your_api_hash_here"

[sending]
send_interval = 2
loop_interval = 300

[rate_limiting]
max_requests = 20
time_window = 60
max_backoff = 300

[health_check]
min_members = 10
max_members = 100000
max_inactive_days = 30
skip_channels = true
check_activity = true
```

### Multi-Account Configuration (`assets/accounts.json`)
```json
[
  {
    "phone": "+1234567890",
    "api_id": "12345678",
    "api_hash": "your_api_hash_here",
    "name": "Bot 1",
    "enabled": true
  }
]
```

## 🏠 Hosting Options

### 1. Direct Hosting
```bash
python host.py
```

### 2. Systemd Service (Linux)
```bash
python host.py systemd
# Follow the generated instructions
```

### 3. Docker Deployment
```bash
python host.py docker
docker-compose up -d
```

## 🧪 Testing

Run the test suite to verify everything works:
```bash
python test_bot.py
```

## 📊 Features Comparison

| Feature | Single Bot | Multi-Bot | Hosting Mode |
|---------|------------|-----------|--------------|
| Multiple Accounts | ❌ | ✅ | ✅ |
| Auto Restart | ❌ | ❌ | ✅ |
| Service Mode | ❌ | ❌ | ✅ |
| Easy Setup | ✅ | ✅ | ✅ |
| Dashboard | ✅ | ✅ | ❌ |
| Docker Support | ❌ | ❌ | ✅ |

## 🔧 Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Check your phone number format (+1234567890)
   - Verify API ID and Hash are correct
   - Get credentials from https://my.telegram.org/auth

2. **Rate Limited**
   - The bot automatically handles rate limits
   - Increase delays in config if needed
   - Reduce max_requests if getting banned

3. **Groups Not Joining**
   - Check invite links are valid
   - Some groups may require approval
   - Verify you're not already in the groups

### Debug Mode
```bash
python -u host.py 2>&1 | tee debug.log
```

## 📈 Performance Tips

1. **Start Small** - Begin with 2-3 accounts
2. **Monitor Resources** - Watch CPU/memory usage
3. **Gradual Scaling** - Add accounts gradually
4. **Use Hosting Mode** - For production deployment

### Resource Requirements
- **Per Bot**: ~50MB RAM, minimal CPU
- **10 Bots**: ~500MB RAM, moderate CPU
- **50+ Bots**: Consider dedicated server

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
```bash
git clone https://github.com/yourusername/telegram-ad-bot.git
cd telegram-ad-bot
pip install -r requirements.txt
python test_bot.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This bot is for educational purposes. Please:
- Respect Telegram's Terms of Service
- Don't spam or abuse groups
- Use reasonable delays between messages
- Be mindful of group rules and guidelines
- Monitor your bots' behavior

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/telegram-ad-bot&type=Date)](https://star-history.com/#yourusername/telegram-ad-bot&Date)

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/telegram-ad-bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/telegram-ad-bot/discussions)
- **Wiki**: [Documentation Wiki](https://github.com/yourusername/telegram-ad-bot/wiki)

---

<div align="center">

**Made with ❤️ for the Telegram community**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/telegram-ad-bot?style=social)](https://github.com/yourusername/telegram-ad-bot)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/telegram-ad-bot?style=social)](https://github.com/yourusername/telegram-ad-bot)
[![GitHub issues](https://img.shields.io/github/issues/yourusername/telegram-ad-bot)](https://github.com/yourusername/telegram-ad-bot/issues)

</div>
