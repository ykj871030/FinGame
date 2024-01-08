from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from linebot.exceptions import LineBotApiError


#======這裡是呼叫的檔案內容=====
#from message import *
#from new import *
#from Function import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('UJggamRStWntuURfiKYyCfwHKEI+7+28Mv7ZXYsiR+97FGzDMhpVXjibBYis3bFXTfTj4JCb5ufwFty7v+nI9FfwrXbMWrUWd6r0cYMGlzyyB/yXJ2szb9cui6hgih+D+vo5UHk37+ENPcNRIy9lzAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('b202c38b2526a4ca07fec24075461cf4')

# 監聽所有來自 /callback 的 Post Request
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


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    userID = str(event.source.user_id)
    userName = line_bot_api.get_profile(userID).display_name
    if 'Open the door!' in msg:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="你知道門的密碼嗎？\n(輸入密碼時請打：門的密碼是：<密碼> )"))
    elif '門的密碼是' in msg:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="(這邊就會去資料庫判斷玩家的關卡去撈答案出來比對)"))
    else:
        sendContent=TextSendMessage(text=f'userID: {userID}\n{userName} 你說的是：\n{msg}嗎？')
        line_bot_api.reply_message(event.reply_token, sendContent)
    # if '最新合作廠商' in msg:
    #     message = imagemap_message()
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif '最新活動訊息' in msg:
    #     message = buttons_message()
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif '註冊會員' in msg:
    #     message = Confirm_Template()
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif '旋轉木馬' in msg:
    #     message = Carousel_Template()
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif '圖片畫廊' in msg:
    #     message = test()
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif '功能列表' in msg:
    #     message = function_list()
    #     line_bot_api.reply_message(event.reply_token, message)
    # else:
    #     message = TextSendMessage(text=msg)
    #     line_bot_api.reply_message(event.reply_token, message)

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(FollowEvent)
def welcome(event):
    userID = str(event.source.user_id)
    userName = line_bot_api.get_profile(userID).display_name
    message = TextSendMessage(text=f'userID: {userID}\n{userName} 歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
