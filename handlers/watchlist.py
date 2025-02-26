from services.database import get_watchlist
from services.crypto_service import get_crypto_price
from services.database import remove_watchlist
import telebot

def register_watchlist_handlers(bot: telebot.TeleBot):
    @bot.message_handler(commands=["watchlist"])
    def handle_watchlist(message):
        """Menampilkan watchlist beserta harga terbaru dalam USD dan IDR."""
        chat_id = message.chat.id
        watchlist = get_watchlist(chat_id)

        if not watchlist:
            bot.reply_to(message, "📭 Watchlist kamu kosong. Gunakan /watchlist add SYMBOL untuk menambahkan.")
            return

        watchlist_with_prices = []
        for symbol in watchlist:
            usd_price, idr_price = get_crypto_price(symbol)
            if usd_price and idr_price:
                watchlist_with_prices.append(f"💰 {symbol.upper()} - ${usd_price:,.5f} | Rp{idr_price:,.3f}")
            else:
                watchlist_with_prices.append(f"❌ {symbol.upper()} - Data tidak tersedia")

        watchlist_text = "📌 Watchlist kamu:\n\n" + "\n".join(watchlist_with_prices)
        bot.reply_to(message, watchlist_text)

    print("✅ Watchlist handlers terdaftar!")

    @bot.message_handler(commands=["removewatchlist"])
    def remove_crypto(message):
        try:
            chat_id = message.chat.id
            symbol = message.text.split()[1].upper()

            remove_watchlist(chat_id, symbol)
            bot.reply_to(message, f"✅ {symbol} telah dihapus dari watchlist kamu!")
        
        except IndexError:
            bot.reply_to(message, "❌ Gunakan format: /remove SYMBOL")
