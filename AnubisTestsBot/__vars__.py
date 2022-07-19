from decouple import config

BOT_TOKEN = config("BOT_TOKEN")
DATABASE_URL = config("DATABASE_URL", default="sqlite://db.sqlite3")

# WEBHOOK
WEBHOOK = config("WEBHOOK", default=False, cast=bool)
WEBHOOK_URL = config("WEBHOOK_URL", default=None)
WEBHOOK_CERT = config("WEBHOOK_CERT", default=None)
