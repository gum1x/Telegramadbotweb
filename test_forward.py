#!/usr/bin/env python3
"""
Test forwarding from source channel to existing groups
"""

import asyncio
import toml
from telethon import TelegramClient, errors

async def test_forwarding():
    # Load config
    with open("assets/config.toml") as f:
        config = toml.loads(f.read())
    
    # Connect to Telegram
    session_name = f"assets/sessions/{config['telegram']['phone_number'].replace('+', '').replace(' ', '')}"
    client = TelegramClient(session_name, config['telegram']['api_id'], config['telegram']['api_hash'])
    
    await client.connect()
    
    if not await client.is_user_authorized():
        print("❌ Not authorized!")
        return
    
    me = await client.get_me()
    print(f"✅ Connected as @{me.username}")
    
    # Get source channel
    source_channel = config['forwarding']['source_channel']
    try:
        channel_entity = await client.get_entity(source_channel)
        print(f"✅ Found source channel: {getattr(channel_entity, 'title', source_channel)}")
    except Exception as e:
        print(f"❌ Error getting source channel: {e}")
        return
    
    # Get all groups (not channels)
    dialogs = await client.get_dialogs()
    groups = [d for d in dialogs if d.is_group and not d.is_channel]
    print(f"📋 Found {len(groups)} groups to forward to")
    
    if len(groups) == 0:
        print("❌ No groups found! You need to join some groups first.")
        print("You can:")
        print("1. Manually join some groups via Telegram")
        print("2. Or run the join_groups.py script")
        return
    
    # Show groups
    print("\n👥 Groups found:")
    for i, group in enumerate(groups[:10], 1):
        print(f"  {i}. {group.title}")
    if len(groups) > 10:
        print(f"  ... and {len(groups) - 10} more")
    
    # Get latest message from source channel
    print(f"\n📨 Getting latest message from {source_channel}...")
    try:
        async for message in client.iter_messages(channel_entity, limit=1):
            if message and message.text:
                print(f"📨 Latest message: {message.text[:100]}...")
                
                # Test forward to first 3 groups only
                test_groups = groups[:3]
                print(f"\n🧪 Testing forward to {len(test_groups)} groups...")
                
                success_count = 0
                for i, group in enumerate(test_groups, 1):
                    try:
                        print(f"  {i}/{len(test_groups)}: Forwarding to {group.title}")
                        await client.forward_messages(group, message)
                        success_count += 1
                        print(f"    ✅ Success!")
                        await asyncio.sleep(15)  # Wait 15 seconds between forwards
                    except Exception as e:
                        print(f"    ❌ Failed: {e}")
                
                print(f"\n📊 Forward test complete: {success_count}/{len(test_groups)} successful")
                break
            else:
                print("❌ No text message found in latest message")
                break
    except Exception as e:
        print(f"❌ Error getting latest message: {e}")
    
    if 'client' in locals():
        await client.disconnect()
    print("\n✅ Test complete!")

if __name__ == "__main__":
    asyncio.run(test_forwarding()) 