from telebot import TeleBot
from services.crypto_service import get_crypto_price

def register_price_handlers(bot: TeleBot):
    """Mendaftarkan command untuk cek harga crypto ke bot."""

    @bot.message_handler(commands=["price"])
    def get_price(message):
        try:
            symbol = message.text.split()[1].upper()
            usd_price, idr_price = get_crypto_price(symbol)

            if usd_price is not None and idr_price is not None:
                formatted_usd = f"${usd_price:,.2f}"
                formatted_idr = f"Rp{idr_price:,.3f}"
                bot.reply_to(message, f"🟡 {symbol}\n💰 {formatted_usd} | {formatted_idr}")
            else:
                bot.reply_to(message, f"❌ Gagal mendapatkan harga {symbol}")

        except IndexError:
            bot.reply_to(message, "❌ Gunakan format: /price SYMBOL")
