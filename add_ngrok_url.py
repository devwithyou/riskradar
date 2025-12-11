#!/usr/bin/env python3
"""
Helper script to add ngrok URL to Django settings
Usage: python add_ngrok_url.py https://your-ngrok-url.ngrok-free.app
"""
import sys
import re

def add_ngrok_url(ngrok_url):
    """Add ngrok URL to CSRF_TRUSTED_ORIGINS in settings.py"""
    
    # Validate URL
    if not ngrok_url.startswith('https://'):
        print("❌ Error: Ngrok URL must start with https://")
        print("Example: https://xxxx-xx-xx-xxx-xxx.ngrok-free.app")
        sys.exit(1)
    
    if 'ngrok' not in ngrok_url:
        print("❌ Error: This doesn't look like a ngrok URL")
        print("Example: https://xxxx-xx-xx-xxx-xxx.ngrok-free.app")
        sys.exit(1)
    
    settings_file = 'webguard/settings.py'
    
    try:
        # Read current settings
        with open(settings_file, 'r') as f:
            content = f.read()
        
        # Check if URL already exists
        if ngrok_url in content:
            print(f"✅ URL already in settings: {ngrok_url}")
            return
        
        # Find CSRF_TRUSTED_ORIGINS and add the URL
        pattern = r"(CSRF_TRUSTED_ORIGINS = \[[\s\S]*?)(\])"
        
        def replace_func(match):
            origins = match.group(1)
            # Remove any old ngrok URLs
            origins = re.sub(r"\s*'https://[^']*ngrok[^']*',?\n", '', origins)
            # Add new URL
            return f"{origins}    '{ngrok_url}',\n{match.group(2)}"
        
        new_content = re.sub(pattern, replace_func, content)
        
        # Write back
        with open(settings_file, 'w') as f:
            f.write(new_content)
        
        print("✅ Successfully added ngrok URL to settings.py")
        print(f"   URL: {ngrok_url}")
        print("")
        print("⚠️  IMPORTANT: Restart your Django server for changes to take effect!")
        print("   Press Ctrl+C and run: python manage.py runserver")
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find {settings_file}")
        print("   Make sure you're running this from the project root directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python add_ngrok_url.py https://your-ngrok-url.ngrok-free.app")
        print("")
        print("Example:")
        print("  python add_ngrok_url.py https://1234-56-78-910-111.ngrok-free.app")
        sys.exit(1)
    
    ngrok_url = sys.argv[1].strip()
    add_ngrok_url(ngrok_url)


