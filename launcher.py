#!/usr/bin/env python3
"""
Unified Telegram Bot Launcher
Choose between single account or multi-account mode
"""

import os
import sys
import json
import asyncio
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text

console = Console()

def show_welcome():
    """Show welcome screen"""
    welcome_text = """
[bold cyan]╔══════════════════════════════════════════╗[/bold cyan]
[bold cyan]║           Telegram Ad Bot               ║[/bold cyan]
[bold cyan]║         Advanced & Simplified           ║[/bold cyan]
[bold cyan]╚══════════════════════════════════════════╝[/bold cyan]

[bold]Choose your bot mode:[/bold]

[1] 📱 Single Account Bot
    • Simple setup with one account
    • Interactive panel interface
    • Perfect for beginners

[2] 🤖 Multi-Account Bot Manager
    • Run multiple accounts simultaneously
    • Central dashboard for all bots
    • Advanced hosting capabilities

[3] 🏠 Hosting Mode
    • Run bots as background service
    • Auto-restart on failure
    • Production deployment

[4] ⚙️  Setup & Configuration
    • Quick setup wizard
    • Account configuration
    • Settings management

[5] 🚪 Exit
    """
    
    panel = Panel(welcome_text, title="Welcome to Telegram Ad Bot", border_style="blue")
    console.print(panel)

def check_dependencies():
    """Check if all dependencies are installed"""
    try:
        import telethon
        import rich
        import toml
        import psutil
        console.print("[green]✓ All dependencies are installed![/green]")
        return True
    except ImportError as e:
        console.print(f"[red]✗ Missing dependency: {e}[/red]")
        console.print("[yellow]Installing dependencies...[/yellow]")
        
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            console.print("[green]✓ Dependencies installed successfully![/green]")
            return True
        except Exception as e:
            console.print(f"[red]✗ Failed to install dependencies: {e}[/red]")
            console.print("[yellow]Please run: pip install -r requirements.txt[/yellow]")
            return False

def check_config_files():
    """Check if configuration files exist"""
    config_status = []
    
    # Check single bot config
    if os.path.exists("assets/config.toml"):
        config_status.append(("Single Bot Config", "✓", "green"))
    else:
        config_status.append(("Single Bot Config", "✗", "red"))
    
    # Check multi-account config
    if os.path.exists("assets/accounts.json"):
        with open("assets/accounts.json", 'r') as f:
            accounts = json.load(f)
        config_status.append((f"Multi-Account Config ({len(accounts)} accounts)", "✓", "green"))
    else:
        config_status.append(("Multi-Account Config", "✗", "red"))
    
    # Check groups file
    if os.path.exists("assets/groups.txt"):
        with open("assets/groups.txt", 'r') as f:
            groups = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        config_status.append((f"Groups File ({len(groups)} groups)", "✓", "green"))
    else:
        config_status.append(("Groups File", "✗", "red"))
    
    return config_status

def show_system_status():
    """Show system status and configuration"""
    console.print("\n[bold cyan]System Status[/bold cyan]")
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Check config files
    config_status = check_config_files()
    
    # Display status table
    table = Table(title="Configuration Status")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")
    
    table.add_row("Dependencies", "✓" if deps_ok else "✗")
    for component, status, color in config_status:
        table.add_row(component, status)
    
    console.print(table)
    
    # Recommendations
    if not deps_ok:
        console.print("[red]Please install dependencies first![/red]")
        return False
    
    missing_configs = [comp for comp, status, _ in config_status if status == "✗"]
    if missing_configs:
        console.print(f"[yellow]Missing configurations: {', '.join(missing_configs)}[/yellow]")
        console.print("[yellow]Use option 4 to set up configurations[/yellow]")
    
    return True

