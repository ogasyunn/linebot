from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, VideoSendMessage, StickerSendMessage, AudioSendMessage, TemplateSendMessage,
    ConfirmTemplate, PostbackAction, MessageAction
)
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


#環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

class Instruments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groupid = db.Column(db.string(80))
    userid = db.Column(db.String(80))
    message = db.Column(db.String(100))

    def __init__(self, groupid, userid, message):
        self.groupid = groupid
        self.userid = userid
        self.message = message

class Answer(dbModel):
    id = db.column(db.Integer, primary_key=True)
    answer = db.Column(db.String(80))

    def __init__(self, answer):
        self.answer = answer

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
        abort(400)

    return 'OK'

@hanndler.add(FollowEvent)
def follow_event(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="こんにちは！")
        )

def register():
    groupid = 

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
