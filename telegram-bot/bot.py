import logging
import urllib.parse as urlparser

import requests


# TODO:
# viber-bot-python: https://github.com/Viber/viber-bot-python


TG_BOT_NAME = ''
TG_BOT_TOKEN = ''
TG_CHAT_ID = ''
TG_CHANNEL_ID = ''


class SomeNameBot:

    logger = logging.getLogger(__name__)

    def send_tg_alert(self):
        url = urlparser.urljoin(self._bot_url(), 'sendMessage')
        headers = {
            'Content-Type': 'application/json',
        }
        params = {
            'chat_id': TG_CHANNEL_ID,
            'text': 'test text',
        }
        resp = requests.post(url, params=params, headers=headers)

    def _bot_url(self):
        return urlparser.urljoin('https://api.telegram.org/bot/', TG_BOT_TOKEN)
