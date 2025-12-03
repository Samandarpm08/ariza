#!/bin/bash

# Startup script to run both bot and admin panel

echo "🚀 DMTT Application System - Starting..."
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ ERROR: .env file not found!"
    echo "Please create .env file with BOT_TOKEN and ADMIN_CHAT_ID"
    exit 1
fi

# Start the bot in background
echo "🤖 Starting Telegram Bot..."
python3 bot.py &
BOT_PID=$!
echo "✅ Bot started (PID: $BOT_PID)"

# Wait a moment
sleep 2

# Start the admin panel
echo ""
echo "🌐 Starting Admin Panel..."
echo "📊 Dashboard will be available at: http://localhost:5000"
echo ""
echo "🛑 To stop both services, press Ctrl+C"
echo "========================================"
echo ""

# Start admin panel (this will run in foreground)
python3 admin_panel.py

# When admin panel stops, also stop the bot
kill $BOT_PID 2>/dev/null
echo ""
echo "✅ All services stopped"
