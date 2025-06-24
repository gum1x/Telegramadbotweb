#!/usr/bin/env python3
"""
Setup script for Telegram Ad Bot
Helps users install dependencies and configure the bot
"""

import os
import sys
import subprocess
import toml

def print_banner():
    """Print the welcome banner"""
    banner = """
╔══════════════════════════════════════════╗
║           Telegram Ad Bot                ║
║         Setup & Configuration            ║
╚══════════════════════════════════════════╝
    """
    print(banner)

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies. Please install manually:")
        print("   pip install -r requirements.txt")
        return False

def create_config():
    """Create or update configuration file"""
    print("\n⚙️  Configuring your bot...")
    
    config_path = "assets/config.toml"
    
    # Check if config exists
    if os.path.exists(config_path):
        print("📁 Configuration file already exists.")
        update = input("Do you want to update it? (y/n): ").lower()
        if update != 'y':
            return True
    
    # Get user input
    print("\nPlease provide your Telegram API credentials:")
    print("Get them from: https://my.telegram.org/auth")
    print()
    
    phone = input("Phone number (e.g., +1234567890): ").strip()
    api_id = input("API ID: ").strip()
    api_hash = input("API Hash: ").strip()
    
    # Validate input
    if not phone or not api_id or not api_hash:
        print("❌ All fields are required!")
        return False
    
    # Create config content
    config_content = f"""[telegram]
# Get your API ID/HASH from https://my.telegram.org/auth
phone_number = "{phone}"
api_id = {api_id}
api_hash = "{api_hash}"

[sending]
# The send interval is how long to wait between sending messages (in seconds)
send_interval = 2
# The loop interval is how long to wait before re-sending messages to all groups (in seconds)
loop_interval = 300

[rate_limiting]
# Maximum requests per time window
max_requests = 20
# Time window in seconds
time_window = 60
# Maximum backoff time in seconds
max_backoff = 300

[auto_join]
# Delay between joining groups (in seconds)
join_delay = 1
# Maximum groups to join per session
max_groups_per_session = 50
"""
    
    # Ensure assets directory exists
    os.makedirs("assets", exist_ok=True)
    
    # Write config file
    try:
        with open(config_path, 'w') as f:
            f.write(config_content)
        print("✅ Configuration file created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create config file: {e}")
        return False

def create_groups_file():
    """Create groups.txt file if it doesn't exist"""
    groups_path = "assets/groups.txt"
    
    if os.path.exists(groups_path):
        print("📁 Groups file already exists.")
        return True
    
    print("\n📋 Creating groups.txt file...")
    print("You can add Telegram group invite links to this file later.")
    
    try:
        with open(groups_path, 'w') as f:
            f.write("# Add Telegram group invite links here\n")
            f.write("# One link per line\n")
            f.write("# Examples:\n")
            f.write("# https://t.me/groupname\n")
            f.write("# @groupname\n")
        print("✅ Groups file created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create groups file: {e}")
        return False

def main():
    """Main setup function"""
    print_banner()
    
    print("This setup will help you configure your Telegram Ad Bot.")
    print()
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Create configuration
    if not create_config():
        return
    
    # Create groups file
    if not create_groups_file():
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit assets/groups.txt to add group invite links")
    print("2. Run: python main.py")
    print("3. Follow the on-screen instructions")
    print("\nHappy botting! 🚀")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1) 