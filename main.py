import telebot
from config import TELEGRAM_BOT_TOKEN
from handlers import register_all_handlers
from services import init_db
import schedule
import time
import threading
from services.database import get_reminders
from services.crypto_service import get_crypto_price

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Add all handlers
register_all_handlers(bot)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "🚀 Selamat datang di Crypto Bot!\nGunakan /help untuk melihat daftar perintah.")

@bot.message_handler(commands=["help"])
def send_help(message):
    help_text = (
        "📋 Perintah yang tersedia:\n"
        "/setreminder SYMBOL CRON - Buat pengingat harga\n"
        "/myreminders - Lihat reminder aktif\n"
        "/removereminder SYMBOL - Hapus reminder\n\n"
        "/watchlist - Kelola daftar pantauan\n"
        "/watchlist add SYMBOL - Tambah ke watchlist\n"
        "/removewatchlist SYMBOL - Hapus dari watchlist\n\n"
        "/price SYMBOL - Cek harga\n"
        "/help - Tampilkan bantuan"
    )
    bot.reply_to(message, help_text)

def run_scheduler():
    """Loop untuk menjalankan scheduler secara terus menerus."""
    while True:
        schedule.run_pending()
        time.sleep(10)

def check_reminders():
    """Cek reminder yang due dan kirim pesan gabungan ke user."""
    from croniter import croniter
    from datetime import datetime

    reminders = get_reminders()
    now = datetime.now()

    reminders_by_chat = {}

    for chat_id, symbol, cron_expr in reminders:
        cron = croniter(cron_expr, now)
        last_run = cron.get_prev(datetime)
        next_run = cron.get_next(datetime)

        if last_run <= now <= next_run:
            usd_price, idr_price = get_crypto_price(symbol)
            if usd_price and idr_price:
                reminder_text = f"🟡 {symbol}: ${usd_price:,.2f} | Rp{idr_price:,.3f}"
            else:
                reminder_text = f"❌ {symbol} - Gagal mendapatkan harga"

            if chat_id not in reminders_by_chat:
                reminders_by_chat[chat_id] = []
            reminders_by_chat[chat_id].append(reminder_text)

    for chat_id, messages in reminders_by_chat.items():
        final_message = "⏰ Reminder Crypto:\n\n" + "\n".join(messages)
        bot.send_message(chat_id, final_message)

schedule.every(1).minutes.do(check_reminders)

# Jalankan scheduler di thread terpisah
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

if __name__ == "__main__":
    init_db()
    print("✅ Database initialized")
    print("🚀 Bot berjalan...")
    bot.infinity_polling()