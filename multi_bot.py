#!/usr/bin/env python3
"""
Multi-Account Telegram Bot Manager
Runs multiple bot instances simultaneously
"""

import os
import sys
import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional
import signal
import threading
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from rich.tree import Tree

# Import the main bot class
from main import TelegramBot

console = Console()

class MultiBotManager:
    def __init__(self):
        self.console = Console()
        self.bots: Dict[str, TelegramBot] = {}
        self.bot_tasks: Dict[str, asyncio.Task] = {}
        self.bot_status: Dict[str, str] = {}
        self.running = False
        self.accounts_file = "assets/accounts.json"
        
    def load_accounts(self) -> List[dict]:
        """Load multiple accounts from JSON file"""
        try:
            if os.path.exists(self.accounts_file):
                with open(self.accounts_file, 'r') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            self.console.print(f"[red]Error loading accounts: {e}[/red]")
            return []
    
    def save_accounts(self, accounts: List[dict]):
        """Save accounts to JSON file"""
        try:
            os.makedirs("assets", exist_ok=True)
            with open(self.accounts_file, 'w') as f:
                json.dump(accounts, f, indent=2)
        except Exception as e:
            self.console.print(f"[red]Error saving accounts: {e}[/red]")
    
    def create_account_config(self, phone: str, api_id: str, api_hash: str) -> dict:
        """Create a single account configuration"""
        return {
            "phone": phone,
            "api_id": api_id,
            "api_hash": api_hash,
            "enabled": True,
            "name": f"Bot {phone}",
            "created_at": datetime.now().isoformat()
        }
    
    def setup_accounts(self):
        """Interactive account setup"""
        self.console.print("[bold cyan]Multi-Account Setup[/bold cyan]")
        self.console.print("This will help you configure multiple Telegram accounts.\n")
        
        accounts = []
        
        while True:
            self.console.print(f"[bold]Account #{len(accounts) + 1}[/bold]")
            
            phone = Prompt.ask("Phone number (e.g., +1234567890)")
            api_id = Prompt.ask("API ID")
            api_hash = Prompt.ask("API Hash")
            name = Prompt.ask("Bot name (optional)", default=f"Bot {phone}")
            
            account = self.create_account_config(phone, api_id, api_hash)
            account["name"] = name
            accounts.append(account)
            
            if not Confirm.ask("Add another account?"):
                break
        
        self.save_accounts(accounts)
        self.console.print(f"[green]✓ Saved {len(accounts)} accounts![/green]")
    
    async def create_bot_instance(self, account: dict) -> Optional[TelegramBot]:
        """Create a bot instance for a specific account"""
        try:
            # Create a custom config for this account
            config = {
                "telegram": {
                    "phone_number": account["phone"],
                    "api_id": int(account["api_id"]),
                    "api_hash": account["api_hash"]
                },
                "sending": {
                    "send_interval": 2,
                    "loop_interval": 300
                },
                "rate_limiting": {
                    "max_requests": 20,
                    "time_window": 60,
                    "max_backoff": 300
                },
                "auto_join": {
                    "join_delay": 5,
                    "max_groups_per_session": 50
                },
                "health_check": {
                    "min_members": 10,
                    "max_members": 100000,
                    "max_inactive_days": 30,
                    "skip_channels": True,
                    "check_activity": True
                }
            }
            
            # Create bot instance with custom config
            bot = TelegramBot()
            bot.config = config
            bot.account_name = account.get("name", account["phone"])
            
            return bot
        except Exception as e:
            self.console.print(f"[red]Error creating bot for {account['phone']}: {e}[/red]")
            return None
    
    async def start_bot(self, account: dict):
        """Start a single bot instance"""
        bot = await self.create_bot_instance(account)
        if not bot:
            return
        
        bot_id = account["phone"]
        self.bots[bot_id] = bot
        self.bot_status[bot_id] = "Starting..."
        
        try:
            # Connect the bot
            await bot.connect()
            self.bot_status[bot_id] = "Connected"
            
            # Keep the bot running in a simple loop
            while self.running:
                try:
                    # Simple keep-alive loop instead of running the full UI
                    await asyncio.sleep(1)
                except Exception as e:
                    self.bot_status[bot_id] = f"Error: {str(e)[:50]}"
                    await asyncio.sleep(5)  # Wait before retrying
                    
        except Exception as e:
            self.bot_status[bot_id] = f"Failed: {str(e)[:50]}"
            self.console.print(f"[red]Bot {bot_id} failed: {e}[/red]")
    
    async def start_all_bots(self):
        """Start all enabled bots"""
        accounts = self.load_accounts()
        enabled_accounts = [acc for acc in accounts if acc.get("enabled", True)]
        
        if not enabled_accounts:
            self.console.print("[yellow]No enabled accounts found![/yellow]")
            return
        
        self.running = True
        self.console.print(f"[bold]Starting {len(enabled_accounts)} bots...[/bold]")
        
        # Create tasks for all bots
        tasks = []
        for account in enabled_accounts:
            task = asyncio.create_task(self.start_bot(account))
            tasks.append(task)
        
        # Wait for all bots to complete
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Stopping all bots...[/yellow]")
            self.running = False
    
    def show_dashboard(self):
        """Show the multi-bot dashboard"""
        accounts = self.load_accounts()
        
        # Create dashboard layout
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        
        # Header
        header_text = f"""
[bold cyan]Multi-Bot Dashboard[/bold cyan]
Total Accounts: {len(accounts)} | Running: {len([b for b in self.bot_status.values() if 'Connected' in b])}
        """
        layout["header"].update(Panel(header_text, style="bold blue"))
        
        # Body - Account status
        if accounts:
            table = Table(title="Account Status")
            table.add_column("Name", style="cyan")
            table.add_column("Phone", style="green")
            table.add_column("Status", style="yellow")
            table.add_column("Enabled", style="magenta")
            
            for account in accounts:
                status = self.bot_status.get(account["phone"], "Not Started")
                enabled = "✓" if account.get("enabled", True) else "✗"
                table.add_row(
                    account.get("name", "Unknown"),
                    account["phone"],
                    status,
                    enabled
                )
            
            layout["body"].update(table)
        else:
            layout["body"].update(Panel("No accounts configured", style="yellow"))
        
        # Footer - Controls
        footer_text = """
[bold]Controls:[/bold]
[1] Start All Bots    [2] Stop All Bots    [3] Add Account    [4] Settings    [5] Exit
        """
        layout["footer"].update(Panel(footer_text, style="cyan"))
        
        return layout
    
    async def run_dashboard(self):
        """Run the interactive dashboard"""
        while True:
            # Clear screen
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Show dashboard
            layout = self.show_dashboard()
            self.console.print(layout)
            
            # Get user input
            choice = Prompt.ask("Select option", choices=["1", "2", "3", "4", "5"])
            
            if choice == "1":
                # Start all bots
                if not self.running:
                    await self.start_all_bots()
                else:
                    self.console.print("[yellow]Bots are already running![/yellow]")
                    
            elif choice == "2":
                # Stop all bots
                if self.running:
                    self.running = False
                    self.console.print("[green]Stopping all bots...[/green]")
                else:
                    self.console.print("[yellow]No bots are running![/yellow]")
                    
            elif choice == "3":
                # Add account
                self.setup_accounts()
                
            elif choice == "4":
                # Settings
                self.show_settings()
                
            elif choice == "5":
                # Exit
                if Confirm.ask("Are you sure you want to exit?"):
                    self.running = False
                    self.console.print("[green]Goodbye![/green]")
                    break
            
            if choice != "5":
                Prompt.ask("\nPress Enter to continue...")
    
    def show_settings(self):
        """Show multi-bot settings"""
        accounts = self.load_accounts()
        
        settings_text = f"""
[bold]Multi-Bot Settings[/bold]

📁 Accounts File: {self.accounts_file}
👥 Total Accounts: {len(accounts)}
🔄 Running Bots: {len([b for b in self.bot_status.values() if 'Connected' in b])}
        """
        
        panel = Panel(settings_text, title="Settings", border_style="yellow")
        self.console.print(panel)
        
        # Account management
        if accounts:
            self.console.print("\n[bold]Account Management[/bold]")
            table = Table()
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Phone", style="yellow")
            table.add_column("Enabled", style="magenta")
            
            for i, account in enumerate(accounts, 1):
                enabled = "✓" if account.get("enabled", True) else "✗"
                table.add_row(
                    str(i),
                    account.get("name", "Unknown"),
                    account["phone"],
                    enabled
                )
            
            self.console.print(table)
            
            # Account actions
            actions_text = """
[bold]Actions:[/bold]
[1] Enable/Disable Account    [2] Delete Account    [3] Back
            """
            self.console.print(actions_text)
            
            action = Prompt.ask("Select action", choices=["1", "2", "3"])
            
            if action == "1":
                # Toggle account
                acc_id = int(Prompt.ask("Enter account ID")) - 1
                if 0 <= acc_id < len(accounts):
                    accounts[acc_id]["enabled"] = not accounts[acc_id].get("enabled", True)
                    self.save_accounts(accounts)
                    self.console.print("[green]Account status updated![/green]")
                    
            elif action == "2":
                # Delete account
                acc_id = int(Prompt.ask("Enter account ID")) - 1
                if 0 <= acc_id < len(accounts):
                    if Confirm.ask(f"Delete account {accounts[acc_id]['phone']}?"):
                        del accounts[acc_id]
                        self.save_accounts(accounts)
                        self.console.print("[green]Account deleted![/green]")

async def main():
    """Main function"""
    manager = MultiBotManager()
    
    # Check if accounts exist
    accounts = manager.load_accounts()
    
    if not accounts:
        console.print("[yellow]No accounts configured. Let's set up your first account![/yellow]")
        manager.setup_accounts()
    
    # Run the dashboard
    await manager.run_dashboard()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Multi-bot manager stopped by user.[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Unexpected error: {e}[/red]") 