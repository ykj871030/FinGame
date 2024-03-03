# ======呼叫所需的函式庫==========
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from linebot.exceptions import LineBotApiError

import tempfile, os
import datetime
import time

# 使用psycopg2來連接Postgresql
import psycopg2

# ======宣告全域變數==========
app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(
    'UJggamRStWntuURfiKYyCfwHKEI+7+28Mv7ZXYsiR+97FGzDMhpVXjibBYis3bFXTfTj4JCb5ufwFty7v+nI9FfwrXbMWrUWd6r0cYMGlzyyB/yXJ2szb9cui6hgih+D+vo5UHk37+ENPcNRIy9lzAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('b202c38b2526a4ca07fec24075461cf4')

# 設置連線PostgreSQL時所需參數
db_name = "fin_game"
db_user = "fin_game_user"
db_password = "ctS3MTDp4lg6x7rcwtYEJDUs2sfqrr6T"
db_host = "dpg-cmdkqnocmk4c73alfs20-a.singapore-postgres.render.com"
db_port = 5432


# 建立連線函式庫(CREATE, INSERT, UPDATE, ALTER, DELETE用)
def postgreSQLConnect(command):
    # 建立連接
    with psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port) as conn:
        with conn.cursor() as cur:
            # 建立游標
            cur = conn.cursor()
            # 建立SQL指令
            sql_command = command
            # 執行指令
            cur.execute(sql_command)
        # 提交
        conn.commit()


# 建立連線函式庫(SELECT用)
def postgreSQLSelect(command):
    # 建立連接
    with psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port) as conn:
        with conn.cursor() as cur:
            # 建立游標
            cur = conn.cursor()
            # 建立SQL指令
            sql_command = command
            # 執行指令
            cur.execute(sql_command)
            # 將查詢結果儲存
            row = cur.fetchall()
    # 回傳查詢結果
    return row


