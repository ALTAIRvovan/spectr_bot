import os
from configparser import ConfigParser

__BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
__CONFIG_PATH = os.path.join(__BASE_DIR, "conf")

__config_name = os.getenv("CONFIG_NAME", "config.cfg")

config = ConfigParser()
config.read(os.path.join(__CONFIG_PATH, __config_name))

broker_url = config.get("CELERY", "BROKER_URL")

GOOGLE_CREDENTIALS_PATH = os.path.join(__CONFIG_PATH, config.get("GOOGLE_CALENDAR", "CREDENTIALS_PATH",
                                                                 fallback="credentials.json"))
GOOGLE_TOKEN_PATH = os.path.join(__CONFIG_PATH, config.get("GOOGLE_CALENDAR", "TOKEN_PATH",
                                                           fallback="token.pickle"))
GOOGLE_SCOPE = list(map(str.strip,
                        config.get("GOOGLE_CALENDAR", "SCOPE",
                                   fallback="https://www.googleapis.com/auth/calendar.readonly").split(";")))

GOOGLE_CALENDAR_ID = config.get("GOOGLE_CALENDAR", "CALENDAR_ID", raw=True)


VK_GROUP_ID = config.getint("VK", "group_id")
VK_CONFIRMATION_TOKEN = config.get("VK", "confirmation_token", raw=True)
VK_CALLBACK_SECRET = config.get("VK", "CALLBACK_SECRET", raw=True)
VK_ACCESS_TOKEN = config.get("VK", "access_token", raw=True)

VK_CURRENT_SPECTRUM_TEAM_CHAT = config.getint("VK", "spectrum_current_team_chat")

BEFORE_TRAIN_NOTIFY_MINUTES = config.getint("SPECTRUM", "minutes_before_training", fallback=60 * 3)
