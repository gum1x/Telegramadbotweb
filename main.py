import os
import sys
import toml
import logging
import asyncio
import time
from datetime import datetime, timedelta
from typing import List, Optional, Dict
import json

from telethon import TelegramClient, functions, types, errors
from telethon.sessions import StringSession
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from rich.layout import Layout
from rich.text import Text

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%H:%M:%S"
)
logging.getLogger("telethon").setLevel(logging.CRITICAL)

console = Console()

class RateLimiter:
    """Advanced rate limiter with exponential backoff"""
    
    def __init__(self, max_requests: int = 20, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
        self.backoff_multiplier = 1
        self.max_backoff = 300  # 5 minutes max backoff
        
    def can_proceed(self) -> bool:
        now = time.time()
        # Remove old requests outside the time window
        self.requests = [req for req in self.requests if now - req < self.time_window]
        
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False
    
    def get_wait_time(self) -> int:
        wait_time = min(self.time_window * self.backoff_multiplier, self.max_backoff)
        self.backoff_multiplier = min(self.backoff_multiplier * 2, 8)
        return wait_time
    
    def reset_backoff(self):
        self.backoff_multiplier = 1

class TelegramBot:
    def __init__(self):
        self.console = Console()
        self.config = self.load_config()
        self.rate_limiter = RateLimiter()
        self.client = None
        self.user = None
        self.source_chat = None
        self.forward_message = None
        self.account_name = None  # Added for multi-account support
        self.stats = {
            'messages_sent': 0,
            'groups_joined': 0,
            'errors': 0,
            'start_time': None
        }
        
    def load_config(self) -> dict:
        """Load configuration from TOML file"""
        try:
            with open("assets/config.toml") as f:
                return toml.loads(f.read())
        except FileNotFoundError:
            self.console.print("[red]Error: config.toml not found![/red]")
            sys.exit(1)
        except Exception as e:
            self.console.print(f"[red]Error loading config: {e}[/red]")
            sys.exit(1)
    
    def load_groups(self) -> List[str]:
        """Load group invites from file"""
        try:
            with open("assets/groups.txt", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            self.console.print("[yellow]Warning: groups.txt not found. No groups to join.[/yellow]")
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
                self.console.print("[yellow]Authentication required...[/yellow]")
                phone = self.config["telegram"]["phone_number"]
                await self.client.send_code_request(phone)
                
                code = Prompt.ask("Enter verification code")
                try:
                    await self.client.sign_in(phone, code)
                except errors.SessionPasswordNeededError:
                    password = Prompt.ask("Enter 2FA password", password=True)
                    await self.client.sign_in(password=password)
                
                self.console.print("[green]✓ Login successful! Session saved for future use.[/green]")
            else:
                self.console.print("[green]✓ Logged in using saved session![/green]")
            
            self.user = await self.client.get_me()
            self.console.print(f"[green]✓ Connected as @{self.user.username}[/green]")
            
        except Exception as e:
            self.console.print(f"[red]Connection failed: {e}[/red]")
            sys.exit(1)
    
    def show_main_menu(self):
        """Display the main menu panel"""
        menu_text = """
[bold cyan]Telegram Ad Bot - Control Panel[/bold cyan]

[1] 📢 Start Message Forwarding
[2] 🔗 Auto Join Groups
[3] 📊 View Statistics
[4] ⚙️  Settings
[5] 🚪 Exit

Select an option to continue...
        """
        
        panel = Panel(menu_text, title="Main Menu", border_style="blue")
        self.console.print(panel)
    
    async def select_source_chat(self):
        """Interactive source chat selection"""
        self.console.print("\n[bold]Select Source Chat:[/bold]")
        
        dialogs = await self.client.get_dialogs()
        chats = [d for d in dialogs if d.is_channel or d.is_group]
        
        table = Table(title="Available Chats")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Type", style="yellow")
        
        for i, chat in enumerate(chats[:20], 1):  # Limit to first 20
            chat_type = "Channel" if chat.is_channel else "Group"
            table.add_row(str(i), chat.title, chat_type)
        
        self.console.print(table)
        
        while True:
            try:
                choice = int(Prompt.ask("Select chat number", default="1"))
                if 1 <= choice <= len(chats):
                    self.source_chat = chats[choice - 1]
                    self.console.print(f"[green]✓ Selected: {self.source_chat.title}[/green]")
                    break
                else:
                    self.console.print("[red]Invalid selection![/red]")
            except ValueError:
                self.console.print("[red]Please enter a valid number![/red]")
    
    async def select_message(self):
        """Interactive message selection"""
        self.console.print("\n[bold]Select Message to Forward:[/bold]")
        
        messages = []
        async for message in self.client.iter_messages(self.source_chat, limit=10):
            if message.text:
                messages.append(message)
        
        table = Table(title="Recent Messages")
        table.add_column("ID", style="cyan")
        table.add_column("Content", style="green")
        table.add_column("Date", style="yellow")
        
        for i, msg in enumerate(messages, 1):
            content = msg.text[:50] + "..." if len(msg.text) > 50 else msg.text
            date = msg.date.strftime("%m/%d %H:%M")
            table.add_row(str(i), content, date)
        
        self.console.print(table)
        
        while True:
            try:
                choice = int(Prompt.ask("Select message number", default="1"))
                if 1 <= choice <= len(messages):
                    self.forward_message = messages[choice - 1]
                    self.console.print(f"[green]✓ Selected message: {self.forward_message.text[:50]}...[/green]")
                    break
                else:
                    self.console.print("[red]Invalid selection![/red]")
            except ValueError:
                self.console.print("[red]Please enter a valid number![/red]")
    
    async def check_group_health(self, invite_link: str) -> dict:
        """Check if a group is healthy and safe to join"""
        try:
            # Extract invite code
            if "t.me/" in invite_link:
                code = invite_link.split("t.me/")[1]
            else:
                code = invite_link
            
            # Get health check settings from config
            health_config = self.config.get("health_check", {})
            min_members = health_config.get("min_members", 10)
            max_members = health_config.get("max_members", 100000)
            max_inactive_days = health_config.get("max_inactive_days", 30)
            skip_channels = health_config.get("skip_channels", True)
            check_activity = health_config.get("check_activity", True)
            
            # Try to get group info without joining
            try:
                # Use resolveUsername to get basic info
                resolved = await self.client(functions.contacts.ResolveUsernameRequest(username=code))
                if not resolved:
                    return {"healthy": False, "reason": "Group not found"}
                
                # Get more detailed info
                full_chat = await self.client(functions.channels.GetFullChannelRequest(resolved.chats[0]))
                chat = resolved.chats[0]
                
                # Check if it's a channel (not a group)
                if skip_channels and hasattr(chat, 'broadcast') and chat.broadcast:
                    return {"healthy": False, "reason": "This is a channel, not a group"}
                
                # Check participant count
                if hasattr(full_chat.full_chat, 'participants_count'):
                    participant_count = full_chat.full_chat.participants_count
                    if participant_count < min_members:
                        return {"healthy": False, "reason": f"Too few members ({participant_count})"}
                    elif participant_count > max_members:
                        return {"healthy": False, "reason": f"Too many members ({participant_count}) - likely spam"}
                
                # Check if group is restricted
                if hasattr(chat, 'restricted') and chat.restricted:
                    return {"healthy": False, "reason": "Group is restricted"}
                
                # Check if group is banned
                if hasattr(chat, 'banned_rights') and chat.banned_rights:
                    return {"healthy": False, "reason": "Group has restrictions"}
                
                # Check if group is deactivated
                if hasattr(chat, 'deactivated') and chat.deactivated:
                    return {"healthy": False, "reason": "Group is deactivated"}
                
                # Check recent activity by getting recent messages
                if check_activity:
                    try:
                        recent_messages = await self.client.get_messages(chat, limit=5)
                        if not recent_messages:
                            return {"healthy": False, "reason": "No recent activity"}
                        
                        # Check if last message is too old
                        latest_message = recent_messages[0]
                        if latest_message.date < datetime.now() - timedelta(days=max_inactive_days):
                            return {"healthy": False, "reason": f"Group appears inactive (no messages in {max_inactive_days} days)"}
                        
                    except Exception:
                        return {"healthy": False, "reason": "Cannot access group messages"}
                
                return {
                    "healthy": True, 
                    "name": chat.title,
                    "participants": participant_count if hasattr(full_chat.full_chat, 'participants_count') else "Unknown",
                    "description": getattr(full_chat.full_chat, 'about', 'No description')
                }
                
            except errors.UsernameNotOccupiedError:
                return {"healthy": False, "reason": "Group does not exist"}
            except errors.UsernameInvalidError:
                return {"healthy": False, "reason": "Invalid group username"}
            except errors.ChatAdminRequiredError:
                return {"healthy": False, "reason": "Admin access required"}
            except errors.ChannelPrivateError:
                return {"healthy": False, "reason": "Group is private"}
            except errors.InviteHashExpiredError:
                return {"healthy": False, "reason": "Invite link expired"}
            except errors.InviteHashInvalidError:
                return {"healthy": False, "reason": "Invalid invite link"}
            except errors.UserPrivacyRestrictedError:
                return {"healthy": False, "reason": "Privacy restrictions"}
            except errors.FloodWaitError as e:
                return {"healthy": False, "reason": f"Rate limited ({e.seconds}s)"}
            except Exception as e:
                return {"healthy": False, "reason": f"Error checking group: {str(e)[:50]}"}
                
        except Exception as e:
            return {"healthy": False, "reason": f"Failed to check group: {str(e)[:50]}"}
    
    async def auto_join_groups(self):
        """Automatically join groups with health checking and rate limiting"""
        groups = self.load_groups()
        if not groups:
            self.console.print("[yellow]No groups to join![/yellow]")
            return
        
        self.console.print(f"[bold]Checking and joining {len(groups)} groups...[/bold]")
        
        # Filter out comments and empty lines
        valid_groups = [g for g in groups if g.strip() and not g.startswith('#')]
        
        if not valid_groups:
            self.console.print("[yellow]No valid groups found in groups.txt![/yellow]")
            return
        
        # Health check results
        healthy_groups = []
        unhealthy_groups = []
        
        # First, check all groups for health
        self.console.print("\n[bold cyan]🔍 Checking group health...[/bold cyan]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            health_task = progress.add_task("Checking groups...", total=len(valid_groups))
            
            for invite in valid_groups:
                progress.update(health_task, description=f"Checking: {invite}")
                
                health_result = await self.check_group_health(invite)
                
                if health_result["healthy"]:
                    healthy_groups.append((invite, health_result))
                    progress.update(health_task, description=f"✓ Healthy: {health_result['name']}")
                else:
                    unhealthy_groups.append((invite, health_result))
                    progress.update(health_task, description=f"✗ Unhealthy: {health_result['reason']}")
                
                await asyncio.sleep(0.5)  # Small delay between checks
                progress.advance(health_task)
        
        # Show health check results
        self.console.print(f"\n[green]✓ Found {len(healthy_groups)} healthy groups[/green]")
        self.console.print(f"[red]✗ Found {len(unhealthy_groups)} unhealthy groups[/red]")
        
        if unhealthy_groups:
            self.console.print("\n[bold yellow]Unhealthy Groups:[/bold yellow]")
            for invite, result in unhealthy_groups:
                self.console.print(f"  • {invite}: {result['reason']}")
        
        if not healthy_groups:
            self.console.print("[yellow]No healthy groups to join![/yellow]")
            return
        
        # Show healthy groups
        self.console.print(f"\n[bold green]Healthy Groups to Join:[/bold green]")
        table = Table(title="Groups to Join")
        table.add_column("Name", style="green")
        table.add_column("Members", style="cyan")
        table.add_column("Description", style="yellow")
        
        for invite, result in healthy_groups:
            description = result.get('description', 'No description')[:50]
            if len(description) > 50:
                description = description[:47] + "..."
            table.add_row(
                result.get('name', invite),
                str(result.get('participants', 'Unknown')),
                description
            )
        
        self.console.print(table)
        
        # Ask for confirmation
        if not Confirm.ask(f"\nJoin {len(healthy_groups)} healthy groups?"):
            self.console.print("[yellow]Joining cancelled.[/yellow]")
            return
        
        # Join healthy groups
        self.console.print(f"\n[bold]Joining {len(healthy_groups)} healthy groups...[/bold]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            join_task = progress.add_task("Joining groups...", total=len(healthy_groups))
            
            for invite, health_result in healthy_groups:
                if not self.rate_limiter.can_proceed():
                    wait_time = self.rate_limiter.get_wait_time()
                    self.console.print(f"[yellow]Rate limited. Waiting {wait_time}s...[/yellow]")
                    await asyncio.sleep(wait_time)
                
                try:
                    # Extract invite code
                    if "t.me/" in invite:
                        code = invite.split("t.me/")[1]
                    else:
                        code = invite
                    
                    await self.client(functions.channels.JoinChannelRequest(code))
                    self.stats['groups_joined'] += 1
                    progress.update(join_task, description=f"✓ Joined: {health_result.get('name', code)}")
                    
                except errors.FloodWaitError as e:
                    self.console.print(f"[red]Flood wait: {e.seconds}s[/red]")
                    await asyncio.sleep(e.seconds)
                except errors.UserPrivacyRestrictedError:
                    progress.update(join_task, description=f"✗ Privacy restricted: {health_result.get('name', code)}")
                except errors.InviteHashExpiredError:
                    progress.update(join_task, description=f"✗ Expired invite: {health_result.get('name', code)}")
                except Exception as e:
                    self.stats['errors'] += 1
                    progress.update(join_task, description=f"✗ Failed: {health_result.get('name', code)}")
                
                await asyncio.sleep(self.config.get("auto_join", {}).get("join_delay", 1))
                progress.advance(join_task)
        
        self.console.print(f"\n[green]✓ Successfully joined {self.stats['groups_joined']} groups![/green]")
        if self.stats['errors'] > 0:
            self.console.print(f"[red]✗ Failed to join {self.stats['errors']} groups[/red]")
    
    async def start_forwarding(self):
        """Start the message forwarding process"""
        if not self.source_chat or not self.forward_message:
            self.console.print("[red]Please select source chat and message first![/red]")
            return
        
        self.stats['start_time'] = datetime.now()
        
        # Get target groups
        dialogs = await self.client.get_dialogs()
        target_groups = [d for d in dialogs if d.is_group and d != self.source_chat]
        
        self.console.print(f"[bold]Starting forwarding to {len(target_groups)} groups...[/bold]")
        
        # Create live display
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        
        layout["header"].update(Panel(f"Forwarding to {len(target_groups)} groups", style="bold blue"))
        
        with Live(layout, refresh_per_second=4):
            for i, group in enumerate(target_groups, 1):
                # Check rate limiting
                if not self.rate_limiter.can_proceed():
                    wait_time = self.rate_limiter.get_wait_time()
                    layout["body"].update(Panel(f"Rate limited. Waiting {wait_time}s...", style="yellow"))
                    await asyncio.sleep(wait_time)
                
                try:
                    # Check if we already sent a message recently
                    recent_messages = await self.client.get_messages(group, limit=5)
                    if any(msg.from_id.user_id == self.user.id for msg in recent_messages):
                        layout["body"].update(Panel(f"Skipping {group.title} (recent message exists)", style="yellow"))
                        continue
                    
                    # Forward message
                    await self.client.forward_messages(group, self.forward_message)
                    self.stats['messages_sent'] += 1
                    self.rate_limiter.reset_backoff()
                    
                    layout["body"].update(Panel(f"✓ Forwarded to {group.title}", style="green"))
                    layout["footer"].update(Panel(f"Progress: {i}/{len(target_groups)} | Sent: {self.stats['messages_sent']} | Errors: {self.stats['errors']}", style="cyan"))
                    
                except errors.FloodWaitError as e:
                    self.console.print(f"[red]Flood wait: {e.seconds}s[/red]")
                    await asyncio.sleep(e.seconds)
                except Exception as e:
                    self.stats['errors'] += 1
                    layout["body"].update(Panel(f"✗ Failed: {group.title} - {str(e)[:50]}", style="red"))
                
                # Wait between messages
                await asyncio.sleep(self.config["sending"]["send_interval"])
        
        self.console.print(f"[green]✓ Forwarding completed! Sent {self.stats['messages_sent']} messages.[/green]")
    
    def show_statistics(self):
        """Display current statistics"""
        if not self.stats['start_time']:
            self.console.print("[yellow]No statistics available yet.[/yellow]")
            return
        
        runtime = datetime.now() - self.stats['start_time']
        
        stats_text = f"""
[bold]Bot Statistics[/bold]

📊 Messages Sent: {self.stats['messages_sent']}
🔗 Groups Joined: {self.stats['groups_joined']}
❌ Errors: {self.stats['errors']}
⏱️  Runtime: {runtime}
        """
        
        panel = Panel(stats_text, title="Statistics", border_style="green")
        self.console.print(panel)
    
    def show_settings(self):
        """Display current settings"""
        health_config = self.config.get("health_check", {})
        
        settings_text = f"""
[bold]Current Settings[/bold]

📱 Phone: {self.config['telegram']['phone_number']}
⏱️  Send Interval: {self.config['sending']['send_interval']}s
🔄 Loop Interval: {self.config['sending']['loop_interval']}s
📊 Rate Limit: {self.rate_limiter.max_requests} requests/{self.rate_limiter.time_window}s
💾 Session: assets/sessions/{self.config['telegram']['phone_number'].replace('+', '').replace(' ', '')}.session

[bold]Health Check Settings[/bold]
👥 Min Members: {health_config.get('min_members', 10)}
👥 Max Members: {health_config.get('max_members', 100000)}
📅 Max Inactive Days: {health_config.get('max_inactive_days', 30)}
📺 Skip Channels: {health_config.get('skip_channels', True)}
🔍 Check Activity: {health_config.get('check_activity', True)}
        """
        
        panel = Panel(settings_text, title="Settings", border_style="yellow")
        self.console.print(panel)
        
        # Show session management options
        session_options = """
[bold]Session Management[/bold]

[1] 🔄 Clear saved session (logout)
[2] ↩️  Back to main menu
        """
        
        session_panel = Panel(session_options, title="Session Options", border_style="cyan")
        self.console.print(session_panel)
        
        choice = Prompt.ask("Select option", choices=["1", "2"])
        
        if choice == "1":
            if Confirm.ask("Are you sure you want to clear the saved session?"):
                session_file = f"assets/sessions/{self.config['telegram']['phone_number'].replace('+', '').replace(' ', '')}.session"
                try:
                    if os.path.exists(session_file):
                        os.remove(session_file)
                        self.console.print("[green]✓ Session cleared! You'll need to log in again next time.[/green]")
                    else:
                        self.console.print("[yellow]No saved session found.[/yellow]")
                except Exception as e:
                    self.console.print(f"[red]Failed to clear session: {e}[/red]")
    
    async def run(self):
        """Main application loop"""
        # Clear screen and show welcome
        os.system('cls' if os.name == 'nt' else 'clear')
        
        welcome_text = """
[bold cyan]╔══════════════════════════════════════════╗[/bold cyan]
[bold cyan]║           Telegram Ad Bot               ║[/bold cyan]
[bold cyan]║         Advanced & Simplified           ║[/bold cyan]
[bold cyan]╚══════════════════════════════════════════╝[/bold cyan]
        """
        
        self.console.print(welcome_text)
        
        # Connect to Telegram
        await self.connect()
        
        # Main menu loop
        while True:
            self.show_main_menu()
            
            choice = Prompt.ask("Select option", choices=["1", "2", "3", "4", "5"])
            
            if choice == "1":
                if not self.source_chat:
                    await self.select_source_chat()
                if not self.forward_message:
                    await self.select_message()
                await self.start_forwarding()
                
            elif choice == "2":
                await self.auto_join_groups()
                
            elif choice == "3":
                self.show_statistics()
                
            elif choice == "4":
                self.show_settings()
                
            elif choice == "5":
                if Confirm.ask("Are you sure you want to exit?"):
                    self.console.print("[green]Goodbye![/green]")
                    break
            
            if choice != "5":
                Prompt.ask("\nPress Enter to continue...")

async def main():
    bot = TelegramBot()
    await bot.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Bot stopped by user.[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Unexpected error: {e}[/red]")