# 更新使用者所在關卡
def updateUserStage(stage, userID):
    updateStageStatus = f'UPDATE user_info SET user_stage={stage} WHERE user_id=\'{userID}\''
    postgreSQLConnect(updateStageStatus)


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
    # 劇情_前情提要
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

    # 劇情_台詞
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
        talkAbout = '國仁：\n咦？怎麼會有一扇門是開著的？這家銀行的控管也太鬆散了吧！如果我偷偷跑進去應該也不會怎樣吧，反正銀行現在連半個人都沒有。'
        guoSay = TextSendMessage(text=talkAbout)
        line_bot_api.reply_message(event.reply_token, guoSay)

    # 第一關內容
    elif '進入：開著的房間' in msg:
        # 將玩家關卡狀態更新為1
        stage = 1
        userID = str(event.source.user_id)
        updateUserStage(stage, userID)
        stageMessage = ImagemapSendMessage(base_url='https://i.imgur.com/CIe6qtf.png',
                                           alt_text='room_1_opne',
                                           base_size=BaseSize(height=1040, width=1040),
                                           actions=[MessageImagemapAction(text='(1)地板小卡',
                                                                          area=ImagemapArea(x=195, y=890, width=158,
                                                                                            height=105)),
                                                    MessageImagemapAction(text='(1)關燈',
                                                                          area=ImagemapArea(x=898, y=449, width=118,
                                                                                            height=161))
                                                    ]
                                           )
        line_bot_api.reply_message(event.reply_token, stageMessage)
    elif '(1)開燈' in msg:
        stageMessage = ImagemapSendMessage(base_url='https://i.imgur.com/CIe6qtf.png',
                                           alt_text='room_1_opne',
                                           base_size=BaseSize(height=1040, width=1040),
                                           actions=[MessageImagemapAction(text='(1)地板小卡',
                                                                          area=ImagemapArea(x=195, y=890, width=158,
                                                                                            height=105)),
                                                    MessageImagemapAction(text='(1)關燈',
                                                                          area=ImagemapArea(x=898, y=449, width=118,
                                                                                            height=161))
                                                    ]
                                           )
        line_bot_api.reply_message(event.reply_token, stageMessage)
    elif '(1)關燈' in msg:
        stageMessage = ImagemapSendMessage(base_url='https://i.imgur.com/yASWBYr.png',
                                           alt_text='room_1_close',
                                           base_size=BaseSize(height=1040, width=1040),
                                           actions=[MessageImagemapAction(text='(1)地板小卡',
                                                                          area=ImagemapArea(x=195, y=890, width=158,
                                                                                            height=105)),
                                                    MessageImagemapAction(text='(1)開燈',
                                                                          area=ImagemapArea(x=898, y=449, width=118,
                                                                                            height=161))
                                                    ]
                                           )
        line_bot_api.reply_message(event.reply_token, stageMessage)
    elif '(1)地板小卡' in msg:
        message = ImageSendMessage(original_content_url='https://i.imgur.com/mer9ofa.png',
                                   preview_image_url='https://i.imgur.com/mer9ofa.png')
        line_bot_api.reply_message(event.reply_token, message)

    # 第二關內容
    elif '進入：MARKET...?' in msg:
        # 此處需要用到SQL來確認玩家是否處在第二關
        stageMessage = ImagemapSendMessage(base_url='https://i.imgur.com/9BqvJZc.png',
                                           alt_text='room_2',
                                           base_size=BaseSize(height=1040, width=1040),
                                           actions=[MessageImagemapAction(text='(2)牆上的照片',
                                                                          area=ImagemapArea(x=8, y=223, width=144,
                                                                                            height=519)),
                                                    MessageImagemapAction(text='(2)書架',
                                                                          area=ImagemapArea(x=169, y=239, width=296,
                                                                                            height=394)),
                                                    MessageImagemapAction(text='(2)陳列架',
                                                                          area=ImagemapArea(x=888, y=322, width=149,
                                                                                            height=367))
                                                    ]
                                           )
        line_bot_api.reply_message(event.reply_token, stageMessage)
    elif '(2)牆上的照片' in msg:
        imagemapMessage = ImagemapSendMessage(base_url='https://i.imgur.com/1EnVfrM.png',
                                              alt_text='room_2_picture',
                                              base_size=BaseSize(height=1040, width=1040),
                                              actions=[MessageImagemapAction(text='(2)照片後的黃紙',
                                                                             area=ImagemapArea(x=678, y=690, width=85,
                                                                                               height=125))
                                                       ]
                                              )
        line_bot_api.reply_message(event.reply_token, imagemapMessage)
    elif '(2)照片後的黃紙' in msg:
        replyArray = []
        replyArray.append(ImageSendMessage(original_content_url='https://i.imgur.com/oAvS1BB.png',
                                           preview_image_url='https://i.imgur.com/oAvS1BB.png'))
        replyArray.append(TextSendMessage(
            text="GDP 國內生產總值(Gross Domestic Product)\n指一個國家在一定時期內生產的所有商品和服務的價值總和。"))
        replyArray.append(AudioSendMessage(
            original_content_url='https://files.soundoftext.com/61f41240-58be-11ee-a44a-8501b7b1aefa.mp3',
            duration=3000))
        line_bot_api.reply_message(event.reply_token, replyArray)
        replyArray.clear()
    elif '(2)書架' in msg:
        message = ImageSendMessage(original_content_url='https://i.imgur.com/WofIzXf.png',
                                   preview_image_url='https://i.imgur.com/WofIzXf.png')
        line_bot_api.reply_message(event.reply_token, message)
    elif '(2)陳列架' in msg:
        message = ImageSendMessage(original_content_url='https://i.imgur.com/paVuOhm.png',
                                   preview_image_url='https://i.imgur.com/paVuOhm.png')
        line_bot_api.reply_message(event.reply_token, message)

    # 第三關內容
    elif '進入：機房' in msg:
        # 此處需要用到SQL來確認玩家是否處在第三關
        stageMessage = ImagemapSendMessage(base_url='https://i.imgur.com/71MDD45.png',
                                           alt_text='room_3',
                                           base_size=BaseSize(height=1040, width=1040),
                                           actions=[MessageImagemapAction(text='(3)電腦',
                                                                          area=ImagemapArea(x=165, y=436, width=224,
                                                                                            height=175)),
                                                    MessageImagemapAction(text='(3)桌上的紙',
                                                                          area=ImagemapArea(x=386, y=553, width=120,
                                                                                            height=75)),
                                                    MessageImagemapAction(text='(3)打開抽屜',
                                                                          area=ImagemapArea(x=385, y=636, width=124,
                                                                                            height=218))
                                                    ]
                                           )
        line_bot_api.reply_message(event.reply_token, stageMessage)
    elif '(3)電腦' in msg:
        # 電腦需要顯示文字(如輸入以及密碼提示)
        replyArray = []
        replyArray.append(ImageSendMessage(original_content_url='https://i.imgur.com/M0JjBY6.png',
                                           preview_image_url='https://i.imgur.com/M0JjBY6.png'))
        replyArray.append(TextSendMessage(text="你知道電腦的密碼嗎？\n(輸入密碼時請輸入：\n電腦的密碼是 XXXXX)"))
        line_bot_api.reply_message(event.reply_token, replyArray)
        replyArray.clear()
    elif '(3)桌上的紙' in msg:
        message = ImageSendMessage(original_content_url='https://i.imgur.com/h0bBBQV.png',
                                   preview_image_url='https://i.imgur.com/h0bBBQV.png')
        line_bot_api.reply_message(event.reply_token, message)
    elif '(3)打開抽屜' in msg:
        imagemapMessage = ImagemapSendMessage(base_url='https://i.imgur.com/9MCsd0J.png',
                                              alt_text='room_3_drawer',
                                              base_size=BaseSize(height=1040, width=1040),
                                              actions=[MessageImagemapAction(text='(3)抽屜裡的東西',
                                                                             area=ImagemapArea(x=410, y=180, width=567,
                                                                                               height=475))
                                                       ]
                                              )
        line_bot_api.reply_message(event.reply_token, imagemapMessage)
    elif '(3)抽屜裡的東西' in msg:
        replyArray = []
        replyArray.append(ImageSendMessage(original_content_url='https://i.imgur.com/GSkijUS.png',
                                           preview_image_url='https://i.imgur.com/GSkijUS.png'))
        replyArray.append(TemplateSendMessage(alt_text='room_3_Bplate',
                                              template=ButtonsTemplate(title='是一個有奇怪記號的...墊板？',
                                                                       text="總感覺疊在桌上的紙上面會發現什麼訊息，要疊上去嗎？",
                                                                       actions=[MessageAction(label="要",
                                                                                              text="(3)將墊板疊在紙上"
                                                                                              ),
                                                                                MessageAction(label="不要",
                                                                                              text="(3)不疊"
                                                                                              )
                                                                                ]
                                                                       )
                                              )
                          )
        line_bot_api.reply_message(event.reply_token, replyArray)
        replyArray.clear()

    elif '(3)將墊板疊在紙上' in msg:
        message = ImageSendMessage(original_content_url='https://i.imgur.com/RptQK1X.png',
                                   preview_image_url='https://i.imgur.com/RptQK1X.png')
        line_bot_api.reply_message(event.reply_token, message)
    elif '(3)不疊' in msg:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text="(將墊板放回抽屜裡...)"))
    # 其他控制選項
    elif '開門！' in msg:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text="你知道門的密碼嗎？\n(輸入密碼時請輸入：\n門的密碼是 XXXXX)"))
    elif '(國仁正思考著...)' in msg:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text="會去資料庫撈提示。"))
    elif '門的密碼是' in msg:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text="(這邊就會去資料庫判斷玩家的關卡去撈答案出來比對)"))
    elif '電腦的密碼是' in msg:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(
                                       text="(這邊就會去判斷電腦的密碼後，給予相對應的回覆，正確就是圖片，錯誤就是文字)"))
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
            replyArray.clear()
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
    try:
        query = f'SELECT * FROM user_info WHERE user_id=\'{userID}\''
        datas = postgreSQLSelect(query)
        if len(datas) == 0:
            addUserSQL = f'INSERT INTO user_info(user_id, user_name, user_stage) VALUES(\'{userID}\',\'{userName}\',0);'
            postgreSQLConnect(addUserSQL)
        message = TextSendMessage(
            text=f'{userName} 您好，歡迎你加入Fin Game！\n你將會在Fin Game的世界學到\n有關金融報導的英文單字。\n若你已經準備好的話，請輸入「開始遊戲」吧！')
        line_bot_api.reply_message(event.reply_token, message)
    except Exception as e:
        app.logger.error(f'Create user information error:{e}')


import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
