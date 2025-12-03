#!/usr/bin/env python3
"""
Helper script to validate and fix .env file
"""

import re
import os

ENV_FILE = ".env"

print("🔧 Checking .env file...")
print()

if not os.path.exists(ENV_FILE):
    print("❌ .env file not found!")
    print("Please create .env file with:")
    print("BOT_TOKEN=your_token_here")
    print("ADMIN_CHAT_ID=your_chat_id_here")
    exit(1)

# Read .env file
with open(ENV_FILE, 'r') as f:
    content = f.read()

print("Current .env content:")
print("-" * 50)
print(content)
print("-" * 50)
print()

# Parse values
bot_token = None
admin_chat_id = None

for line in content.split('\n'):
    line = line.strip()
    if line.startswith('BOT_TOKEN='):
        bot_token = line.split('=', 1)[1].strip()
    elif line.startswith('ADMIN_CHAT_ID='):
        admin_chat_id = line.split('=', 1)[1].strip()

# Validate BOT_TOKEN
print("✓ Checking BOT_TOKEN...")
if not bot_token:
    print("  ❌ BOT_TOKEN is empty!")
elif bot_token == "your_bot_token_here":
    print("  ❌ BOT_TOKEN is still the placeholder value!")
else:
    print(f"  ✅ BOT_TOKEN is set (length: {len(bot_token)})")

print()

# Validate ADMIN_CHAT_ID
print("✓ Checking ADMIN_CHAT_ID...")
if not admin_chat_id:
    print("  ❌ ADMIN_CHAT_ID is empty!")
elif admin_chat_id == "123456789":
    print("  ❌ ADMIN_CHAT_ID is still the placeholder value!")
else:
    print(f"  📝 Current value: {admin_chat_id}")
    
    # Try to clean it
    cleaned = re.sub(r'[^0-9]', '', admin_chat_id)
    
    if cleaned != admin_chat_id:
        print(f"  ⚠️  Contains non-numeric characters!")
        print(f"  🔧 Cleaned value would be: {cleaned}")
        print()
        
        response = input("  Do you want to fix this? (y/n): ")
        if response.lower() == 'y':
            # Update .env file
            new_content = content.replace(f"ADMIN_CHAT_ID={admin_chat_id}", f"ADMIN_CHAT_ID={cleaned}")
            with open(ENV_FILE, 'w') as f:
                f.write(new_content)
            print("  ✅ Fixed! ADMIN_CHAT_ID updated to:", cleaned)
        else:
            print("  ⏭️  Skipped")
    else:
        print(f"  ✅ ADMIN_CHAT_ID is valid: {admin_chat_id}")

print()
print("=" * 50)
print("Done!")
