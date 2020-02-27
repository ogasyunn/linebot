from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, FollowEvent, UnfollowEvent, JoinEvent, PostbackEvent, TextMessage, TextSendMessage, ImageSendMessage, VideoSendMessage, StickerSendMessage, AudioSendMessage, TemplateSendMessage,
    ConfirmTemplate, PostbackAction, MessageAction, 
)
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import func

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

class Instruments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groupid = db.Column(db.String(80))
    userid = db.Column(db.String(80))
    message = db.Column(db.String(100))
    status = db.Column(db.String(15))
    icon = db.Column(db.String(200))

    def __init__(self, groupid, userid, message, status, icon):
        self.groupid = groupid
        self.userid = userid
        self.message = message
        self.status = status
        self.icon = icon

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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

def dealmessage(event):

    usermessage = event.message.text
    user_id = event.source.user_id
    messagetype = event.source.type

    if messagetype == "user":

        if db.session.query(Instruments).filter(Instruments.userid == user_id).first() == None:
            instruments = Instruments(None ,user_id ,None ,None ,None)
            db.session.add(instruments)
            db.session.commit()

        instruments = db.session.query(Instruments).filter(Instruments.userid == user_id).first()
        
        if instruments.status == "registing":
            instruments.message = usermessage
            instruments.status == "registed"
            db.session.add(instruments)
            db.session.commit()
            
            message = TemplateSendMessage(
            alt_text='Confirm Template',
            template=ConfirmTemplate(
                text="自己紹介は\n" + usermessage + "\nでいいですか？",
                actions=[
                    PostbackAction(
                        label="もう一回登録する",
                        display_text="もう一回登録する",
                        data="retry"
                    ),
                    PostbackAction(
                        label="これでいいよ",
                        display_text="これでいいよ",
                        data="ok"
                    )
                ]
            )
        )

        if usermessage == "自己紹介":
            message = TextSendMessage(text="次に送るメッセージを自己紹介に登録するね")
            
            instruments.status = "registing"
            db.session.add(instruments)
            db.session.commit()

        elif usermessage == "自分の自己紹介":
            my_instrument = db.session.query(Instruments).filter(Instruments.userid == user_id).first()
            message = TextSendMessage(text=my_instrument.message)

    elif messagetype == "group":

        profile = line_bot_api.get_profile(user_id)
        answer = db.session.query(Answer)
        if db.session.query(Instruments).filter(Instruments.userid == user_id).first() == None:
            instruments = Instruments( event.source.group_id,user_id ,None ,None ,profile.picture_url)
            message = TextSendMessage(text="教えてくれてありがとう！\nよろしくね" + profile.display_name + "さん\n個人のほうで　自己紹介　って言ってみて")
            
        elif db.session.query(Instruments).filter(Instruments.userid == user_id).first() != None:
            instruments = db.session.query(Instruments).filter(Instruments.userid == user_id).first()
            instruments.groupid = event.source.group_id
            instruments.icon = profile.picture_url
            message = TextSendMessage(text="おっ、" + profile.display_name + "さんじゃないか\nこっちでもろしくね")
        
        elif message == "問題":
                
            message = quiz(event)

        db.session.add(instruments)
        db.session.commit()

    return message

def quiz(event):
    
    instruments = db.session.quary(Instruments).filter(Instruments.status == "registed").all()
    quizmember = instruments.userid
    quizmembericon = instruments.icon
    
    count = session.query(func.count(quizmember)) - 1
    num = random(0 ,count)
    answer = Answer(quiznumber[num])
    db.session.add(answed)
    db.session.commit()
    
    memberinstruments = db.session.quary(Instruments).filter(Instruments.userid == answer).first()
    
    contents = []
    
    for i in range(count):
        quizmembername = enent.source.quizemember[i]
        item = QuickReplyButton(action=PostbackAction(imageUrl = quizmembericon[i], label = quizmembername, display_text = quizmembername + "さん", data = quizemember[i]))
        contents.append(item)
    
    message = TextSendMessage(text = memberinstruments.message, quick_reply=QuickReply(items = item))
    
    return message

@handler.add(PostbackEvent)
def postbackevent(event):
    if event.postback.data == "retry":
        instruments = db.session.query(Instruments).filter(Instruments.userid == event.source.user_id).first()
        instruments.status = "registing"
        db.session.add(instruments)
        db.session.commit()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="もう一度自己紹介を入力してね")
            )
    elif event.postback.data == "ok":
        instruments = db.session.query(Instruments).filter(Instruments.userid == event.source.user_id).first()
        instruments.status = "registed"
        db.session.add(instruments)
        db.session.commit()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="登録しました")
            )
    elif event.postback.data == db.session.quary(Instruments).filter(Instruments.userid == answer).first().answer
    
@handler.add(FollowEvent)
def follow_event(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="こんにちは！")
        )

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    sendmessage = dealmessage(event)
    line_bot_api.reply_message(
        event.reply_token,
        sendmessage
        )

@handler.add(JoinEvent)
def joinevent(event):
    group_id = event.source.group_id
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="こんにちは！\n子のアカウントを追加してからみなさんの名前を教えてください")
        )

@handler.add(UnfollowEvent)
def unfollowevent(event):
    if db.session.query(Instruments).filter(Instruments.userid == event.source.user_id).first() != None:

        instruments = db.session.query(Instruments).filter(Instruments.userid == event.source.user_id).first()
        instruments.groupid = None
        instruments.userid = None
        instruments.message = None
        instruments.status = None
        instruments.icon = None
        db.session.add(instruments)
        db.session.commit()

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

