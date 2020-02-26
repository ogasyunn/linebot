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
"""
import pymysql
import pymysql.cursors

connection = pymysql.connect(
        host='us-cdbr-iron-east-04.cleardb.net',
        user='bc9fde5ae25666:d6b61d67',
        password='d6b61d67',
        db='mysql',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()                
    finally:
        cursor.close()
        connection.close()
"""
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


#環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(80), unique=True)
    message = db.Column(db.String(80), unique=True)

    def __init__(self, userid, message):
        self.userid = userid
        self.mwssage = message

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    user = User(event.source.user_id, event,message.text)
    db.session.add(User)
    db.session.commit()

    sendmessages = []

    messages = db.session.query(User).all()
    for message in messages:
        sendmessages.append(TextSendMessage(message))
"""
    confirm_template_message = TemplateSendMessage(
        alt_text='Confirm Template',
        template=ConfirmTemplate(
            text='are you ok?',
            actions=[
                PostbackAction(
                    label='postback',
                    display_text='postback text',
                    data='action=buy&itemid=1'
                ),
                MessageAction(
                    label='message',
                    text='I understood'
                )
            ]
        )
    )
"""

    line_bot_api.reply_message(event.reply_token,sendmessages )

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
