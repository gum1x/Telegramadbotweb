#!/usr/bin/env python3
"""
Deployment Test Script
Tests all components to ensure no deployment errors
"""

import sys
import os
import json
import asyncio
from datetime import datetime

def test_imports():
    """Test all required imports"""
    print("🔍 Testing imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        import telethon
        print("✅ Telethon imported successfully")
    except ImportError as e:
        print(f"❌ Telethon import failed: {e}")
        return False
    
    try:
        import gevent
        print("✅ Gevent imported successfully")
    except ImportError as e:
        print(f"❌ Gevent import failed: {e}")
        return False
    
    try:
        from flask_socketio import SocketIO
        print("✅ Flask-SocketIO imported successfully")
    except ImportError as e:
        print(f"❌ Flask-SocketIO import failed: {e}")
        return False
    
    return True

def test_web_bot_import():
    """Test web_bot module import"""
    print("\n🔍 Testing web_bot module...")
    
    try:
        import web_bot
        print("✅ web_bot module imported successfully")
    except Exception as e:
        print(f"❌ web_bot import failed: {e}")
        return False
    
    try:
        from web_bot import app, bot
        print("✅ Flask app and bot instance created successfully")
    except Exception as e:
        print(f"❌ App/bot creation failed: {e}")
        return False
    
    return True

def test_config_files():
    """Test configuration files"""
    print("\n🔍 Testing configuration files...")
    
    # Test config.json
    if os.path.exists('config.json'):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            print("✅ config.json exists and is valid JSON")
        except Exception as e:
            print(f"❌ config.json error: {e}")
            return False
    else:
        print("⚠️  config.json not found (will be created on first run)")
    
    # Test groups.txt
    if os.path.exists('groups.txt'):
        try:
            with open('groups.txt', 'r') as f:
                content = f.read()
            print("✅ groups.txt exists")
        except Exception as e:
            print(f"❌ groups.txt error: {e}")
            return False
    else:
        print("⚠️  groups.txt not found (will be created when needed)")
    
    return True

def test_directories():
    """Test required directories"""
    print("\n🔍 Testing directories...")
    
    required_dirs = ['assets', 'assets/sessions', 'templates', 'static', 'static/css', 'static/js']
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path} exists")
        else:
            print(f"❌ {dir_path} missing")
            return False
    
    return True

def test_flask_routes():
    """Test Flask routes"""
    print("\n🔍 Testing Flask routes...")
    
    try:
        from web_bot import app
        
        # Test route registration
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        expected_routes = ['/', '/config', '/api/connect', '/api/authenticate', 
                          '/api/groups', '/api/channels', '/api/forward', 
                          '/api/join-groups', '/api/start-forwarding', 
                          '/api/stop-forwarding', '/api/stats']
        
        for route in expected_routes:
            if route in routes:
                print(f"✅ Route {route} registered")
            else:
                print(f"❌ Route {route} missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Route testing failed: {e}")
        return False

def test_environment():
    """Test environment variables"""
    print("\n🔍 Testing environment...")
    
    # Test Python version
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 8:
        print(f"✅ Python version {python_version.major}.{python_version.minor} is compatible")
    else:
        print(f"❌ Python version {python_version.major}.{python_version.minor} is too old (need 3.8+)")
        return False
    
    # Test working directory
    if os.path.exists('web_bot.py'):
        print("✅ Working directory is correct")
    else:
        print("❌ web_bot.py not found in current directory")
        return False
    
    return True

def main():
    """Run all deployment tests"""
    print("🚀 Starting deployment tests...")
    print("=" * 50)
    
    tests = [
        test_environment,
        test_imports,
        test_web_bot_import,
        test_config_files,
        test_directories,
        test_flask_routes
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print(f"❌ Test {test.__name__} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your deployment is ready.")
        print("\n📝 Next steps:")
        print("1. Configure your Telegram credentials")
        print("2. Run: python web_bot.py")
        print("3. Open: http://localhost:5000")
        return True
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 