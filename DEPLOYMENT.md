# 🚀 PythonAnywhere Deployment Guide

Complete guide to deploy your DMTT Application Bot on PythonAnywhere (100% FREE, 24/7).

---

## 📋 What You'll Get

- ✅ Telegram bot running 24/7
- ✅ Admin panel accessible at: `yourusername.pythonanywhere.com`
- ✅ Completely FREE forever
- ✅ No credit card required

---

## 🎯 Step-by-Step Deployment

### Step 1: Create PythonAnywhere Account

1. Go to: https://www.pythonanywhere.com/registration/register/beginner/
2. Fill in:
   - Username: `samandarpm` (or any name you want)
   - Email: `samandarbekpm@gmail.com`
   - Password: (your choice)
3. Click **"Register"**
4. Verify your email

---

### Step 2: Open Bash Console

1. After logging in, click **"Consoles"** tab
2. Click **"Bash"** under "Start a new console"
3. You'll see a terminal - this is where we'll set everything up

---

### Step 3: Clone Your Repository

In the Bash console, run these commands:

```bash
# Clone your repository
git clone https://github.com/Samandarpm08/ariza.git

# Go into the directory
cd ariza

# Check files are there
ls -la
```

---

### Step 4: Install Dependencies

```bash
# Install required packages
pip3 install --user -r requirements.txt
```

Wait for installation to complete (takes 2-3 minutes).

---

### Step 5: Set Up Environment Variables

```bash
# Create .env file
nano .env
```

In the nano editor, paste this (replace with your actual values):

```
BOT_TOKEN=your_bot_token_here
ADMIN_CHAT_ID=1769729434,6835402377
```

**To save:**
- Press `Ctrl + X`
- Press `Y`
- Press `Enter`

---

### Step 6: Set Up the Web App (Admin Panel)

1. Click **"Web"** tab at the top
2. Click **"Add a new web app"**
3. Click **"Next"** (accept the default domain)
4. Select **"Manual configuration"**
5. Select **"Python 3.10"**
6. Click **"Next"**

---

### Step 7: Configure Web App

On the Web tab, scroll down and configure:

#### A. Source Code
- **Source code:** `/home/samandarpm/ariza`
- **Working directory:** `/home/samandarpm/ariza`

#### B. Virtualenv
- Leave blank (we're using --user installs)

#### C. WSGI Configuration File
Click on the WSGI configuration file link (something like `/var/www/samandarpm_pythonanywhere_com_wsgi.py`)

**Delete everything** and replace with:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/samandarpm/ariza'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

# Import Flask app
from admin_panel import app as application
```

**Save the file** (click "Save" button at top)

---

### Step 8: Reload Web App

1. Go back to the **"Web"** tab
2. Scroll to top
3. Click the big green **"Reload"** button
4. Your admin panel is now live at: `https://samandarpm.pythonanywhere.com`

---

### Step 9: Set Up Telegram Bot (Always-On Task)

PythonAnywhere free tier doesn't support always-on tasks, so we'll use a workaround:

#### Option A: Use "Always-on" Task (Paid Feature - $5/month)

If you upgrade to paid account:
1. Go to **"Tasks"** tab
2. Click **"Create a new scheduled task"**
3. Command: `/home/samandarpm/ariza/bot.py`
4. Schedule: Daily at any time
5. This keeps it running

#### Option B: Keep Bot Running in Console (Free)

1. Go to **"Consoles"** tab
2. Open a **new Bash console**
3. Run:

```bash
cd ariza
python3 bot.py
```

**Important:** This console must stay open. If you close it, the bot stops.

To keep it running even after you close browser:
```bash
cd ariza
nohup python3 bot.py > bot.log 2>&1 &
```

Check if it's running:
```bash
ps aux | grep bot.py
```

---

### Step 10: Test Everything

1. **Test Admin Panel:**
   - Visit: `https://samandarpm.pythonanywhere.com`
   - You should see your dashboard

2. **Test Telegram Bot:**
   - Open Telegram
   - Find your bot
   - Send `/start`
   - Submit a test application

3. **Check Admin Panel:**
   - Refresh the admin panel
   - Your test application should appear

---

## 🔧 Troubleshooting

### Bot Not Responding

```bash
# Check if bot is running
ps aux | grep bot.py

# If not running, start it
cd ariza
python3 bot.py
```

### Admin Panel Shows Error

1. Go to **"Web"** tab
2. Click **"Error log"** 
3. Check what the error is
4. Usually it's missing dependencies - reinstall:
   ```bash
   pip3 install --user -r requirements.txt
   ```

### Can't See Applications

- Make sure `applications.csv` exists:
  ```bash
  cd ariza
  ls -la applications.csv
  ```

---

## 📊 Monitoring

### View Bot Logs

```bash
cd ariza
tail -f bot.log
```

### View Admin Panel Logs

1. Go to **"Web"** tab
2. Click **"Error log"** or **"Server log"**

---

## 🔄 Updating Your Code

When you push changes to GitHub:

```bash
# SSH into PythonAnywhere console
cd ariza

# Pull latest changes
git pull origin main

# Reinstall dependencies if needed
pip3 install --user -r requirements.txt

# Reload web app
# Go to Web tab and click "Reload"

# Restart bot
pkill -f bot.py
nohup python3 bot.py > bot.log 2>&1 &
```

---

## 💡 Pro Tips

1. **Keep Console Open:** The free tier requires keeping a console open for the bot. Use `nohup` to run it in background.

2. **Check Logs Regularly:** Monitor both bot.log and web app logs for errors.

3. **Backup CSV:** Download `applications.csv` regularly as backup.

4. **Upgrade for Always-On:** If you need guaranteed 24/7 bot uptime, upgrade to Hacker plan ($5/month) for always-on tasks.

---

## 🆘 Need Help?

If something doesn't work:

1. Check the error logs
2. Make sure all environment variables are set
3. Verify dependencies are installed
4. Restart both bot and web app

---

## ✅ Final Checklist

- [ ] PythonAnywhere account created
- [ ] Repository cloned
- [ ] Dependencies installed
- [ ] .env file created with BOT_TOKEN and ADMIN_CHAT_ID
- [ ] Web app configured and reloaded
- [ ] Bot running in console
- [ ] Admin panel accessible online
- [ ] Test application submitted successfully

---

**Your URLs:**
- Admin Panel: `https://samandarpm.pythonanywhere.com`
- Telegram Bot: Your bot username from @BotFather

**Congratulations! Your bot is now deployed! 🎉**
