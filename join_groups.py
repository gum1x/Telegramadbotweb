#!/usr/bin/env python3
"""
Script to join groups and test forwarding
"""

import asyncio
import toml
from telethon import TelegramClient, errors, functions
from telethon.sessions import StringSession

async def join_groups_and_test():
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
    
    # Load groups from file
    try:
        with open("assets/groups.txt", encoding="utf-8") as f:
            group_links = [line.strip() for line in f if line.strip()]
        print(f"📋 Found {len(group_links)} group links in groups.txt")
    except FileNotFoundError:
        print("❌ groups.txt not found!")
        return
    
    # Join groups
    print("\n🔗 Joining groups...")
    joined_count = 0
    
    for i, link in enumerate(group_links, 1):
        try:
            print(f"  {i}/{len(group_links)}: Joining {link}")
            await client(functions.messages.ImportChatInviteRequest(hash=link.split('/')[-1]))
            joined_count += 1
            print(f"    ✅ Joined successfully")
            await asyncio.sleep(5)  # Wait 5 seconds between joins
        except Exception as e:
            print(f"    ❌ Failed: {e}")
            await asyncio.sleep(2)
    
    print(f"\n📊 Joined {joined_count}/{len(group_links)} groups")
    
    # Test forwarding
    print("\n🔄 Testing forwarding...")
    
    # Get source channel
    source_channel = config['forwarding']['source_channel']
    try:
        channel_entity = await client.get_entity(source_channel)
        print(f"✅ Found source channel: {getattr(channel_entity, 'title', source_channel)}")
    except Exception as e:
        print(f"❌ Error getting source channel: {e}")
        return
    
    # Get all groups
    dialogs = await client.get_dialogs()
    groups = [d for d in dialogs if d.is_group and not d.is_channel]
    print(f"📋 Found {len(groups)} groups to forward to")
    
    if len(groups) == 0:
        print("❌ No groups found! Make sure you've joined some groups first.")
        return
    
    # Get latest message from source channel
    try:
        async for message in client.iter_messages(channel_entity, limit=1):
            if message:
                print(f"📨 Latest message: {message.text[:100]}...")
                
                # Test forward to first group only
                test_group = groups[0]
                print(f"🧪 Testing forward to: {test_group.title}")
                
                try:
                    await client.forward_messages(test_group, message)
                    print("✅ Forward test successful!")
                except Exception as e:
                    print(f"❌ Forward test failed: {e}")
                break
    except Exception as e:
        print(f"❌ Error getting latest message: {e}")
    
    if 'client' in locals():
        await client.disconnect()
    print("\n✅ Setup complete!")

if __name__ == "__main__":
    asyncio.run(join_groups_and_test()) 