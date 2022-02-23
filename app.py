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

line_bot_api = LineBotApi('kX9gJAY+DEopSznzucozbgGFKLpmKdgV5srflHz1wSaAc6VpLAmgkD0mjN8oEExKLXa7hgAQExW0gV1MsaehBfy3FTd6cIHeMWVhlPLDc3tr6a02Wb/3vRxed2ALESLfeW2UhyoOA1/em8qZUk9lgQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9846cfbcc2c7e39db50849adb418c684')


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