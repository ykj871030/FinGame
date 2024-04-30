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
app.json.ensure_ascii = False
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(
    'UJggamRStWntuURfiKYyCfwHKEI+7+28Mv7ZXYsiR+97FGzDMhpVXjibBYis3bFXTfTj4JCb5ufwFty7v+nI9FfwrXbMWrUWd6r0cYMGlzyyB/yXJ2szb9cui6hgih+D+vo5UHk37+ENPcNRIy9lzAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('b202c38b2526a4ca07fec24075461cf4')

# 設置連線PostgreSQL時所需參數
db_name = "fin_game_v0bs"
db_user = "fin_game_user"
db_password = "3owEq7LIqYwZ51if6TlHqAtS3BiQftiq"
db_host = "dpg-co8vvgtjm4es73an6sig-a.singapore-postgres.render.com"
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


# 取得使用者所在關卡
def getUserStage(userID):
    getUserStage = f'SELECT user_stage FROM user_info WHERE user_id=\'{userID}\''
    datas = postgreSQLSelect(getUserStage)
    return datas[0][0]


# 網站測試
@app.route("/FinGameReview")
def FinGameReview():
    html = '''
    <!DOCTYPE html>
    <html lang="zh-Hant-TW">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
            <title>FinGame Review</title>
        </head>
        <body>
            <div style="width:100%; height:60px; text-align:center;">
                <h1>FinGame Review</h1>
            </div>
    '''
    vocabularySQL = '''
                    SELECT no, vocabulary, translate, meaning, speak_url
                    FROM vocabulary_info
                    ORDER BY no ASC
                    '''
    rows = postgreSQLSelect(vocabularySQL)
    for row in rows:
        html += f'''
        <div style="width:100%; height:320px; text-align:center;">
            <table border="1" style="width:100%; height:320px; text-align:center; font-size: 1.5rem;">
                <tr>
                    <td style="width:50%; height:80px;"><b>{row[1]}</b></td>
                    <td style="width:50%; height:80px;">{row[2]}</td>
                </tr>
                <tr>
                    <td colspan="2" style="width:100%; height:80px;"><audio src="{row[4]}" controls style="width:50%;"></audio></td>
                </tr>
                <tr>
                    <td colspan="2" align="left" style="width:100%; height:100px;">{row[3]}</td>
                </tr>
            </table>
        </div>
        <br><br><br>
        '''
    html += '''
        </body>
    </html>
    '''
    return html


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
    if "Start" in msg:
        query = f'SELECT * FROM user_info WHERE user_id=\'{userID}\''
        datas = postgreSQLSelect(query)
        if len(datas) == 0:
            addUserSQL = f'INSERT INTO user_info(user_id, user_name, user_stage) VALUES(\'{userID}\',\'{userName}\',0);'
            postgreSQLConnect(addUserSQL)
        story_carousel_template_message = TemplateSendMessage(alt_text='Carousel template',
                                                              template=CarouselTemplate(columns=[
                                                                  CarouselColumn(
                                                                      thumbnail_image_url='https://i.imgur.com/RgBlFpa.png',
                                                                      title="Guoren wants to invest.",
                                                                      text="So he meets the financial planning personnel.",
                                                                      actions=[
                                                                          MessageAction(
                                                                              label="Guoren says:",
                                                                              text="(0-1)Guoren says:"
                                                                          ), MessageAction(
                                                                              label="<<Swipe left<<",
                                                                              text="<<Swipe left<<"
                                                                          )
                                                                      ]
                                                                  ), CarouselColumn(
                                                                      thumbnail_image_url='https://i.imgur.com/kF5g7ri.png',
                                                                      title="Guoren took a number.",
                                                                      text="Guoren arrived at the bank, and took a number",
                                                                      actions=[
                                                                          MessageAction(
                                                                              label="Guoren says:",
                                                                              text="(0-2)Guoren says:"
                                                                          ), MessageAction(
                                                                              label="<<Swipe left<<",
                                                                              text="<<Swipe left<<"
                                                                          )
                                                                      ]
                                                                  ), CarouselColumn(
                                                                      thumbnail_image_url='https://i.imgur.com/F8ho4aP.png',
                                                                      title="After taking the number plate.",
                                                                      text="Guoren found that everyone suddenly disappeared.",
                                                                      actions=[
                                                                          MessageAction(
                                                                              label="Guoren says:",
                                                                              text="(0-3)Guoren says:"
                                                                          ), MessageAction(
                                                                              label="<<Swipe left<<",
                                                                              text="<<Swipe left<<"
                                                                          )
                                                                      ]
                                                                  ), CarouselColumn(
                                                                      thumbnail_image_url='https://i.imgur.com/3vu72hU.png',
                                                                      title="Surprisingly, there was an open door.",
                                                                      text="Guoren decides to go inside and find out what's going on.",
                                                                      actions=[
                                                                          MessageAction(
                                                                              label="Guoren says:",
                                                                              text="(0-4)Guoren says:"
                                                                          ), MessageAction(
                                                                              label="Enter the room",
                                                                              text="Enter the open room"
                                                                          )
                                                                      ]
                                                                  )
                                                              ]
                                                              )
                                                              )
        line_bot_api.reply_message(event.reply_token, story_carousel_template_message)

    # 劇情_台詞
    elif "(0-1)Guoren says:" in msg:
        talkAbout = '''Guoren:\nI have idle assets recently. As the saying goes, "If you don't care about your money, your money won't care about you". Let's go and meet with the financial planning personnel.'''
        guoSay = TextSendMessage(text=talkAbout)
        line_bot_api.reply_message(event.reply_token, guoSay)
    elif "(0-2)Guoren says:" in msg:
        talkAbout = '''Guoren:\nI have a lot of paperwork to do. I'll wait for my number to be called. I hope I'll be assigned to a female teller.'''
        guoSay = TextSendMessage(text=talkAbout)
        line_bot_api.reply_message(event.reply_token, guoSay)
    elif "(0-3)Guoren says:" in msg:
        talkAbout = '''Guoren:\nThere's no line at the bank today, lucky me! No, what's going on here? Why is there no one at the counter? Is it closing time? I just got to the bank!'''
        guoSay = TextSendMessage(text=talkAbout)
        line_bot_api.reply_message(event.reply_token, guoSay)
    elif "(0-4)Guoren says:" in msg:
        talkAbout = '''Guoren:\nHuh? Why is there an open door? The control of this bank is too loose, isn't it? I don't think it would be a problem if I sneaked in. There's no one in the bank right now.'''
        guoSay = TextSendMessage(text=talkAbout)
        line_bot_api.reply_message(event.reply_token, guoSay)

    # 第一關內容
    elif 'Enter the open room' in msg:
        # 將玩家關卡狀態更新為1
        stage = 1
        updateUserStage(stage, userID)
        stageMessage = ImagemapSendMessage(base_url='https://i.imgur.com/CIe6qtf.png',
                                           alt_text='room_1_opne',
                                           base_size=BaseSize(height=1040, width=1040),
                                           actions=[MessageImagemapAction(text='(1)Orange paper',
                                                                          area=ImagemapArea(x=195, y=890, width=158,
                                                                                            height=105)),
                                                    MessageImagemapAction(text='(1)Turn off the light',
                                                                          area=ImagemapArea(x=898, y=449, width=118,
                                                                                            height=161))
                                                    ]
                                           )
        line_bot_api.reply_message(event.reply_token, stageMessage)
    elif '(1)Turn on the light' in msg:
        # 要確認玩家是否在第一關
        userStage = getUserStage(userID)
        if userStage == 1:
            stageMessage = ImagemapSendMessage(base_url='https://i.imgur.com/CIe6qtf.png',
                                               alt_text='room_1_opne',
                                               base_size=BaseSize(height=1040, width=1040),
                                               actions=[MessageImagemapAction(text='(1)Orange paper',
                                                                              area=ImagemapArea(x=195, y=890, width=158,
                                                                                                height=105)),
                                                        MessageImagemapAction(text='(1)Turn off the light',
                                                                              area=ImagemapArea(x=898, y=449, width=118,
                                                                                                height=161))
                                                        ]
                                               )
        elif userStage == 0:
            stageMessage = TemplateSendMessage(alt_text='start_game',
                                               template=ButtonsTemplate(title='Are you ready?',
                                                                        text="Click \"Start\" to join FinGame!",
                                                                        actions=[MessageAction(label="Start!",
                                                                                               text="Start"
                                                                                               )]))
        else:
            stageMessage = TextSendMessage(text='Guoren: Um...')
        line_bot_api.reply_message(event.reply_token, stageMessage)
    elif '(1)Turn off the light' in msg:
        # 要確認玩家是否在第一關
        userStage = getUserStage(userID)
        if userStage == 1:
            stageMessage = ImagemapSendMessage(base_url='https://i.imgur.com/yASWBYr.png',
                                               alt_text='room_1_close',
                                               base_size=BaseSize(height=1040, width=1040),
                                               actions=[MessageImagemapAction(text='(1)Orange paper',
                                                                              area=ImagemapArea(x=195, y=890, width=158,
                                                                                                height=105)),
                                                        MessageImagemapAction(text='(1)Turn on the light',
                                                                              area=ImagemapArea(x=898, y=449, width=118,
                                                                                                height=161))
                                                        ]
                                               )
        elif userStage == 0:
            stageMessage = TemplateSendMessage(alt_text='start_game',
                                               template=ButtonsTemplate(title='Are you ready?',
                                                                        text="Click \"Start\" to join FinGame!",
                                                                        actions=[MessageAction(label="Start!",
                                                                                               text="Start"
                                                                                               )]))
        else:
            stageMessage = TextSendMessage(text='Guoren: Um...')
        line_bot_api.reply_message(event.reply_token, stageMessage)
    elif '(1)Orange paper' in msg:
        # 要確認玩家是否在第一關
        userStage = getUserStage(userID)
        if userStage == 1:
            message = ImageSendMessage(original_content_url='https://i.imgur.com/mer9ofa.png',
                                       preview_image_url='https://i.imgur.com/mer9ofa.png')
        elif userStage == 0:
            message = TemplateSendMessage(alt_text='start_game',
                                          template=ButtonsTemplate(title='Are you ready?',
                                                                   text="Click \"Start\" to join FinGame!",
                                                                   actions=[MessageAction(label="Start!",
                                                                                          text="Start"
                                                                                          )]))
        else:
            message = TextSendMessage(text='Guoren: Um...')
        line_bot_api.reply_message(event.reply_token, message)

    # 第二關內容
    elif 'Enter the MARKET...?' in msg:
        # 要確認玩家是否在第二關
        userStage = getUserStage(userID)
        if userStage == 2:
            stageMessage = ImagemapSendMessage(base_url='https://i.imgur.com/9BqvJZc.png',
                                               alt_text='room_2',
                                               base_size=BaseSize(height=1040, width=1040),
                                               actions=[MessageImagemapAction(text='(2)portrait',
                                                                              area=ImagemapArea(x=8, y=223, width=144,
                                                                                                height=519)),
                                                        MessageImagemapAction(text='(2)bookshelf',
                                                                              area=ImagemapArea(x=169, y=239, width=296,
                                                                                                height=394)),
                                                        MessageImagemapAction(text='(2)Display stands',
                                                                              area=ImagemapArea(x=888, y=322, width=149,
                                                                                                height=367))
                                                        ]
                                               )
        elif userStage == 0:
            stageMessage = TemplateSendMessage(alt_text='start_game',
                                               template=ButtonsTemplate(title='Are you ready?',
                                                                        text="Click \"Start\" to join FinGame!",
                                                                        actions=[MessageAction(label="Start!",
                                                                                               text="Start"
                                                                                               )]))
        else:
            stageMessage = TextSendMessage(text='Guoren: Um...')
        line_bot_api.reply_message(event.reply_token, stageMessage)
    elif '(2)portrait' in msg:
        # 要確認玩家是否在第二關
        userStage = getUserStage(userID)
        if userStage == 2:
            imagemapMessage = ImagemapSendMessage(base_url='https://i.imgur.com/1EnVfrM.png',
                                                  alt_text='room_2_picture',
                                                  base_size=BaseSize(height=1040, width=1040),
                                                  actions=[MessageImagemapAction(text='(2)yellow paper',
                                                                                 area=ImagemapArea(x=678, y=690,
                                                                                                   width=85,
                                                                                                   height=125))
                                                           ]
                                                  )
        elif userStage == 0:
            imagemapMessage = TemplateSendMessage(alt_text='start_game',
                                                  template=ButtonsTemplate(title='Are you ready?',
                                                                           text="Click \"Start\" to join FinGame!",
                                                                           actions=[MessageAction(label="Start!",
                                                                                                  text="Start"
                                                                                                  )]))
        else:
            imagemapMessage = TextSendMessage(text='Guoren: Um...')
        line_bot_api.reply_message(event.reply_token, imagemapMessage)
    elif '(2)yellow paper' in msg:
        # 要確認玩家是否在第二關
        userStage = getUserStage(userID)
        if userStage == 2:
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
        elif userStage == 0:
            message = TemplateSendMessage(alt_text='start_game',
                                          template=ButtonsTemplate(title='Are you ready?',
                                                                   text="Click \"Start\" to join FinGame!",
                                                                   actions=[MessageAction(label="Start!",
                                                                                          text="Start"
                                                                                          )]))
            line_bot_api.reply_message(event.reply_token, message)
        else:
            message = TextSendMessage(text='Guoren: Um...')
            line_bot_api.reply_message(event.reply_token, message)
    elif '(2)bookshelf' in msg:
        # 要確認玩家是否在第二關
        userStage = getUserStage(userID)
        if userStage == 2:
            message = ImageSendMessage(original_content_url='https://i.imgur.com/WofIzXf.png',
                                       preview_image_url='https://i.imgur.com/WofIzXf.png')
        elif userStage == 0:
            message = TemplateSendMessage(alt_text='start_game',
                                          template=ButtonsTemplate(title='Are you ready?',
                                                                   text="Click \"Start\" to join FinGame!",
                                                                   actions=[MessageAction(label="Start!",
                                                                                          text="Start"
                                                                                          )]))
        else:
            message = TextSendMessage(text='Guoren: Um...')
        line_bot_api.reply_message(event.reply_token, message)
    elif '(2)Display stands' in msg:
        # 要確認玩家是否在第二關
        userStage = getUserStage(userID)
        if userStage == 2:
            message = ImageSendMessage(original_content_url='https://i.imgur.com/paVuOhm.png',
                                       preview_image_url='https://i.imgur.com/paVuOhm.png')
        elif userStage == 0:
            message = TemplateSendMessage(alt_text='start_game',
                                          template=ButtonsTemplate(title='Are you ready?',
                                                                   text="Click \"Start\" to join FinGame!",
                                                                   actions=[MessageAction(label="Start!",
                                                                                          text="Start"
                                                                                          )]))
        else:
            message = TextSendMessage(text='Guoren: Um...')
        line_bot_api.reply_message(event.reply_token, message)

    # 第三關內容
    elif 'Enter the IDC' in msg:
        # 要確認玩家是否在第三關
        userStage = getUserStage(userID)
        if userStage == 3:
            stageMessage = ImagemapSendMessage(base_url='https://i.imgur.com/71MDD45.png',
                                               alt_text='room_3',
                                               base_size=BaseSize(height=1040, width=1040),
                                               actions=[MessageImagemapAction(text='(3)computer',
                                                                              area=ImagemapArea(x=165, y=436, width=224,
                                                                                                height=175)),
                                                        MessageImagemapAction(text='(3)paper',
                                                                              area=ImagemapArea(x=386, y=553, width=120,
                                                                                                height=75)),
                                                        MessageImagemapAction(text='(3)Open the drawer',
                                                                              area=ImagemapArea(x=385, y=636, width=124,
                                                                                                height=218))
                                                        ]
                                               )
        elif userStage == 0:
            stageMessage = TemplateSendMessage(alt_text='start_game',
                                               template=ButtonsTemplate(title='Are you ready?',
                                                                        text="Click \"Start\" to join FinGame!",
                                                                        actions=[MessageAction(label="Start!",
                                                                                               text="Start"
                                                                                               )]))
        else:
            stageMessage = TextSendMessage(text='Guoren: Um...')
        line_bot_api.reply_message(event.reply_token, stageMessage)
    elif '(3)computer' in msg:
        # 要確認玩家是否在第三關
        userStage = getUserStage(userID)
        if userStage == 3:
            replyArray = []
            replyArray.append(ImageSendMessage(original_content_url='https://i.imgur.com/M0JjBY6.png',
                                               preview_image_url='https://i.imgur.com/M0JjBY6.png'))
            replyArray.append(TextSendMessage(text="Do you know the password to your computer?\n(Input Format: \npassword is XXXXX)"))
            line_bot_api.reply_message(event.reply_token, replyArray)
            replyArray.clear()
        elif userStage == 0:
            stageMessage = TemplateSendMessage(alt_text='start_game',
                                               template=ButtonsTemplate(title='Are you ready?',
                                                                        text="Click \"Start\" to join FinGame!",
                                                                        actions=[MessageAction(label="Start!",
                                                                                               text="Start"
                                                                                               )]))
            line_bot_api.reply_message(event.reply_token, stageMessage)
        else:
            stageMessage = TextSendMessage(text='Guoren: Um...')
            line_bot_api.reply_message(event.reply_token, stageMessage)
    elif '(3)paper' in msg:
        # 要確認玩家是否在第三關
        userStage = getUserStage(userID)
        if userStage == 3:
            message = ImageSendMessage(original_content_url='https://i.imgur.com/h0bBBQV.png',
                                       preview_image_url='https://i.imgur.com/h0bBBQV.png')
        elif userStage == 0:
            message = TemplateSendMessage(alt_text='start_game',
                                          template=ButtonsTemplate(title='Are you ready?',
                                                                   text="Click \"Start\" to join FinGame!",
                                                                   actions=[MessageAction(label="Start!",
                                                                                          text="Start"
                                                                                          )]))
        else:
            message = TextSendMessage(text='Guoren: Um...')
        line_bot_api.reply_message(event.reply_token, message)
    elif '(3)Open the drawer' in msg:
        # 要確認玩家是否在第三關
        userStage = getUserStage(userID)
        if userStage == 3:
            imagemapMessage = ImagemapSendMessage(base_url='https://i.imgur.com/9MCsd0J.png',
                                                  alt_text='room_3_drawer',
                                                  base_size=BaseSize(height=1040, width=1040),
                                                  actions=[MessageImagemapAction(text='(3)Item in the drawer',
                                                                                 area=ImagemapArea(x=410, y=180,
                                                                                                   width=567,
                                                                                                   height=475))
                                                           ]
                                                  )
        elif userStage == 0:
            imagemapMessage = TemplateSendMessage(alt_text='start_game',
                                                  template=ButtonsTemplate(title='Are you ready?',
                                                                           text="Click \"Start\" to join FinGame!",
                                                                           actions=[MessageAction(label="Start!",
                                                                                                  text="Start"
                                                                                                  )]))
        else:
            imagemapMessage = TextSendMessage(text='Guoren: Um...')
        line_bot_api.reply_message(event.reply_token, imagemapMessage)
    elif '(3)Item in the drawer' in msg:
        # 要確認玩家是否在第三關
        userStage = getUserStage(userID)
        if userStage == 3:
            replyArray = []
            replyArray.append(ImageSendMessage(original_content_url='https://i.imgur.com/GSkijUS.png',
                                               preview_image_url='https://i.imgur.com/GSkijUS.png'))
            replyArray.append(TemplateSendMessage(alt_text='room_3_Bplate',
                                                  template=ButtonsTemplate(title="It's a pad with a strange marking on it.",
                                                                           text="Do you want to stack it on top of the paper on the table?",
                                                                           actions=[MessageAction(label="Yes",
                                                                                                  text="(3)Stack the pad on the paper"
                                                                                                  ),
                                                                                    MessageAction(label="No",
                                                                                                  text="(3)Don't stack"
                                                                                                  )
                                                                                    ]
                                                                           )
                                                  )
                              )
            line_bot_api.reply_message(event.reply_token, replyArray)
            replyArray.clear()
        elif userStage == 0:
            stageMessage = TemplateSendMessage(alt_text='start_game',
                                               template=ButtonsTemplate(title='Are you ready?',
                                                                        text="Click \"Start\" to join FinGame!",
                                                                        actions=[MessageAction(label="Start!",
                                                                                               text="Start"
                                                                                               )]))
            line_bot_api.reply_message(event.reply_token, stageMessage)
        else:
            stageMessage = TextSendMessage(text='Guoren: Um...')
            line_bot_api.reply_message(event.reply_token, stageMessage)
    elif '(3)Stack the pad on the paper' in msg:
        # 要確認玩家是否在第三關
        userStage = getUserStage(userID)
        if userStage == 3:
            message = ImageSendMessage(original_content_url='https://i.imgur.com/RptQK1X.png',
                                       preview_image_url='https://i.imgur.com/RptQK1X.png')
        elif userStage == 0:
            message = TemplateSendMessage(alt_text='start_game',
                                          template=ButtonsTemplate(title='Are you ready?',
                                                                   text="Click \"Start\" to join FinGame!",
                                                                   actions=[MessageAction(label="Start!",
                                                                                          text="Start"
                                                                                          )]))
        else:
            message = TextSendMessage(text='Guoren: Um...')
        line_bot_api.reply_message(event.reply_token, message)
    elif 'Don\'t stack' in msg:
        # 要確認玩家是否在第三關
        userStage = getUserStage(userID)
        if userStage == 3:
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(text="(Put the pad back in the drawer...)"))
        elif userStage == 0:
            line_bot_api.reply_message(event.reply_token, TemplateSendMessage(alt_text='start_game',
                                                                              template=ButtonsTemplate(
                                                                                  title='Are you ready?',
                                                                                  text="Click \"Start\" to join FinGame!",
                                                                                  actions=[
                                                                                      MessageAction(label="Start!",
                                                                                                    text="Start"
                                                                                                    )])))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Guoren: Um...'))
    # 其他控制選項
    elif 'Open the door!' in msg:
        userStage = getUserStage(userID)
        if userStage == 0:
            line_bot_api.reply_message(event.reply_token, TemplateSendMessage(alt_text='start_game',
                                                                              template=ButtonsTemplate(
                                                                                  title='Are you ready?',
                                                                                  text="Click \"Start\" to join FinGame!",
                                                                                  actions=[
                                                                                      MessageAction(label="Start!",
                                                                                                    text="Start"
                                                                                                    )])))
        elif userStage == 4:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(
                text='Click "REVIEW" to review the financial terminology you learned at FinGame!'))
        else:
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(text="Do you know the code to the door?\n(Input Format: \nthe door code is XXXXX)"))
    elif 'Hint' in msg:
        hintSQL = f'''
        SELECT u.user_id, u.user_stage, s.hint
        FROM user_info u LEFT JOIN stage_info s ON u.user_stage = s.stage
        WHERE u.user_id = '{userID}'
        '''
        datas = postgreSQLSelect(hintSQL)
        stage = datas[0][1]
        if stage == 0:
            line_bot_api.reply_message(event.reply_token,
                                       TemplateSendMessage(alt_text='start_game',
                                                           template=ButtonsTemplate(title='Are you ready?',
                                                                                    text="Click \"Start\" to join FinGame!",
                                                                                    actions=[
                                                                                        MessageAction(label="Start!",
                                                                                                      text="Start"
                                                                                                      )])))
        elif stage == 4:
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(
                                           text='Click "REVIEW" to review the financial terminology you learned at FinGame!'))
        else:
            hint = datas[0][2]
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(text=hint))
    elif 'the door code is' in msg.lower():
        answerSQL = f'''
        SELECT u.user_id, u.user_stage, s.answer, v.vocabulary
        FROM user_info u
        LEFT JOIN stage_info s ON u.user_stage = s.stage
        LEFT JOIN vocabulary_info v ON s.answer = v.no
        WHERE u.user_id = '{userID}'
        '''
        datas = postgreSQLSelect(answerSQL)
        stage = datas[0][1]
        if stage == 0:
            line_bot_api.reply_message(event.reply_token,
                                       TemplateSendMessage(alt_text='start_game',
                                                           template=ButtonsTemplate(title='Are you ready?',
                                                                                    text="Click \"Start\" to join FinGame!",
                                                                                    actions=[
                                                                                        MessageAction(label="Start!",
                                                                                                      text="Start"
                                                                                                      )])))
        elif stage == 4:
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(
                                           text='Click "REVIEW" to review the financial terminology you learned at FinGame!'))
        else:
            replyArray = []
            if stage == 3:
                trueAnswer = datas[0][2].lower()
            else:
                trueAnswer = datas[0][3].lower()
            ans = msg.split('is')[1]
            ansRS = ans.strip().lower()
            # 去看玩家輸入的英文有沒有在單字庫裡
            vocabularySQL = f'''
            SELECT vocabulary, translate, meaning, speak_url, millisecond
            FROM vocabulary_info
            WHERE vocabulary = '{ansRS}'
            '''
            rows = postgreSQLSelect(vocabularySQL)
            if len(rows) != 0:
                voc = rows[0][0]
                trans = rows[0][1]
                mean = rows[0][2]
                url = rows[0][3]
                sec = rows[0][4]
                replyArray.append(TextSendMessage(text=f"{voc} {trans}\n{mean}"))
                replyArray.append(AudioSendMessage(original_content_url=url, duration=sec))

            # 判斷是否為答案
            if ansRS == trueAnswer:
                updateUserStage(stage + 1, userID)
                if stage == 3:
                    replyArray.append(TemplateSendMessage(alt_text='open_door',
                                                          template=ButtonsTemplate(title='The door is open!',
                                                                                   text='It was accompanied by a white light and a distinct shaking.',
                                                                                   actions=[
                                                                                       MessageAction(
                                                                                           label=trueAnswer.upper() + "!",
                                                                                           text=trueAnswer.upper() + "!"
                                                                                       )
                                                                                   ]
                                                                                   )
                                                          )
                                      )
                else:
                    nextSQL = f"SELECT stage, stage_name FROM stage_info WHERE stage ='{stage + 1}'"
                    datas = postgreSQLSelect(nextSQL)
                    stageName = datas[0][1]
                    replyArray.append(TemplateSendMessage(alt_text='open_door',
                                                          template=ButtonsTemplate(title='The door is open!',
                                                                                   text="Guoren: It's my lucky day! I'm pretty awesome!",
                                                                                   actions=[
                                                                                       MessageAction(label="Enter the room",
                                                                                                     text=f'Enter the {stageName}'
                                                                                                     )
                                                                                   ]
                                                                                   )
                                                          )
                                      )
            else:
                replyArray.append(TextSendMessage(text=f"Wrong password! Please try again later."))
            line_bot_api.reply_message(event.reply_token, replyArray)
            replyArray.clear()
    elif 'password is' in msg.lower():
        computerSQL = f'''
        SELECT u.user_id, u.user_stage, c.pwd, c.hint
        FROM user_info u
        LEFT JOIN computer_pwd c ON u.user_stage = c.stage
        WHERE u.user_id = '{userID}'
        '''
        datas = postgreSQLSelect(computerSQL)
        stage = datas[0][1]
        truePwd = datas[0][2]
        hint = datas[0][3]
        if stage == 0:
            line_bot_api.reply_message(event.reply_token,
                                       TemplateSendMessage(alt_text='start_game',
                                                           template=ButtonsTemplate(title='Are you ready?',
                                                                                    text="Click \"Start\" to join FinGame!",
                                                                                    actions=[
                                                                                        MessageAction(label="Start!",
                                                                                                      text="Start"
                                                                                                      )])))
        elif stage == 4:
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(
                                           text='Click "REVIEW" to review the financial terminology you learned at FinGame!'))
        elif stage == 3:
            replyArray = []
            pwd = msg.split('is')[1]
            pwdRS = pwd.strip().lower()

            # 去看玩家輸入的英文有沒有在單字庫裡
            vocabularySQL = f'''
                        SELECT vocabulary, translate, meaning, speak_url, millisecond
                        FROM vocabulary_info
                        WHERE vocabulary = '{pwdRS}'
                        '''
            rows = postgreSQLSelect(vocabularySQL)
            if len(rows) != 0:
                voc = rows[0][0]
                trans = rows[0][1]
                mean = rows[0][2]
                url = rows[0][3]
                sec = rows[0][4]
                replyArray.append(TextSendMessage(text=f"{voc} {trans}\n{mean}"))
                replyArray.append(AudioSendMessage(original_content_url=url, duration=sec))
            # 判斷是否為電腦密碼
            if pwdRS == truePwd:
                replyArray.append(ImageSendMessage(original_content_url='https://i.imgur.com/WmZVxZk.png',
                                                   preview_image_url='https://i.imgur.com/WmZVxZk.png'))
            else:
                replyArray.append(TextSendMessage(text=f"Wrong password! Please try again later.\nNote: No symbols included."))
                replyArray.append(TextSendMessage(text=f"{hint}"))
            line_bot_api.reply_message(event.reply_token, replyArray)
            replyArray.clear()
    elif '<<Swipe left<<' in msg:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text="Swipe left for stories."))
    elif 'WAKEUP!' in msg:
        userStage = getUserStage(userID)
        if userStage == 0:
            message = TemplateSendMessage(alt_text='start_game',
                                          template=ButtonsTemplate(title='Are you ready?',
                                                                   text="Click \"Start\" to join FinGame!",
                                                                   actions=[MessageAction(label="Start!",
                                                                                          text="Start"
                                                                                          )]))
        elif userStage == 4:
            message = TemplateSendMessage(alt_text='Carousel template',
                                          template=CarouselTemplate(columns=[
                                              CarouselColumn(
                                                  thumbnail_image_url='https://i.imgur.com/alt97CB.png',
                                                  title='Guoren is woken up by a bank teller.',
                                                  text="Everything is Guoren's dream!",
                                                  actions=[
                                                      MessageAction(
                                                          label='Guoren says:',
                                                          text='(END-1)Guoren says:'
                                                      ), MessageAction(
                                                          label='<<Swipe left<<',
                                                          text='<<Swipe left<<'
                                                      )
                                                  ]
                                              ), CarouselColumn(
                                                  thumbnail_image_url='https://i.imgur.com/WJpKVks.png',
                                                  title='Guoren will become a financial guru.',
                                                  text='Guoren will enter the financial investment market.',
                                                  actions=[
                                                      MessageAction(
                                                          label='Guoren says:',
                                                          text='(END-2)Guoren says:'
                                                      ), MessageAction(
                                                          label='Game over',
                                                          text='Game over'
                                                      )
                                                  ]
                                              )
                                          ]
                                          )
                                          )
        else:
            message = TextSendMessage(text="(It seems that an inexplicable force is calling out to Guoren. But Guoren did not think so....)")
        line_bot_api.reply_message(event.reply_token, message)

    # 遊戲結尾
    elif '(END-1)Guoren says:' in msg:
        userStage = getUserStage(userID)
        if userStage == 0:
            guoSay = TemplateSendMessage(alt_text='start_game',
                                         template=ButtonsTemplate(title='Are you ready?',
                                                                  text="Click \"Start\" to join FinGame!",
                                                                  actions=[MessageAction(label="Start!",
                                                                                         text="Start"
                                                                                         )]))
        elif userStage == 4:
            talkInTheEnd = '''Guoren:\nI fell asleep! It's embarrassing. What kind of bank has such poor control? It was just a dream. It doesn't matter. There's nothing more important than being woken up by a female banker. I'm here to do my paperwork.'''
            guoSay = TextSendMessage(text=talkInTheEnd)
        else:
            guoSay = TextSendMessage(text='Guoren: Um...')
        line_bot_api.reply_message(event.reply_token, guoSay)
    elif '(END-2)Guoren says:' in msg:
        userStage = getUserStage(userID)
        if userStage == 0:
            guoSay = TemplateSendMessage(alt_text='start_game',
                                         template=ButtonsTemplate(title='Are you ready?',
                                                                  text="Click \"Start\" to join FinGame!",
                                                                  actions=[MessageAction(label="Start!",
                                                                                         text="Start"
                                                                                         )]))
        elif userStage == 4:
            talkInTheEnd = '''Guoren:\nHa-ha-ha! Everything is ready! The world's second Warren Buffett is about to be born! I'm getting ready to enter the financial markets!'''
            guoSay = TextSendMessage(text=talkInTheEnd)
        else:
            guoSay = TextSendMessage(text='Guoren: Um...')
        line_bot_api.reply_message(event.reply_token, guoSay)
    elif 'Game over' in msg:
        userStage = getUserStage(userID)
        if userStage == 0:
            message = TemplateSendMessage(alt_text='start_game',
                                          template=ButtonsTemplate(title='Are you ready?',
                                                                   text="Click \"Start\" to join FinGame!",
                                                                   actions=[MessageAction(label="Start!",
                                                                                          text="Start"
                                                                                          )]))
        elif userStage == 4:
            message = TextSendMessage(
                text='Congratulations!!!\n\nHopefully, you will learn some financial terminology during the game. Learning these words will help you when you read financial news in English in the future.\n\nIf you want to review these terminology, you can open the rich menus and click "REVIEW".\n\nFinGame would like to thanks for playing!')
        else:
            message = TextSendMessage(text='Guoren: Um...')
        line_bot_api.reply_message(event.reply_token, message)

    # 複習單字
    elif 'Review vocabulary' in msg:
        userStage = getUserStage(userID)
        if userStage == 0:
            message = TemplateSendMessage(alt_text='start_game',
                                          template=ButtonsTemplate(title='Are you ready?',
                                                                   text="Click \"Start\" to join FinGame!",
                                                                   actions=[MessageAction(label="Start!",
                                                                                          text="Start"
                                                                                          )]))
        elif userStage == 4:
            message = TextSendMessage(
                text="Let’s review financial terminology we learned in FinGame together!\nhttps://fingame-glb9.onrender.com/FinGameReview")
        else:
            message = TextSendMessage(text='Guoren: Um...')
        line_bot_api.reply_message(event.reply_token, message)

    # 輸入其他文字的時候
    else:
        userStage = getUserStage(userID)
        if userStage == 0:
            message = TemplateSendMessage(alt_text='start_game',
                                          template=ButtonsTemplate(title='Are you ready?',
                                                                   text="Click \"Start\" to join FinGame!",
                                                                   actions=[MessageAction(label="Start!",
                                                                                          text="Start"
                                                                                          )]))
        elif userStage == 4:
            message = TextSendMessage(text='Click "REVIEW" to review the financial terminology you learned at FinGame!')
        else:
            message = TextSendMessage(text='Guoren: Um...')
        line_bot_api.reply_message(event.reply_token, message)


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
            text=f'Hello {userName}, welcome to join FinGame!\nYou will learn financial terminology at FinGame.\n\nDuring the game, if you need to enter an answer or need a hint, you can open the rich menus and click the button.\n\nIf FinGame does not respond, you will need to enter any input and wait 1 minute before continuing to play.\n\nIf you are ready, \nplease enter "Start" !')
        line_bot_api.reply_message(event.reply_token, message)
    except Exception as e:
        app.logger.error(f'Create user information error:{e}')


import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
