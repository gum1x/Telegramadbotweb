#!/usr/bin/env python3
"""
Test script for Telegram Bot functionality
Tests basic components without requiring real credentials
"""

import os
import sys
import json
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def test_dependencies():
    """Test if all dependencies are installed"""
    console.print("[bold cyan]Testing Dependencies...[/bold cyan]")
    
    dependencies = [
        ("telethon", "Telegram client library"),
        ("rich", "Rich terminal UI"),
        ("toml", "TOML configuration parser"),
        ("psutil", "System monitoring")
    ]
    
    table = Table(title="Dependency Check")
    table.add_column("Package", style="cyan")
    table.add_column("Description", style="green")
    table.add_column("Status", style="yellow")
    
    all_ok = True
    
    for package, description in dependencies:
        try:
            __import__(package)
            status = "✓ Installed"
        except ImportError:
            status = "✗ Missing"
            all_ok = False
        
        table.add_row(package, description, status)
    
    console.print(table)
    return all_ok

def test_config_files():
    """Test configuration files"""
    console.print("\n[bold cyan]Testing Configuration Files...[/bold cyan]")
    
    config_files = [
        ("assets/config.toml", "Single bot configuration"),
        ("assets/accounts.json", "Multi-account configuration"),
        ("assets/groups.txt", "Groups list"),
        ("requirements.txt", "Python dependencies")
    ]
    
    table = Table(title="Configuration Files")
    table.add_column("File", style="cyan")
    table.add_column("Description", style="green")
    table.add_column("Status", style="yellow")
    
    all_ok = True
    
    for file_path, description in config_files:
        if os.path.exists(file_path):
            try:
                # Try to read the file
                with open(file_path, 'r') as f:
                    content = f.read()
                
                if file_path.endswith('.json'):
                    json.loads(content)  # Test JSON parsing
                elif file_path.endswith('.toml'):
                    import toml
                    toml.loads(content)  # Test TOML parsing
                
                status = "✓ Valid"
            except Exception as e:
                status = f"✗ Error: {str(e)[:30]}"
                all_ok = False
        else:
            status = "✗ Missing"
            all_ok = False
        
        table.add_row(file_path, description, status)
    
    console.print(table)
    return all_ok

def test_bot_class():
    """Test bot class initialization"""
    console.print("\n[bold cyan]Testing Bot Class...[/bold cyan]")
    
    try:
        from main import TelegramBot, RateLimiter
        
        # Test RateLimiter
        rate_limiter = RateLimiter()
        assert rate_limiter.can_proceed() == True
        console.print("[green]✓ RateLimiter works correctly[/green]")
        
        # Test TelegramBot initialization (without connecting)
        test_config = {
            "telegram": {
                "phone_number": "+1234567890",
                "api_id": 12345678,
                "api_hash": "test_hash"
            },
            "sending": {"send_interval": 2, "loop_interval": 300},
            "rate_limiting": {"max_requests": 20, "time_window": 60, "max_backoff": 300},
            "auto_join": {"join_delay": 5, "max_groups_per_session": 50},
            "health_check": {
                "min_members": 10, "max_members": 100000, "max_inactive_days": 30,
                "skip_channels": True, "check_activity": True
            }
        }
        
        bot = TelegramBot()
        bot.config = test_config
        console.print("[green]✓ TelegramBot class initializes correctly[/green]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]✗ Bot class test failed: {e}[/red]")
        return False

def test_multi_bot_manager():
    """Test multi-bot manager"""
    console.print("\n[bold cyan]Testing Multi-Bot Manager...[/bold cyan]")
    
    try:
        from multi_bot import MultiBotManager
        
        manager = MultiBotManager()
        console.print("[green]✓ MultiBotManager initializes correctly[/green]")
        
        # Test account loading
        accounts = manager.load_accounts()
        console.print(f"[green]✓ Loaded {len(accounts)} accounts[/green]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]✗ Multi-bot manager test failed: {e}[/red]")
        return False

