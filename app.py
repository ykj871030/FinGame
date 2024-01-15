from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from linebot.exceptions import LineBotApiError

# ======這裡是呼叫的檔案內容=====
# from message import *
# from new import *
# from Function import *
# ======這裡是呼叫的檔案內容=====

# ======python的函數庫==========
import tempfile, os
import datetime
import time

# ======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(
    'UJggamRStWntuURfiKYyCfwHKEI+7+28Mv7ZXYsiR+97FGzDMhpVXjibBYis3bFXTfTj4JCb5ufwFty7v+nI9FfwrXbMWrUWd6r0cYMGlzyyB/yXJ2szb9cui6hgih+D+vo5UHk37+ENPcNRIy9lzAdB04t89/1O/w1cDnyilFU=')
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
    if '開始遊戲' in msg:
        story_carousel_template_message = TemplateSendMessage(alt_text='Carousel template',
                                                              template=CarouselTemplate(columns=[
                                                                  CarouselColumn(
                                                                      thumbnail_image_url='https://i.imgur.com/RgBlFpa.png',
                                                                      title='國仁要去銀行',
                                                                      text='國仁目前想要投資金融市場，所以前往銀行，詢問理財專員。',
                                                                      actions=[
                                                                          MessageAction(
                                                                              label='國仁說：',
                                                                              text='(0-1)國仁說：'
                                                                          ), MessageAction(
                                                                              label='<<<左滑<<<',
                                                                              text='<<<左滑<<<'
                                                                          )
                                                                      ]
                                                                  ), CarouselColumn(
                                                                      thumbnail_image_url='https://i.imgur.com/kF5g7ri.png',
                                                                      title='國仁抽號碼牌',
                                                                      text='國仁到了銀行，遵守排隊原則，抽了張號碼牌。',
                                                                      actions=[
                                                                          MessageAction(
                                                                              label='國仁說：',
                                                                              text='(0-2)國仁說：'
                                                                          ), MessageAction(
                                                                              label='<<<左滑<<<',
                                                                              text='<<<左滑<<<'
                                                                          )
                                                                      ]
                                                                  ), CarouselColumn(
                                                                      thumbnail_image_url='https://i.imgur.com/F8ho4aP.png',
                                                                      title='國仁發現銀行的人都消失了',
                                                                      text='抽完號碼牌的國仁發現，原本在銀行的人突然都不見了。',
                                                                      actions=[
                                                                          MessageAction(
                                                                              label='國仁說：',
                                                                              text='(0-3)國仁說：'
                                                                          ), MessageAction(
                                                                              label='<<<左滑<<<',
                                                                              text='<<<左滑<<<'
                                                                          )
                                                                      ]
                                                                  ), CarouselColumn(
                                                                      thumbnail_image_url='https://i.imgur.com/3vu72hU.png',
                                                                      title='國仁看見有扇門是開著的',
                                                                      text='但銀行內竟然有扇門是開著的，出自於好奇，國仁決定走進去一探究竟。',
                                                                      actions=[
                                                                          MessageAction(
                                                                              label='國仁說：',
                                                                              text='(0-4)國仁說：'
                                                                          ), MessageAction(
                                                                              label='進入房間：',
                                                                              text='進入：開著的房間'
                                                                          )
                                                                      ]
                                                                  )
                                                              ]
                                                              )
                                                              )
        line_bot_api.reply_message(event.reply_token, story_carousel_template_message)
    # 劇情
    elif '(0-1)國仁說：' in msg:
        talkAbout = '國仁：\n最近剛賺了一筆，手上的閒置資金不知道要做什麼？你不理財，財不理你，閒著也是閒著，不如去銀行詢問理財專員吧！'
        guoSay = TextSendMessage(text=talkAbout)
        line_bot_api.reply_message(event.reply_token, guoSay)
    elif '(0-2)國仁說：' in msg:
        talkAbout = '國仁：\n找了理財專員才發現我還有很多手續要辦理，反正我也是第一次理財，就抽抽號碼牌，等櫃檯叫號吧！希望會被分配到妹子櫃檯。'
        guoSay = TextSendMessage(text=talkAbout)
        line_bot_api.reply_message(event.reply_token, guoSay)
    elif '(0-3)國仁說：' in msg:
        talkAbout = '國仁：\n今天銀行沒什麼人，看來也不需要排隊了，真幸運！不對，這是什麼情況？怎麼連櫃檯的人都沒有？難不成下班了嗎？我也才剛到銀行欸！。'
        guoSay = TextSendMessage(text=talkAbout)
        line_bot_api.reply_message(event.reply_token, guoSay)
    elif '(0-4)國仁說：' in msg:
        talkAbout = '國仁：\n咦？怎麼會有一扇門是開著的？這家銀行的控管誒太鬆散了吧！如果我偷偷跑進去應該也不會怎樣吧，反正銀行現在連半個人都沒有。'
        guoSay = TextSendMessage(text=talkAbout)
        line_bot_api.reply_message(event.reply_token, guoSay)
    # 第一關內容
    elif '進入：開著的房間' in msg:
        # 此處需要用到SQL來確認玩家是否處在第一關
        stageMessage = ImagemapSendMessage(base_url='https://i.imgur.com/CIe6qtf.png',
                                           alt_text='room_1_opne',
                                           base_size=BaseSize(height=1024, width=1024),
                                           actions=[MessageImagemapAction(text='(1)地板小卡：',
                                                                          area=ImagemapArea(x=195, y=890, width=158,
                                                                                            height=105)),
                                                    MessageImagemapAction(text='(1)關燈：',
                                                                          area=ImagemapArea(x=898, y=449, width=118,
                                                                                            height=161)),
                                                    ]
                                           )
        line_bot_api.reply_message(event.reply_token, stageMessage)
    elif '(1)開燈：' in msg:
        stageMessage = ImagemapSendMessage(base_url='https://i.imgur.com/CIe6qtf.png',
                                           alt_text='room_1_opne',
                                           base_size=BaseSize(height=1024, width=1024),
                                           actions=[MessageImagemapAction(text='(1)地板小卡：',
                                                                          area=ImagemapArea(x=195, y=890, width=158,
                                                                                            height=105)),
                                                    MessageImagemapAction(text='(1)關燈：',
                                                                          area=ImagemapArea(x=898, y=449, width=118,
                                                                                            height=161)),
                                                    ]
                                           )
        line_bot_api.reply_message(event.reply_token, stageMessage)
    elif '(1)關燈：' in msg:
        stageMessage = ImagemapSendMessage(base_url='https://i.imgur.com/yASWBYr.png',
                                           alt_text='room_1_close',
                                           base_size=BaseSize(height=1024, width=1024),
                                           actions=[MessageImagemapAction(text='(1)地板小卡：',
                                                                          area=ImagemapArea(x=195, y=890, width=158,
                                                                                            height=105)),
                                                    MessageImagemapAction(text='(1)開燈：',
                                                                          area=ImagemapArea(x=898, y=449, width=118,
                                                                                            height=161)),
                                                    ]
                                           )
        line_bot_api.reply_message(event.reply_token, stageMessage)
    elif '(1)地板小卡：' in msg:
        message = ImageSendMessage(original_content_url='https://i.imgur.com/mer9ofa.png',
                                   preview_image_url='https://i.imgur.com/mer9ofa.png')
        line_bot_api.reply_message(event.reply_token, message)
    elif 'Open the door!' in msg:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text="你知道門的密碼嗎？\n(輸入密碼時請打：門的密碼是：<密碼> )"))
    elif '門的密碼是' in msg:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text="(這邊就會去資料庫判斷玩家的關卡去撈答案出來比對)"))
    elif '<<<左滑<<<' in msg:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text="左滑看故事"))
    elif 'inflation' in msg:
        try:
            replyArray = []
            replyArray.append(TextSendMessage(text="inflation 通膨\n一種經濟現象，指一段時間內物價上升的幅度。"))
            replyArray.append(AudioSendMessage(
                original_content_url='https://files.soundoftext.com/ad64dd70-67df-11ed-a44a-8501b7b1aefa.mp3',
                duration=1000))
            line_bot_api.reply_message(event.reply_token, replyArray)
        except Exception as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(e)))
    else:
        sendContent = TextSendMessage(text=f'userID: {userID}\n{userName} 你說的是：\n{msg}嗎？')
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


# 加入好友的時候會跳出的訊息
@handler.add(FollowEvent)
def welcome(event):
    userID = str(event.source.user_id)
    userName = line_bot_api.get_profile(userID).display_name
    message = TextSendMessage(
        text=f'{userName} 您好，歡迎你加入Fin Game！\n你將會在Fin Game的世界學到\n有關金融報導的英文單字。\n若你已經準備好的話，請輸入「開始遊戲」吧！')
    line_bot_api.reply_message(event.reply_token, message)


import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
