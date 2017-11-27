from flask import Flask, request, abort
from dotenv import load_dotenv, find_dotenv
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    ButtonsTemplate,
    TemplateSendMessage,
    PostbackTemplateAction,
    MessageTemplateAction,
    URITemplateAction
)

app = Flask(__name__)
load_dotenv(find_dotenv())

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))


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
    if (event.message.text == '/select'):
        reply_message = TemplateSendMessage(
            alt_text='Message not supported',
            template=ButtonsTemplate(
                title='Menu',
                text='Please select action',
                actions=[
                    MessageTemplateAction(
                        label='Say hi!',
                        text='/hi'
                    ),
                    URITemplateAction(
                        label='Go to website',
                        uri='http://example.com/'
                    )
                ]
            )
        )
    elif (event.message.text == '/hi'):
        reply_message = TextSendMessage(text='hi!')
    else:
        reply_message = TextSendMessage(text='Type /select for view main menu')

    line_bot_api.reply_message(
        event.reply_token,
        reply_message
    )


if __name__ == "__main__":
    app.run()
