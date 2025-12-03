"""
Telegram Bot for DMTT Director Position Applications
Language: Uzbek
Framework: python-telegram-bot v20+

This bot collects applications with name, phone, and PDF document,
saves to CSV, and forwards to admin.
"""

import os
import csv
import re
import logging
from datetime import datetime
from pathlib import Path
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# ============================================================================
# CONFIGURATION
# ============================================================================

# Bot token from BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Admin chat IDs to receive notifications (can be comma-separated for multiple admins)
ADMIN_CHAT_ID_STR = os.getenv("ADMIN_CHAT_ID")

# Validate configuration
if not BOT_TOKEN or BOT_TOKEN == "your_bot_token_here":
    print("❌ ERROR: BOT_TOKEN not set in .env file!")
    print("Please edit .env file and add your bot token from @BotFather")
    exit(1)

if not ADMIN_CHAT_ID_STR or ADMIN_CHAT_ID_STR == "123456789":
    print("❌ ERROR: ADMIN_CHAT_ID not set in .env file!")
    print("Please edit .env file and add your chat ID from @userinfobot")
    exit(1)

# Parse admin chat IDs (support multiple admins separated by comma)
try:
    ADMIN_CHAT_IDS = [int(id.strip()) for id in ADMIN_CHAT_ID_STR.split(',')]
    print(f"✅ Configured {len(ADMIN_CHAT_IDS)} admin(s): {ADMIN_CHAT_IDS}")
except ValueError:
    print("❌ ERROR: ADMIN_CHAT_ID must be a number or comma-separated numbers!")
    print(f"Current value: {ADMIN_CHAT_ID_STR}")
    exit(1)

# CSV file to store applications
CSV_FILE = "applications.csv"

# Conversation states
WAITING_NAME, WAITING_PHONE, WAITING_PDF = range(3)

# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def validate_uzbek_phone(phone: str) -> bool:
    """
    Validate Uzbek phone number format.
    Accepts: +998 XX XXX XX XX or +998XXXXXXXXX or 998XXXXXXXXX
    """
    # Remove spaces and common separators
    cleaned = re.sub(r'[\s\-()]', '', phone)
    
    # Check if it matches Uzbek phone pattern
    pattern = r'^(\+?998)[0-9]{9}$'
    return bool(re.match(pattern, cleaned))

def normalize_phone(phone: str) -> str:
    """Normalize phone number to standard format"""
    cleaned = re.sub(r'[\s\-()]', '', phone)
    if not cleaned.startswith('+'):
        if cleaned.startswith('998'):
            cleaned = '+' + cleaned
        else:
            cleaned = '+998' + cleaned
    return cleaned

def init_csv():
    """Initialize CSV file with headers if it doesn't exist"""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Sana', 'Ism', 'Telefon', 'Username', 
                'Chat ID', 'File ID', 'Fayl nomi'
            ])
        logger.info(f"CSV file created: {CSV_FILE}")

def save_to_csv(data: dict):
    """Save application data to CSV file"""
    try:
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                data['date'],
                data['name'],
                data['phone'],
                data['username'],
                data['chat_id'],
                data['file_id'],
                data['file_name']
            ])
        logger.info(f"Data saved for user: {data['name']}")
        return True
    except Exception as e:
        logger.error(f"Error saving to CSV: {e}")
        return False

# ============================================================================
# CONVERSATION HANDLERS
# ============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Start command handler - begins the application process
    """
    user = update.effective_user
    logger.info(f"User {user.id} (@{user.username}) started the bot")
    
    # Clear any existing data
    context.user_data.clear()
    
    # Send welcome message
    welcome_message = (
        "Farg'ona viloyati maktabgacha va maktab ta'limi boshqarmasi "
        "bo'sh (vakant) DMTT direktori lavozimlariga ochiq tanlov e'lon qiladi.\n\n"
        "Ariza qabul qilish 2025-yil 9-dekabrdan 13-dekabrgacha davom etadi.\n\n"
        "Iltimos, arizani topshirish uchun quyidagi ma'lumotlarni kiriting."
    )
    
    await update.message.reply_text(welcome_message)
    await update.message.reply_text("To'liq ismingizni kiriting:")
    
    return WAITING_NAME

async def receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Receive and validate user's full name
    """
    name = update.message.text.strip()
    
    # Basic validation
    if len(name) < 3:
        await update.message.reply_text(
            "Iltimos, to'liq ismingizni kiriting (kamida 3 ta harf):"
        )
        return WAITING_NAME
    
    # Save name
    context.user_data['name'] = name
    logger.info(f"Name received: {name}")
    
    # Ask for phone number
    await update.message.reply_text(
        "Telefon raqamingizni kiriting (masalan: +998 90 123 45 67):"
    )
    
    return WAITING_PHONE