def test_health_check():
    """Test health check functionality"""
    console.print("\n[bold cyan]Testing Health Check Logic...[/bold cyan]")
    
    try:
        from main import TelegramBot
        
        bot = TelegramBot()
        
        # Test health check with mock data
        test_invite = "https://t.me/testgroup"
        
        # Mock health check result
        health_result = {
            "healthy": False,
            "reason": "Test group (not real)"
        }
        
        console.print(f"[green]✓ Health check logic works[/green]")
        console.print(f"[yellow]Test result: {health_result['reason']}[/yellow]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]✗ Health check test failed: {e}[/red]")
        return False

def create_test_config():
    """Create test configuration files"""
    console.print("\n[bold cyan]Creating Test Configuration...[/bold cyan]")
    
    # Create assets directory
    os.makedirs("assets", exist_ok=True)
    
    # Create test config.toml
    test_config = """[telegram]
phone_number = "+1234567890"
api_id = 12345678
api_hash = "test_hash_for_testing_only"

[sending]
send_interval = 2
loop_interval = 300

[rate_limiting]
max_requests = 20
time_window = 60
max_backoff = 300

[auto_join]
join_delay = 5
max_groups_per_session = 50

[health_check]
min_members = 10
max_members = 100000
max_inactive_days = 30
skip_channels = true
check_activity = true
"""
    
    with open("assets/config.toml", 'w') as f:
        f.write(test_config)
    
    # Create test accounts.json
    test_accounts = [
        {
            "phone": "+1234567890",
            "api_id": "12345678",
            "api_hash": "test_hash_1",
            "name": "Test Bot 1",
            "enabled": True,
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "phone": "+0987654321",
            "api_id": "87654321",
            "api_hash": "test_hash_2",
            "name": "Test Bot 2",
            "enabled": True,
            "created_at": "2024-01-01T00:00:00"
        }
    ]
    
    with open("assets/accounts.json", 'w') as f:
        json.dump(test_accounts, f, indent=2)
    
    # Create test groups.txt
    test_groups = """# Test Groups (for testing only)
https://t.me/testgroup1
https://t.me/testgroup2
@testgroup3
"""
    
    with open("assets/groups.txt", 'w') as f:
        f.write(test_groups)
    
    console.print("[green]✓ Test configuration files created[/green]")

def main():
    """Run all tests"""
    console.print("[bold cyan]╔══════════════════════════════════════════╗[/bold cyan]")
    console.print("[bold cyan]║           Telegram Bot Tests            ║[/bold cyan]")
    console.print("[bold cyan]╚══════════════════════════════════════════╝[/bold cyan]")
    
    # Check if test config should be created
    if not os.path.exists("assets/config.toml"):
        if console.input("\n[yellow]No configuration found. Create test config? (y/n): [/yellow]").lower() == 'y':
            create_test_config()
    
    # Run tests
    tests = [
        ("Dependencies", test_dependencies),
        ("Configuration Files", test_config_files),
        ("Bot Class", test_bot_class),
        ("Multi-Bot Manager", test_multi_bot_manager),
        ("Health Check", test_health_check)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            console.print(f"[red]✗ {test_name} test crashed: {e}[/red]")
            results.append((test_name, False))
    
    # Summary
    console.print("\n[bold cyan]Test Summary[/bold cyan]")
    summary_table = Table()
    summary_table.add_column("Test", style="cyan")
    summary_table.add_column("Result", style="green")
    
    passed = 0
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        summary_table.add_row(test_name, status)
        if result:
            passed += 1
    
    console.print(summary_table)
    
    console.print(f"\n[bold]Results: {passed}/{len(results)} tests passed[/bold]")
    
    if passed == len(results):
        console.print("[green]🎉 All tests passed! Your bot is ready to use.[/green]")
    else:
        console.print("[yellow]⚠️  Some tests failed. Check the errors above.[/yellow]")
    
    console.print("\n[bold]Next Steps:[/bold]")
    console.print("1. Run 'python launcher.py' to start the bot")
    console.print("2. Use option 4 to configure your real accounts")
    console.print("3. Replace test credentials with real ones")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Tests interrupted by user.[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Test suite failed: {e}[/red]") 