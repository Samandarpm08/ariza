# DMTT Director Application Bot

Telegram bot for collecting applications for DMTT Director positions in Fergana region.

## Features

✅ **Multi-step form** with state management  
✅ **Phone validation** for Uzbek numbers (+998)  
✅ **PDF document** upload and validation  
✅ **CSV storage** for all applications  
✅ **Admin notifications** with forwarded documents  
✅ **Error handling** and restart capability  
✅ **Uzbek language** interface  

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Your Bot

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the bot token you receive

### 3. Get Your Admin Chat ID

1. Open Telegram and search for [@userinfobot](https://t.me/userinfobot)
2. Send `/start` to get your chat ID
3. Copy the ID number

### 4. Configure Environment Variables

Create a `.env` file or set environment variables:

```bash
export BOT_TOKEN="your_bot_token_here"
export ADMIN_CHAT_ID="your_chat_id_here"
```

Or edit the `bot.py` file directly and replace:
- `YOUR_BOT_TOKEN_HERE` with your actual bot token
- `123456789` with your actual admin chat ID

### 5. Run the Bot

```bash
python bot.py
```

You should see: `✅ Bot ishga tushdi! To'xtatish uchun Ctrl+C bosing.`

## Usage

### User Commands

- `/start` - Start the application process
- `/restart` - Restart the application from beginning
- `/cancel` - Cancel current application

### Application Flow

1. User sends `/start`
2. Bot asks for full name
3. Bot asks for phone number (validates Uzbek format)
4. Bot asks for PDF document
5. Bot saves data to CSV and forwards to admin
6. User receives confirmation message

### Data Storage

All applications are saved to `applications.csv` with the following fields:

- Date and time
- Full name
- Phone number
- Telegram username
- Chat ID
- File ID
- File name

### Admin Notifications

When a user submits an application, the admin receives:

1. A message with user details
2. The uploaded PDF document

## Phone Number Validation

The bot accepts Uzbek phone numbers in these formats:

- `+998 90 123 45 67`
- `+998901234567`
- `998901234567`

All numbers are normalized to `+998XXXXXXXXX` format.

## Error Handling

- Invalid phone numbers prompt re-entry
- Non-PDF files are rejected
- Files larger than 20MB are rejected
- All errors are logged
- Users can restart at any time with `/start` or `/restart`

## File Structure

```
Ariza/
├── bot.py              # Main bot code
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
├── README.md          # This file
└── applications.csv   # Generated when first application is received
```

## Troubleshooting

### Bot doesn't respond
- Check if bot token is correct
- Ensure bot is running (`python bot.py`)
- Check internet connection

### Admin not receiving notifications
- Verify admin chat ID is correct
- Make sure admin has started a chat with the bot first

### CSV file not created
- Check write permissions in the directory
- Look for error messages in console

## Security Notes

⚠️ **Important:**
- Never commit `.env` file or bot token to version control
- Keep `applications.csv` secure (contains personal data)
- Regularly backup the CSV file
- Consider adding `.env` and `applications.csv` to `.gitignore`

## Production Deployment

For production use, consider:

1. **Use environment variables** instead of hardcoded values
2. **Deploy on a server** (VPS, cloud platform)
3. **Use process manager** like `systemd` or `pm2`
4. **Set up logging** to file for monitoring
5. **Regular backups** of CSV data
6. **Consider database** instead of CSV for larger scale

### Example systemd service

Create `/etc/systemd/system/dmtt-bot.service`:

```ini
[Unit]
Description=DMTT Application Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/Ariza
Environment="BOT_TOKEN=your_token"
Environment="ADMIN_CHAT_ID=your_id"
ExecStart=/usr/bin/python3 /path/to/Ariza/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable dmtt-bot
sudo systemctl start dmtt-bot
```

## License

This bot is created for Fergana Region Education Department.