def run_single_bot():
    """Run single account bot"""
    console.print("\n[bold]Starting Single Account Bot...[/bold]")
    
    if not os.path.exists("assets/config.toml"):
        console.print("[red]Single bot config not found![/red]")
        console.print("[yellow]Please use option 4 to set up your account first.[/yellow]")
        return
    
    try:
        import subprocess
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        console.print("\n[yellow]Single bot stopped by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error running single bot: {e}[/red]")

def run_multi_bot():
    """Run multi-account bot manager"""
    console.print("\n[bold]Starting Multi-Account Bot Manager...[/bold]")
    
    if not os.path.exists("assets/accounts.json"):
        console.print("[red]Multi-account config not found![/red]")
        console.print("[yellow]Please use option 4 to set up your accounts first.[/yellow]")
        return
    
    try:
        import subprocess
        subprocess.run([sys.executable, "multi_bot.py"])
    except KeyboardInterrupt:
        console.print("\n[yellow]Multi-bot manager stopped by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error running multi-bot manager: {e}[/red]")

def run_hosting():
    """Run hosting mode"""
    console.print("\n[bold]Starting Hosting Mode...[/bold]")
    
    if not os.path.exists("assets/accounts.json"):
        console.print("[red]Multi-account config not found![/red]")
        console.print("[yellow]Please use option 4 to set up your accounts first.[/yellow]")
        return
    
    console.print("[yellow]Hosting mode will run bots in the background.[/yellow]")
    console.print("[yellow]Press Ctrl+C to stop all bots.[/yellow]")
    
    try:
        import subprocess
        subprocess.run([sys.executable, "host.py"])
    except KeyboardInterrupt:
        console.print("\n[yellow]Hosting mode stopped by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error running hosting mode: {e}[/red]")

def setup_wizard():
    """Interactive setup wizard"""
    console.print("\n[bold cyan]Setup Wizard[/bold cyan]")
    console.print("This will help you configure your bot(s).\n")
    
    setup_options = """
[bold]Setup Options:[/bold]

[1] 📱 Single Account Setup
    • Configure one Telegram account
    • Simple and quick setup

[2] 🤖 Multi-Account Setup
    • Configure multiple Telegram accounts
    • Advanced multi-bot setup

[3] 📋 Groups Setup
    • Add groups to join
    • Configure group list

[4] ⚙️  Settings Configuration
    • Configure bot settings
    • Rate limiting and delays

[5] ↩️  Back to Main Menu
    """
    
    panel = Panel(setup_options, title="Setup Options", border_style="yellow")
    console.print(panel)
    
    choice = Prompt.ask("Select setup option", choices=["1", "2", "3", "4", "5"])
    
    if choice == "1":
        setup_single_account()
    elif choice == "2":
        setup_multi_account()
    elif choice == "3":
        setup_groups()
    elif choice == "4":
        setup_settings()
    elif choice == "5":
        return

def setup_single_account():
    """Setup single account configuration"""
    console.print("\n[bold]Single Account Setup[/bold]")
    
    # Get account details
    phone = Prompt.ask("Phone number (e.g., +1234567890)")
    api_id = Prompt.ask("API ID")
    api_hash = Prompt.ask("API Hash")
    
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
join_delay = 5
# Maximum groups to join per session
max_groups_per_session = 50

