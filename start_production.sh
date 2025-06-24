#!/bin/bash

# Telegram AdBot Production Startup Script

set -e

echo "🚀 Starting Telegram AdBot in production mode..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "web_bot.py" ]; then
    echo "❌ web_bot.py not found. Please run this script from the project directory."
    exit 1
fi

# Set production environment variables
export FLASK_ENV=production
export FLASK_DEBUG=false
export PYTHONUNBUFFERED=1

# Set default port if not specified
export PORT=${PORT:-5000}

# Generate secret key if not set
if [ -z "$SECRET_KEY" ]; then
    export SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    echo "🔑 Generated new SECRET_KEY"
fi

# Check if config.json exists, create if not
if [ ! -f "config.json" ]; then
    echo "📝 Creating default config.json..."
    cat > config.json << EOF
{
  "telegram": {
    "phone": "",
    "api_id": "",
    "api_hash": ""
  },
  "forwarding": {
    "source_channel": "",
    "enabled": false,
    "interval": 3600,
    "delay": 15
  },
  "auto_join": {
    "enabled": false,
    "delay": 30
  }
}
EOF
fi

# Create necessary directories
mkdir -p assets/sessions
mkdir -p static/css static/js templates

# Check if requirements are installed
echo "🔍 Checking dependencies..."
python3 -c "import flask, telethon, gevent, flask_socketio" 2>/dev/null || {
    echo "📦 Installing dependencies..."
    pip3 install -r requirements_web.txt
}

# Run deployment test
echo "🧪 Running deployment tests..."
python3 test_deployment.py

if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Deployment tests failed. Please fix the issues above."
    exit 1
fi

# Start the application
echo "🌐 Starting web server on port $PORT..."
echo "📱 Open http://localhost:$PORT in your browser"
echo "🛑 Press Ctrl+C to stop"

# Run the application
exec python3 web_bot.py 