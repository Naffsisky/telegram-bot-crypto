from .price import register_price_handlers
from .reminders import register_reminder_handlers
from .watchlist import register_watchlist_handlers

def register_all_handlers(bot):
    """Mendaftarkan semua command handlers ke bot."""
    register_price_handlers(bot)
    register_reminder_handlers(bot)
    register_watchlist_handlers(bot)
