from flask import Flask, request, abort
from dotenv import load_dotenv, find_dotenv
from wit import Wit
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)
load_dotenv(find_dotenv())

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))
client = Wit(os.environ.get('WIT_ACCESS_TOKEN'))


@app.route('/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info('Request body: {}'.format(body))

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    resp = client.message(event.message.text)
    if (resp.get('entities').get('greeting', None) != None):
        resp = resp.get('entities').get('greeting')[0]
        if resp.get('value') == 'hai':
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='Hai! Semoga harimu menyenangkan')
            )
        elif resp.get('value') == 'halo':
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='Halo juga! Semangat buat hari ini :)')
            )


if __name__ == "__main__":
    app.run()
