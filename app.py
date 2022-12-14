from flask import Flask, request, abort

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

line_bot_api = LineBotApi('C09qGlf8MtH3jRsbuEsCUA3xNaOsjra82d+CrfyT3cfAqjdYOJSf6LAaGq/wir4iTIYuWw4hsSG0Sq9W9kSXj0R+9z1DUG5WLsGGsm+j7050FDVbtKGeuLklsMgHq0GgNX6KX027RwN/062PyUDGrQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('37ab057a92dd6cb7c24a104e6575db00')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()