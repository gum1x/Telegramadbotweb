#!/usr/bin/env python3
"""
Automated Telegram Message Forwarding Bot for Back4App Hosting
Forwards messages from a specified channel to all groups every hour
"""

import os
import sys
import toml
import logging
import asyncio
import time
from datetime import datetime, timedelta
from typing import List, Optional
import json

from telethon import TelegramClient, errors
from telethon.sessions import StringSession

# Setup logging for Back4App
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutoForwardBot:
    def __init__(self):
        self.config = self.load_config()
        self.client = None
        self.user = None
        self.source_channel = None
        self.last_forwarded_message_id = None
        self.groups = []
        
    def load_config(self) -> dict:
        """Load configuration from TOML file or environment variables"""
        try:
            # Try to load from config file first
            if os.path.exists("assets/config.toml"):
                with open("assets/config.toml") as f:
                    return toml.loads(f.read())
            
            # Fallback to environment variables for Back4App
            return {
                'telegram': {
                    'phone_number': os.getenv('TELEGRAM_PHONE'),
                    'api_id': int(os.getenv('TELEGRAM_API_ID', 0)),
                    'api_hash': os.getenv('TELEGRAM_API_HASH')
                },
                'forwarding': {
                    'source_channel': os.getenv('SOURCE_CHANNEL', '@your_channel'),
                    'forward_interval': int(os.getenv('FORWARD_INTERVAL', 3600)),  # 1 hour default
                    'send_delay': int(os.getenv('SEND_DELAY', 2))
                }
            }
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            sys.exit(1)
    
    def load_groups(self) -> List[str]:
        """Load group invites from file"""
        try:
            if os.path.exists("assets/groups.txt"):
                with open("assets/groups.txt", encoding="utf-8") as f:
                    return [line.strip() for line in f if line.strip()]
            return []
        except Exception as e:
            logger.error(f"Error loading groups: {e}")
            return []
    
    async def connect(self):
        """Connect to Telegram with persistent session"""
        try:
            # Create sessions directory if it doesn't exist
            os.makedirs("assets/sessions", exist_ok=True)
            
            # Use phone number as session name for persistence
            session_name = f"assets/sessions/{self.config['telegram']['phone_number'].replace('+', '').replace(' ', '')}"
            
            self.client = TelegramClient(
                session_name,
                self.config["telegram"]["api_id"],
                self.config["telegram"]["api_hash"]
            )
            
            await self.client.connect()
            
            if not await self.client.is_user_authorized():
                logger.error("Not authorized! Please run the bot locally first to authenticate.")
                sys.exit(1)
            
            self.user = await self.client.get_me()
            logger.info(f"Connected as @{self.user.username}")
            
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            sys.exit(1)
    
    async def get_source_channel(self):
        """Get the source channel entity"""
        try:
            channel_username = self.config['forwarding']['source_channel']
            self.source_channel = await self.client.get_entity(channel_username)
            logger.info(f"Source channel: {self.source_channel.title}")
        except Exception as e:
            logger.error(f"Error getting source channel: {e}")
            sys.exit(1)
    
    async def get_all_groups(self):
        """Get all groups the user is a member of"""
        try:
            dialogs = await self.client.get_dialogs()
            self.groups = [d for d in dialogs if d.is_group and not d.is_channel]
            logger.info(f"Found {len(self.groups)} groups")
        except Exception as e:
            logger.error(f"Error getting groups: {e}")
    
    async def get_latest_message(self):
        """Get the latest message from the source channel"""
        try:
            async for message in self.client.iter_messages(self.source_channel, limit=1):
                if message and message.id != self.last_forwarded_message_id:
                    return message
            return None
        except Exception as e:
            logger.error(f"Error getting latest message: {e}")
            return None
    
    async def forward_to_groups(self, message):
        """Forward message to all groups"""
        if not message:
            logger.info("No new message to forward")
            return
        
        logger.info(f"Forwarding message {message.id} to {len(self.groups)} groups")
        
        success_count = 0
        error_count = 0
        
        for group in self.groups:
            try:
                await self.client.forward_messages(group, message)
                success_count += 1
                logger.info(f"Forwarded to {group.title}")
                
                # Rate limiting delay
                await asyncio.sleep(self.config['forwarding']['send_delay'])
                
            except Exception as e:
                error_count += 1
                logger.error(f"Failed to forward to {group.title}: {e}")
        
        self.last_forwarded_message_id = message.id
        logger.info(f"Forwarding complete: {success_count} success, {error_count} errors")
    
    async def run_forever(self):
        """Main loop that runs forever"""
        logger.info("Starting auto-forward bot...")
        
        await self.connect()
        await self.get_source_channel()
        await self.get_all_groups()
        
        logger.info("Bot is running. Press Ctrl+C to stop.")
        
        while True:
            try:
                # Get latest message
                message = await self.get_latest_message()
                
                if message:
                    await self.forward_to_groups(message)
                else:
                    logger.info("No new messages to forward")
                
                # Wait for next cycle
                interval = self.config['forwarding']['forward_interval']
                logger.info(f"Waiting {interval} seconds until next check...")
                await asyncio.sleep(interval)
                
            except KeyboardInterrupt:
                logger.info("Bot stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying
        
        await self.client.disconnect()

async def main():
    bot = AutoForwardBot()
    await bot.run_forever()

if __name__ == "__main__":
    asyncio.run(main()) 