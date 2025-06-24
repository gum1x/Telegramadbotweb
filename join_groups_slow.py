#!/usr/bin/env python3
"""
Join groups with longer delays to avoid rate limiting
"""

import asyncio
import toml
from telethon import TelegramClient, errors, functions

async def join_groups_slowly():
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
            group_links = [line.strip() for line in f if line.strip() and (line.strip().startswith('http') or line.strip().startswith('t.me/'))]
        print(f"📋 Found {len(group_links)} group links in groups.txt")
    except FileNotFoundError:
        print("❌ groups.txt not found!")
        return
    
    # Join groups with longer delays
    print("\n🔗 Joining groups (with 30-second delays)...")
    joined_count = 0
    
    for i, link in enumerate(group_links[:5], 1):  # Start with first 5 groups
        try:
            print(f"\n  {i}/{min(5, len(group_links))}: Joining {link}")
            
            # Extract hash from link
            if 't.me/' in link:
                hash_part = link.split('t.me/')[-1]
            else:
                hash_part = link.split('/')[-1]
            
            await client(functions.messages.ImportChatInviteRequest(hash=hash_part))
            joined_count += 1
            print(f"    ✅ Joined successfully!")
            
            # Wait 30 seconds between joins
            print(f"    ⏳ Waiting 30 seconds...")
            await asyncio.sleep(30)
            
        except errors.FloodWaitError as e:
            wait_time = e.seconds
            print(f"    ⏳ Rate limited! Waiting {wait_time} seconds...")
            await asyncio.sleep(wait_time)
            # Try again after waiting
            try:
                await client(functions.messages.ImportChatInviteRequest(hash=hash_part))
                joined_count += 1
                print(f"    ✅ Joined successfully after waiting!")
            except Exception as e2:
                print(f"    ❌ Still failed after waiting: {e2}")
        except Exception as e:
            print(f"    ❌ Failed: {e}")
            await asyncio.sleep(5)
    
    print(f"\n📊 Joined {joined_count}/5 groups")
    
    # Check current groups
    dialogs = await client.get_dialogs()
    groups = [d for d in dialogs if d.is_group and not d.is_channel]
    print(f"📋 You now have {len(groups)} groups total")
    
    if 'client' in locals():
        await client.disconnect()
    print("\n✅ Group joining complete!")

if __name__ == "__main__":
    asyncio.run(join_groups_slowly()) 