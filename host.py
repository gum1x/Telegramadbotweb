#!/usr/bin/env python3
"""
Hosting Script for Multi-Account Telegram Bot
Runs bots as a service with automatic restart and monitoring
"""

import os
import sys
import json
import asyncio
import logging
import signal
import time
from datetime import datetime
from typing import Dict, List
import subprocess
import psutil

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_host.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class BotHost:
    def __init__(self):
        self.running = False
        self.bot_processes: Dict[str, subprocess.Popen] = {}
        self.accounts_file = "assets/accounts.json"
        self.max_restarts = 5
        self.restart_delay = 30  # seconds
        
    def load_accounts(self) -> List[dict]:
        """Load accounts from JSON file"""
        try:
            if os.path.exists(self.accounts_file):
                with open(self.accounts_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading accounts: {e}")
            return []
    
    def start_single_bot(self, account: dict) -> subprocess.Popen:
        """Start a single bot process"""
        try:
            # Create environment variables for the bot
            env = os.environ.copy()
            env['TELEGRAM_PHONE'] = account['phone']
            env['TELEGRAM_API_ID'] = str(account['api_id'])
            env['TELEGRAM_API_HASH'] = account['api_hash']
            env['BOT_NAME'] = account.get('name', account['phone'])
            
            # Start the bot process
            process = subprocess.Popen(
                [sys.executable, 'main.py'],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            logger.info(f"Started bot for {account['phone']} (PID: {process.pid})")
            return process
            
        except Exception as e:
            logger.error(f"Failed to start bot for {account['phone']}: {e}")
            return None
    
    def stop_single_bot(self, phone: str):
        """Stop a single bot process"""
        if phone in self.bot_processes:
            process = self.bot_processes[phone]
            try:
                process.terminate()
                process.wait(timeout=10)
                logger.info(f"Stopped bot for {phone}")
            except subprocess.TimeoutExpired:
                process.kill()
                logger.warning(f"Force killed bot for {phone}")
            except Exception as e:
                logger.error(f"Error stopping bot for {phone}: {e}")
            finally:
                del self.bot_processes[phone]
    
    def start_all_bots(self):
        """Start all enabled bots"""
        accounts = self.load_accounts()
        enabled_accounts = [acc for acc in accounts if acc.get('enabled', True)]
        
        if not enabled_accounts:
            logger.warning("No enabled accounts found!")
            return
        
        logger.info(f"Starting {len(enabled_accounts)} bots...")
        
        for account in enabled_accounts:
            process = self.start_single_bot(account)
            if process:
                self.bot_processes[account['phone']] = process
    
    def stop_all_bots(self):
        """Stop all running bots"""
        logger.info("Stopping all bots...")
        for phone in list(self.bot_processes.keys()):
            self.stop_single_bot(phone)
    
    def monitor_bots(self):
        """Monitor and restart failed bots"""
        while self.running:
            try:
                for phone, process in list(self.bot_processes.items()):
                    if process.poll() is not None:
                        logger.warning(f"Bot {phone} has stopped (exit code: {process.returncode})")
                        
                        # Restart the bot
                        self.stop_single_bot(phone)
                        time.sleep(2)
                        
                        # Find the account and restart
                        accounts = self.load_accounts()
                        account = next((acc for acc in accounts if acc['phone'] == phone), None)
                        if account and account.get('enabled', True):
                            new_process = self.start_single_bot(account)
                            if new_process:
                                self.bot_processes[phone] = new_process
                                logger.info(f"Restarted bot for {phone}")
                
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                logger.error(f"Error in bot monitoring: {e}")
                time.sleep(30)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info("Received shutdown signal, stopping all bots...")
        self.running = False
        self.stop_all_bots()
        sys.exit(0)
    
    def run(self):
        """Main hosting function"""
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        logger.info("Starting Telegram Bot Host...")
        
        # Start all bots
        self.running = True
        self.start_all_bots()
        
        # Start monitoring
        try:
            self.monitor_bots()
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
        finally:
            self.stop_all_bots()
            logger.info("Bot host stopped")

def create_systemd_service():
    """Create a systemd service file for hosting"""
    service_content = """[Unit]
Description=Telegram Multi-Bot Host
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/path/to/Telegram-AdBot
ExecStart=/usr/bin/python3 /path/to/Telegram-AdBot/host.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""
    
    with open('telegram-bot-host.service', 'w') as f:
        f.write(service_content)
    
    print("Created systemd service file: telegram-bot-host.service")
    print("To install:")
    print("1. Edit the service file with your username and paths")
    print("2. sudo cp telegram-bot-host.service /etc/systemd/system/")
    print("3. sudo systemctl daemon-reload")
    print("4. sudo systemctl enable telegram-bot-host")
    print("5. sudo systemctl start telegram-bot-host")

def create_docker_compose():
    """Create a Docker Compose file for hosting"""
    docker_compose = """version: '3.8'

services:
  telegram-bot-host:
    build: .
    container_name: telegram-bot-host
    restart: unless-stopped
    volumes:
      - ./assets:/app/assets
      - ./logs:/app/logs
    environment:
      - PYTHONUNBUFFERED=1
    networks:
      - bot-network

networks:
  bot-network:
    driver: bridge
"""
    
    dockerfile = """FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p assets/sessions logs

# Run the host
CMD ["python", "host.py"]
"""
    
    with open('docker-compose.yml', 'w') as f:
        f.write(docker_compose)
    
    with open('Dockerfile', 'w') as f:
        f.write(dockerfile)
    
    print("Created Docker files:")
    print("- docker-compose.yml")
    print("- Dockerfile")
    print("\nTo run with Docker:")
    print("1. docker-compose up -d")
    print("2. docker-compose logs -f")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "systemd":
            create_systemd_service()
        elif sys.argv[1] == "docker":
            create_docker_compose()
        else:
            print("Usage: python host.py [systemd|docker]")
            print("  systemd - Create systemd service file")
            print("  docker  - Create Docker files")
            print("  (no args) - Run the host directly")
    else:
        # Run the host
        host = BotHost()
        host.run() 