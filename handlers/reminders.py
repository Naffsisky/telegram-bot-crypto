from telebot import TeleBot
from services.crypto_service import get_crypto_price
from services.database import add_reminder, get_reminders, remove_reminder
from croniter import croniter

def register_reminder_handlers(bot: TeleBot):
    """Mendaftarkan semua command terkait reminder ke bot."""
    
    @bot.message_handler(commands=["setreminder"])
    def set_reminder(message):
        """Menangani perintah /setreminder SYMBOL CRON_EXPRESSION."""
        try:
            args = message.text.split(None, 2)
            if len(args) != 3:
                raise ValueError("Format salah! Gunakan: /setreminder SYMBOL CRON_EXPRESSION")

            symbol = args[1].upper()
            cron_expr = args[2]

            # Validasi format cron
            if not croniter.is_valid(cron_expr):
                bot.reply_to(message, "❌ Format cron tidak valid! Gunakan format yang benar seperti '*/1 * * * *'")
                return

            add_reminder(message.chat.id, symbol, cron_expr)
            bot.reply_to(message, f"✅ Reminder untuk {symbol} ditambahkan dengan jadwal: {cron_expr}")

        except ValueError as e:
            bot.reply_to(message, f"❌ {str(e)}")

    @bot.message_handler(commands=["myreminders"])
    def list_reminders(message):
        """Menampilkan semua reminder yang dibuat pengguna."""
        chat_id = message.chat.id
        reminders = get_reminders(chat_id)

        if not reminders:
            bot.reply_to(message, "📋 Anda tidak memiliki reminder aktif.")
            return

        reminder_list = "\n".join(f"🔔 {symbol}: {cron_expr}" for chat_id, symbol, cron_expr in reminders)

        bot.reply_to(message, f"📋 Reminder Anda:\n{reminder_list}")

    @bot.message_handler(commands=["removereminder"])
    def remove_reminder_cmd(message):
        """Menghapus reminder berdasarkan simbol."""
        try:
            symbol = message.text.split()[1].upper()
            success = remove_reminder(message.chat.id, symbol)

            if success:
                bot.reply_to(message, f"✅ Reminder untuk {symbol} dihapus.")
            else:
                bot.reply_to(message, f"❌ Tidak ada reminder untuk {symbol} ditemukan.")

        except IndexError:
            bot.reply_to(message, "❌ Gunakan format: /removereminder SYMBOL")
