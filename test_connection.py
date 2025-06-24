#!/usr/bin/env python3
"""
Test script to verify Telegram connection and list available channels
"""

import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

async def test_connection():
    # Your credentials
    api_id = 23337938
    api_hash = "f49652eb9d10d48f2432770a55430d11"
    session_name = "assets/sessions/12064757656"
    
    print("Testing Telegram connection...")
    
    try:
        client = TelegramClient(session_name, api_id, api_hash)
        await client.connect()
        
        if await client.is_user_authorized():
            me = await client.get_me()
            print(f"✅ Connected successfully as @{me.username}")
            
            # Get dialogs (chats)
            print("\n📋 Available channels and groups:")
            dialogs = await client.get_dialogs()
            
            channels = []
            groups = []
            
            for dialog in dialogs:
                if dialog.is_channel:
                    channels.append(dialog)
                elif dialog.is_group:
                    groups.append(dialog)
            
            print(f"\n📺 Channels ({len(channels)}):")
            for i, channel in enumerate(channels[:10], 1):  # Show first 10
                username = getattr(channel.entity, 'username', 'private')
                print(f"  {i}. {channel.title} (@{username})")
            
            print(f"\n👥 Groups ({len(groups)}):")
            for i, group in enumerate(groups[:10], 1):  # Show first 10
                print(f"  {i}. {group.title}")
            
            if len(channels) > 10:
                print(f"  ... and {len(channels) - 10} more channels")
            if len(groups) > 10:
                print(f"  ... and {len(groups) - 10} more groups")
                
        else:
            print("❌ Not authorized. Please run main.py first to authenticate.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'client' in locals():
            await client.disconnect()

if __name__ == "__main__":
    asyncio.run(test_connection()) 