async def receive_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Receive and validate phone number
    """
    phone = update.message.text.strip()
    
    # Validate phone number
    if not validate_uzbek_phone(phone):
        await update.message.reply_text(
            "❌ Telefon raqam noto'g'ri formatda.\n\n"
            "Iltimos, quyidagi formatda kiriting:\n"
            "+998 90 123 45 67\n"
            "yoki\n"
            "+998901234567\n\n"
            "Qaytadan kiriting:"
        )
        return WAITING_PHONE
    
    # Normalize and save phone
    normalized_phone = normalize_phone(phone)
    context.user_data['phone'] = normalized_phone
    logger.info(f"Phone received: {normalized_phone}")
    
    # Ask for PDF document
    await update.message.reply_text(
        "✅ Telefon raqam qabul qilindi.\n\n"
        "Iltimos, PDF hujjatingizni yuklang:"
    )
    
    return WAITING_PDF

async def receive_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Receive and process PDF document
    """
    # Check if message contains a document
    if not update.message.document:
        await update.message.reply_text(
            "❌ Iltimos, faqat PDF fayl yuboring.\n\n"
            "PDF hujjatingizni yuklang:"
        )
        return WAITING_PDF
    
    document = update.message.document
    
    # Validate file type
    if not document.file_name.lower().endswith('.pdf'):
        await update.message.reply_text(
            "❌ Faqat PDF formatdagi fayllar qabul qilinadi.\n\n"
            "Iltimos, PDF hujjatingizni yuklang:"
        )
        return WAITING_PDF
    
    # Validate file size (max 20MB)
    if document.file_size > 20 * 1024 * 1024:
        await update.message.reply_text(
            "❌ Fayl hajmi juda katta (maksimal 20MB).\n\n"
            "Iltimos, kichikroq PDF fayl yuklang:"
        )
        return WAITING_PDF
    
    user = update.effective_user
    
    # Prepare data for saving
    application_data = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'name': context.user_data['name'],
        'phone': context.user_data['phone'],
        'username': f"@{user.username}" if user.username else "N/A",
        'chat_id': user.id,
        'file_id': document.file_id,
        'file_name': document.file_name
    }
    
    # Save to CSV
    if not save_to_csv(application_data):
        await update.message.reply_text(
            "❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.\n\n"
            "Botni qayta boshlash uchun /start buyrug'ini yuboring."
        )
        return ConversationHandler.END
    
    # Send confirmation to user
    await update.message.reply_text(
        "✅ Arizangiz qabul qilindi. Rahmat!"
    )
    
    # Forward to admin
    try:
        admin_message = (
            "📋 Yangi ariza kelib tushdi:\n\n"
            f"👤 Ism: {application_data['name']}\n"
            f"📱 Telefon: {application_data['phone']}\n"
            f"🆔 Username: {application_data['username']}\n"
            f"📅 Sana: {application_data['date']}\n\n"
            "📄 PDF fayl quyida:"
        )
        
        # Send to all admins
        for admin_id in ADMIN_CHAT_IDS:
            try:
                await context.bot.send_message(
                    chat_id=admin_id,
                    text=admin_message
                )
                
                await context.bot.send_document(
                    chat_id=admin_id,
                    document=document.file_id,
                    caption=f"Ariza: {application_data['name']}"
                )
                
                logger.info(f"Application forwarded to admin {admin_id} for user: {application_data['name']}")
            except Exception as e:
                logger.error(f"Error forwarding to admin {admin_id}: {e}")
        

        
    except Exception as e:
        logger.error(f"Error forwarding to admin: {e}")
        # Don't inform user about admin notification failure
    
    # Clear user data
    context.user_data.clear()
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Cancel the conversation
    """
    context.user_data.clear()
    await update.message.reply_text(
        "❌ Ariza bekor qilindi.\n\n"
        "Qaytadan boshlash uchun /start buyrug'ini yuboring."
    )
    logger.info(f"User {update.effective_user.id} cancelled the conversation")
    return ConversationHandler.END

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Restart command - same as start
    """
    return await start(update, context)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Log errors and notify user
    """
    logger.error(f"Exception while handling an update: {context.error}")
    
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.\n\n"
            "Botni qayta boshlash uchun /start buyrug'ini yuboring."
        )

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """
    Main function to run the bot
    """
    # Initialize CSV file
    init_csv()
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Define conversation handler
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CommandHandler('restart', restart)
        ],
        states={
            WAITING_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name)
            ],
            WAITING_PHONE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_phone)
            ],
            WAITING_PDF: [
                MessageHandler(filters.Document.ALL, receive_pdf),
                MessageHandler(filters.TEXT & ~filters.COMMAND, 
                             lambda u, c: u.message.reply_text(
                                 "❌ Iltimos, PDF fayl yuboring (matn emas)."
                             ))
            ],
        },
        fallbacks=[
            CommandHandler('cancel', cancel),
            CommandHandler('start', start),
            CommandHandler('restart', restart)
        ],
        allow_reentry=True
    )
    
    # Add handlers
    application.add_handler(conv_handler)
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("Bot started successfully!")
    print("✅ Bot ishga tushdi! To'xtatish uchun Ctrl+C bosing.")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
