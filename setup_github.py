#!/usr/bin/env python3
"""
GitHub Repository Setup Script
Helps users prepare the repository for GitHub
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Print setup banner"""
    banner = """
╔══════════════════════════════════════════╗
║        GitHub Repository Setup           ║
║         Telegram Ad Bot v2.0             ║
╚══════════════════════════════════════════╝
    """
    print(banner)

def check_git():
    """Check if git is installed"""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def init_git_repo():
    """Initialize git repository"""
    if not check_git():
        print("❌ Git is not installed. Please install Git first.")
        return False
    
    try:
        # Check if already a git repo
        if os.path.exists(".git"):
            print("✓ Git repository already initialized")
            return True
        
        # Initialize git repository
        subprocess.run(["git", "init"], check=True)
        print("✓ Git repository initialized")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to initialize git repository: {e}")
        return False

def create_initial_commit():
    """Create initial commit"""
    try:
        # Add all files
        subprocess.run(["git", "add", "."], check=True)
        print("✓ Files added to git")
        
        # Create initial commit
        subprocess.run(["git", "commit", "-m", "Initial commit: Telegram Ad Bot v2.0"], check=True)
        print("✓ Initial commit created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create initial commit: {e}")
        return False

def setup_remote():
    """Setup remote repository"""
    print("\n📋 GitHub Repository Setup")
    print("1. Go to https://github.com/new")
    print("2. Create a new repository named 'telegram-ad-bot'")
    print("3. Don't initialize with README (we already have one)")
    print("4. Copy the repository URL")
    
    repo_url = input("\nEnter your GitHub repository URL: ").strip()
    
    if not repo_url:
        print("❌ No repository URL provided")
        return False
    
    try:
        # Add remote origin
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
        print("✓ Remote origin added")
        
        # Push to GitHub
        subprocess.run(["git", "branch", "-M", "main"], check=True)
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        print("✓ Code pushed to GitHub")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to setup remote: {e}")
        return False

def create_release():
    """Create a GitHub release"""
    print("\n📦 Creating GitHub Release")
    print("1. Go to your GitHub repository")
    print("2. Click 'Releases' on the right side")
    print("3. Click 'Create a new release'")
    print("4. Tag version: v2.0.0")
    print("5. Release title: Telegram Ad Bot v2.0")
    print("6. Description:")
    
    release_description = """
## 🚀 Telegram Ad Bot v2.0

### ✨ New Features
- **Multi-Account Support** - Run multiple bots simultaneously
- **Advanced Hosting** - Service mode with auto-restart
- **Health Checking** - Validate groups before joining
- **Beautiful UI** - Rich terminal interface
- **Session Persistence** - Save login sessions

### 🛡️ Safety Features
- Advanced rate limiting with exponential backoff
- Group health checking to avoid banned groups
- Error recovery and automatic retries
- Duplicate message prevention

### 🏠 Hosting Options
- Direct hosting mode
- Systemd service integration
- Docker containerization
- Process monitoring and auto-restart

### 📱 Usage Modes
- Single account bot (beginner-friendly)
- Multi-account manager (advanced users)
- Hosting mode (production deployment)

### 🧪 Testing
- Comprehensive test suite
- Automated GitHub Actions
- Dependency checking
- Configuration validation

### 📚 Documentation
- Complete setup guide
- Multi-account documentation
- Contributing guidelines
- Troubleshooting guide

### 🔧 Installation
```bash
git clone https://github.com/yourusername/telegram-ad-bot.git
cd telegram-ad-bot
pip install -r requirements.txt
python launcher.py
```

### 📄 License
MIT License - see LICENSE file for details

### ⚠️ Disclaimer
This bot is for educational purposes. Please respect Telegram's Terms of Service and use responsibly.
    """
    
    print(release_description)
    print("\n7. Upload the following files as assets:")
    print("   - telegram-ad-bot-v2.0.zip (if you create one)")
    print("8. Click 'Publish release'")

def create_zip_release():
    """Create a zip file for release"""
    try:
        import zipfile
        
        # Files to include in release
        include_files = [
            "launcher.py",
            "main.py", 
            "multi_bot.py",
            "host.py",
            "test_bot.py",
            "setup.py",
            "requirements.txt",
            "README.md",
            "README_MULTI.md",
            "CONTRIBUTING.md",
            "LICENSE",
            ".gitignore",
            "assets/config.example.toml",
            "assets/accounts.example.json", 
            "assets/groups.example.txt"
        ]
        
        # Directories to include
        include_dirs = [
            "assets",
            ".github"
        ]
        
        zip_filename = "telegram-ad-bot-v2.0.zip"
        
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add individual files
            for file_path in include_files:
                if os.path.exists(file_path):
                    zipf.write(file_path)
                    print(f"✓ Added {file_path}")
            
            # Add directories
            for dir_path in include_dirs:
                if os.path.exists(dir_path):
                    for root, dirs, files in os.walk(dir_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = file_path
                            zipf.write(file_path, arcname)
                            print(f"✓ Added {file_path}")
        
        print(f"✓ Release package created: {zip_filename}")
        return True
    except Exception as e:
        print(f"❌ Failed to create release package: {e}")
        return False

def main():
    """Main setup function"""
    print_banner()
    
    print("This script will help you set up your GitHub repository for Telegram Ad Bot.")
    print()
    
    # Step 1: Initialize git repository
    print("Step 1: Initializing Git Repository")
    if not init_git_repo():
        return
    
    # Step 2: Create initial commit
    print("\nStep 2: Creating Initial Commit")
    if not create_initial_commit():
        return
    
    # Step 3: Setup remote repository
    print("\nStep 3: Setting up GitHub Repository")
    if not setup_remote():
        return
    
    # Step 4: Create release package
    print("\nStep 4: Creating Release Package")
    create_zip_release()
    
    # Step 5: Create GitHub release
    print("\nStep 5: Creating GitHub Release")
    create_release()
    
    print("\n🎉 GitHub repository setup complete!")
    print("\nNext steps:")
    print("1. Create the GitHub release as described above")
    print("2. Update the README.md with your actual GitHub username")
    print("3. Enable GitHub Actions in your repository")
    print("4. Set up branch protection rules")
    print("5. Create issues and milestones for future development")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1) 