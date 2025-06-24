#!/usr/bin/env python3
"""
Simplified Telegram AdBot with Web Panel
Features:
- Web interface for easy control
- Forward messages from channels to groups
- Auto-join groups
- Statistics dashboard
- Simple configuration
"""

import os
import json
import asyncio
import threading
import time
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_socketio import SocketIO, emit
from telethon import TelegramClient, errors, functions
from telethon.sessions import StringSession
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Flask app setup
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'
socketio = SocketIO(app, cors_allowed_origins="*")

class TelegramWebBot:
    def __init__(self):
        self.client = None
        self.user = None
        self.is_running = False
        self.stats = {
            'messages_forwarded': 0,
            'groups_joined': 0,
            'errors': 0,
            'last_forward': None,
            'start_time': None
        }
        self.config = self.load_config()
        self.forwarding_task = None
        
    def load_config(self):
        """Load configuration from JSON file"""
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r') as f:
                    return json.load(f)
            else:
                # Create default config
                default_config = {
                    'telegram': {
                        'phone': '',
                        'api_id': '',
                        'api_hash': ''
                    },
                    'forwarding': {
                        'source_channel': '',
                        'enabled': False,
                        'interval': 3600,  # 1 hour
                        'delay': 15
                    },
                    'auto_join': {
                        'enabled': False,
                        'delay': 30
                    }
                }
                with open('config.json', 'w') as f:
                    json.dump(default_config, f, indent=2)
                return default_config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {}
    
    def save_config(self):
        """Save configuration to JSON file"""
        try:
            with open('config.json', 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving config: {e}")
            return False
    
    async def connect(self):
        """Connect to Telegram"""
        try:
            if not self.config['telegram']['phone'] or not self.config['telegram']['api_id'] or not self.config['telegram']['api_hash']:
                return False, "Please configure Telegram credentials first"
            
            self.client = TelegramClient(
                StringSession(),
                int(self.config['telegram']['api_id']),
                self.config['telegram']['api_hash']
            )
            
            await self.client.connect()
            
            if not await self.client.is_user_authorized():
                return False, "Not authorized. Please authenticate first."
            
            self.user = await self.client.get_me()
            return True, f"Connected as @{self.user.username}"
            
        except Exception as e:
            return False, f"Connection failed: {e}"
    
    async def authenticate(self, phone, code):
        """Authenticate with phone and code"""
        try:
            if not self.client:
                return False, "Client not initialized"
            
            await self.client.send_code_request(phone)
            await self.client.sign_in(phone, code)
            self.user = await self.client.get_me()
            return True, f"Authenticated as @{self.user.username}"
            
        except errors.SessionPasswordNeededError:
            return False, "2FA password required"
        except Exception as e:
            return False, f"Authentication failed: {e}"
    
    async def get_groups(self):
        """Get all groups the user is in"""
        try:
            if not self.client:
                return []
            
            dialogs = await self.client.get_dialogs()
            groups = [d for d in dialogs if d.is_group and not d.is_channel]
            return [{'id': g.id, 'title': g.title} for g in groups]
            
        except Exception as e:
            logger.error(f"Error getting groups: {e}")
            return []
    
    async def get_channels(self):
        """Get all channels the user can access"""
        try:
            if not self.client:
                return []
            
            dialogs = await self.client.get_dialogs()
            channels = [d for d in dialogs if d.is_channel]
            return [{'id': c.id, 'title': c.title, 'username': getattr(c.entity, 'username', '')} for c in channels]
            
        except Exception as e:
            logger.error(f"Error getting channels: {e}")
            return []
    
    async def forward_message(self):
        """Forward latest message from source channel to all groups"""
        try:
            if not self.client or not self.config['forwarding']['source_channel']:
                return False, "No source channel configured"
            
            # Get source channel
            source_channel = await self.client.get_entity(self.config['forwarding']['source_channel'])
            
            # Get latest message
            async for message in self.client.iter_messages(source_channel, limit=1):
                if message and message.text:
                    # Get all groups
                    groups = await self.get_groups()
                    
                    if not groups:
                        return False, "No groups found"
                    
                    # Forward to all groups
                    success_count = 0
                    for group in groups:
                        try:
                            await self.client.forward_messages(group['id'], message)
                            success_count += 1
                            await asyncio.sleep(self.config['forwarding']['delay'])
                        except Exception as e:
                            logger.error(f"Failed to forward to {group['title']}: {e}")
                    
                    self.stats['messages_forwarded'] += success_count
                    self.stats['last_forward'] = datetime.now().isoformat()
                    
                    return True, f"Forwarded to {success_count}/{len(groups)} groups"
                else:
                    return False, "No text message found"
                    
        except Exception as e:
            self.stats['errors'] += 1
            return False, f"Forwarding failed: {e}"
    
    async def join_groups_from_file(self, filename='groups.txt'):
        """Join groups from a text file"""
        try:
            if not self.client:
                return False, "Not connected"
            
            if not os.path.exists(filename):
                return False, f"File {filename} not found"
            
            with open(filename, 'r') as f:
                links = [line.strip() for line in f if line.strip() and (line.startswith('http') or line.startswith('t.me/'))]
            
            if not links:
                return False, "No valid links found"
            
            joined_count = 0
            for i, link in enumerate(links[:10], 1):  # Limit to first 10
                try:
                    if 't.me/' in link:
                        hash_part = link.split('t.me/')[-1]
                    else:
                        hash_part = link.split('/')[-1]
                    
                    await self.client(functions.messages.ImportChatInviteRequest(hash=hash_part))
                    joined_count += 1
                    await asyncio.sleep(self.config['auto_join']['delay'])
                    
                except Exception as e:
                    logger.error(f"Failed to join {link}: {e}")
            
            self.stats['groups_joined'] += joined_count
            return True, f"Joined {joined_count} groups"
            
        except Exception as e:
            return False, f"Join groups failed: {e}"
    
    async def start_forwarding_loop(self):
        """Start the automatic forwarding loop"""
        self.is_running = True
        self.stats['start_time'] = datetime.now().isoformat()
        
        while self.is_running:
            try:
                if self.config['forwarding']['enabled']:
                    success, message = await self.forward_message()
                    if success:
                        logger.info(f"Forwarding successful: {message}")
                    else:
                        logger.error(f"Forwarding failed: {message}")
                
                # Wait for next cycle
                await asyncio.sleep(self.config['forwarding']['interval'])
                
            except Exception as e:
                logger.error(f"Error in forwarding loop: {e}")
                await asyncio.sleep(60)
    
    def stop_forwarding(self):
        """Stop the forwarding loop"""
        self.is_running = False
        if self.forwarding_task:
            self.forwarding_task.cancel()

# Global bot instance
bot = TelegramWebBot()

# Web routes
@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html', bot=bot)

@app.route('/config', methods=['GET', 'POST'])
def config():
    """Configuration page"""
    if request.method == 'POST':
        # Update config
        bot.config['telegram']['phone'] = request.form.get('phone', '')
        bot.config['telegram']['api_id'] = request.form.get('api_id', '')
        bot.config['telegram']['api_hash'] = request.form.get('api_hash', '')
        bot.config['forwarding']['source_channel'] = request.form.get('source_channel', '')
        bot.config['forwarding']['enabled'] = request.form.get('forwarding_enabled') == 'on'
        bot.config['forwarding']['interval'] = int(request.form.get('interval', 3600))
        bot.config['forwarding']['delay'] = int(request.form.get('delay', 15))
        bot.config['auto_join']['enabled'] = request.form.get('auto_join_enabled') == 'on'
        bot.config['auto_join']['delay'] = int(request.form.get('join_delay', 30))
        
        if bot.save_config():
            flash('Configuration saved successfully!', 'success')
        else:
            flash('Error saving configuration!', 'error')
        
        return redirect(url_for('config'))
    
    return render_template('config.html', bot=bot)

@app.route('/api/connect', methods=['POST'])
def api_connect():
    """API endpoint to connect to Telegram"""
    async def _connect():
        success, message = await bot.connect()
        return {'success': success, 'message': message}
    
    result = asyncio.run(_connect())
    return jsonify(result)

@app.route('/api/authenticate', methods=['POST'])
def api_authenticate():
    """API endpoint to authenticate"""
    data = request.get_json()
    phone = data.get('phone')
    code = data.get('code')
    
    async def _authenticate():
        success, message = await bot.authenticate(phone, code)
        return {'success': success, 'message': message}
    
    result = asyncio.run(_authenticate())
    return jsonify(result)

@app.route('/api/groups')
def api_groups():
    """API endpoint to get groups"""
    async def _get_groups():
        return await bot.get_groups()
    
    groups = asyncio.run(_get_groups())
    return jsonify(groups)

@app.route('/api/channels')
def api_channels():
    """API endpoint to get channels"""
    async def _get_channels():
        return await bot.get_channels()
    
    channels = asyncio.run(_get_channels())
    return jsonify(channels)

@app.route('/api/forward', methods=['POST'])
def api_forward():
    """API endpoint to forward message"""
    async def _forward():
        return await bot.forward_message()
    
    success, message = asyncio.run(_forward())
    return jsonify({'success': success, 'message': message})

@app.route('/api/join-groups', methods=['POST'])
def api_join_groups():
    """API endpoint to join groups"""
    async def _join_groups():
        return await bot.join_groups_from_file()
    
    success, message = asyncio.run(_join_groups())
    return jsonify({'success': success, 'message': message})

@app.route('/api/start-forwarding', methods=['POST'])
def api_start_forwarding():
    """API endpoint to start automatic forwarding"""
    if not bot.is_running:
        bot.forwarding_task = asyncio.create_task(bot.start_forwarding_loop())
        return jsonify({'success': True, 'message': 'Forwarding started'})
    else:
        return jsonify({'success': False, 'message': 'Forwarding already running'})

@app.route('/api/stop-forwarding', methods=['POST'])
def api_stop_forwarding():
    """API endpoint to stop automatic forwarding"""
    bot.stop_forwarding()
    return jsonify({'success': True, 'message': 'Forwarding stopped'})

@app.route('/api/stats')
def api_stats():
    """API endpoint to get statistics"""
    return jsonify(bot.stats)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True) 