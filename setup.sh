#!/bin/bash

# Setup script for DMTT Application Bot

echo "🤖 DMTT Application Bot - Setup"
echo "================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit the .env file and add your:"
    echo "   1. BOT_TOKEN (from @BotFather)"
    echo "   2. ADMIN_CHAT_ID (from @userinfobot)"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Check if python-telegram-bot is installed
echo "🔍 Checking dependencies..."
if python3 -c "import telegram" 2>/dev/null; then
    echo "✅ python-telegram-bot is installed"
else
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
fi

echo ""
echo "================================"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your bot token and admin chat ID"
echo "2. Run: python3 bot.py"
echo ""
echo "For detailed instructions, see README.md"