[health_check]
# Minimum number of members required for a group to be considered healthy
min_members = 10
# Maximum number of members (groups with more are considered spam)
max_members = 100000
# Maximum days since last activity for a group to be considered active
max_inactive_days = 30
# Whether to skip channels (only join groups)
skip_channels = true
# Whether to check group activity before joining
check_activity = true
"""
    
    # Ensure assets directory exists
    os.makedirs("assets", exist_ok=True)
    
    # Write config file
    try:
        with open("assets/config.toml", 'w') as f:
            f.write(config_content)
        console.print("[green]✓ Single account configuration saved![/green]")
    except Exception as e:
        console.print(f"[red]✗ Failed to save configuration: {e}[/red]")

def setup_multi_account():
    """Setup multi-account configuration"""
    console.print("\n[bold]Multi-Account Setup[/bold]")
    
    accounts = []
    
    while True:
        console.print(f"\n[bold]Account #{len(accounts) + 1}[/bold]")
        
        phone = Prompt.ask("Phone number (e.g., +1234567890)")
        api_id = Prompt.ask("API ID")
        api_hash = Prompt.ask("API Hash")
        name = Prompt.ask("Bot name (optional)", default=f"Bot {phone}")
        
        account = {
            "phone": phone,
            "api_id": api_id,
            "api_hash": api_hash,
            "name": name,
            "enabled": True,
            "created_at": "2024-01-01T00:00:00"
        }
        accounts.append(account)
        
        if not Confirm.ask("Add another account?"):
            break
    
    # Save accounts
    try:
        os.makedirs("assets", exist_ok=True)
        with open("assets/accounts.json", 'w') as f:
            json.dump(accounts, f, indent=2)
        console.print(f"[green]✓ Saved {len(accounts)} accounts![/green]")
    except Exception as e:
        console.print(f"[red]✗ Failed to save accounts: {e}[/red]")

def setup_groups():
    """Setup groups configuration"""
    console.print("\n[bold]Groups Setup[/bold]")
    
    groups = []
    
    console.print("Enter Telegram group invite links (one per line):")
    console.print("Examples: https://t.me/groupname or @groupname")
    console.print("Press Enter twice when done.\n")
    
    while True:
        group = input(f"Group #{len(groups) + 1}: ").strip()
        if not group:
            break
        if group and not group.startswith('#'):
            groups.append(group)
    
    # Save groups
    try:
        os.makedirs("assets", exist_ok=True)
        with open("assets/groups.txt", 'w') as f:
            f.write("# Telegram Group Invite Links\n")
            f.write("# Add one invite link per line\n")
            f.write("# Examples:\n")
            f.write("# https://t.me/groupname\n")
            f.write("# @groupname\n\n")
            for group in groups:
                f.write(f"{group}\n")
        console.print(f"[green]✓ Saved {len(groups)} groups![/green]")
    except Exception as e:
        console.print(f"[red]✗ Failed to save groups: {e}[/red]")

def setup_settings():
    """Setup global settings"""
    console.print("\n[bold]Settings Configuration[/bold]")
    console.print("This will configure global bot settings.\n")
    
    # Get settings
    send_interval = Prompt.ask("Send interval (seconds)", default="2")
    join_delay = Prompt.ask("Join delay (seconds)", default="5")
    max_requests = Prompt.ask("Max requests per minute", default="20")
    
    # Create settings content
    settings_content = f"""# Global Bot Settings
# These settings apply to all bots

SEND_INTERVAL = {send_interval}
JOIN_DELAY = {join_delay}
MAX_REQUESTS_PER_MINUTE = {max_requests}

# Health Check Settings
MIN_MEMBERS = 10
MAX_MEMBERS = 100000
MAX_INACTIVE_DAYS = 30
SKIP_CHANNELS = true
CHECK_ACTIVITY = true
"""
    
    try:
        with open("settings.py", 'w') as f:
            f.write(settings_content)
        console.print("[green]✓ Global settings saved![/green]")
    except Exception as e:
        console.print(f"[red]✗ Failed to save settings: {e}[/red]")

def main():
    """Main launcher function"""
    while True:
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Show welcome
        show_welcome()
        
        # Show system status
        system_ok = show_system_status()
        
        # Get user choice
        choice = Prompt.ask("\nSelect option", choices=["1", "2", "3", "4", "5"])
        
        if choice == "1":
            run_single_bot()
        elif choice == "2":
            run_multi_bot()
        elif choice == "3":
            run_hosting()
        elif choice == "4":
            setup_wizard()
        elif choice == "5":
            if Confirm.ask("Are you sure you want to exit?"):
                console.print("[green]Goodbye![/green]")
                break
        
        if choice != "5":
            Prompt.ask("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Launcher stopped by user.[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Unexpected error: {e}[/red]") 