from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, FollowEvent, TextMessage, TextSendMessage, ImageSendMessage, VideoSendMessage, StickerSendMessage, AudioSendMessage, TemplateSendMessage,
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
    status = db.Column(db.String(15))

    def __init__(self, groupid, userid, message):
        self.groupid = groupid
        self.userid = userid
        self.message = message
        self.status = status

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

def dealmessage(usermessage, user_id):
    if db.session.query(Instruments).filter(Instruments.userid == "user_id").first() == none :
        instruments.userid = "user_id"
        db.session.add(instruments)
        session.commit()

    instruments = db.session.query(Instruments).filter(Instruments.userid == "user_id").first()
    answer = db.session.query(Answer)
    
    if instruments.status == "registing"
        instruments.message = usermessage
        instruments.status == "registed"
        db.session.add(instruments)
        db.session.commit()
        
        # 確認項目入れる

    if usermessage = "自己紹介":
        message = "次に送るメッセージを登録するね"
        
        instruments.status = "rgisting"
        db.session.add(instruments)
        db.session.commit()
    
@handler.add(FollowEvent)
def follow_event(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="こんにちは！")
        )

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    profile = line_bot_api.get_profile(user_id)
    sendmessage = dealmessage(event.message.text, profile)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=sendmessage)
        )

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
