import os
#for image search
import urllib
import re
import random
#database
import psycopg2

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)

def send_guide_flex(reply_token) :
    try :
        contents = {    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "請選擇一個選項", "size": "md", "weight": "bold"}
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "spacer", "size": "xxl"},
                            {   "type": "button", "style": "secondary", "height": "sm",
                                "action": {"type": "message", "text": "我現在想吃...", "label": "我現在想吃..."}},
                            {"type": "text", "text": " ", "size": "xxs", "weight": "bold"},
                            {   "type": "button", "style": "secondary", "height": "sm",
                                "action": {"type": "message", "text": "小幫手推薦...", "label": "小幫手推薦..."}},
                            {"type": "text", "text": " ", "size": "xxs", "weight": "bold"},
                            {   "type": "button", "style": "secondary", "height": "sm",
                                "action": {"type": "message", "text": "紀錄一下我吃了什麼", "label": "紀錄一下我吃了什麼"}},
                            {"type": "text", "text": " ", "size": "xxs", "weight": "bold"},
                            {   "type": "button", "style": "secondary", "height": "sm",
                                "action": {"type": "message", "text": "看看過去我吃了什麼", "label": "看看過去我吃了什麼"}}
                        ]
                    }
                }
        line_bot_api = LineBotApi(channel_access_token)        
        line_bot_api.reply_message(
            reply_token,
            FlexSendMessage(
                alt_text = "來選擇一項服務吧!",
                contents = contents
            )
        )
        return True
    except :
        return False

def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_ask_image_flex(reply_token) :
    try :
        contents = {    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "您現在想吃 ...", "size": "md", "weight": "bold"}
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "spacer", "size": "xxl"},
                            {   "type": "button", "style": "secondary", "height": "sm",
                                "action": {"type": "message", "text": "中式料理", "label": "中式料理"}},
                            {"type": "text", "text": " ", "size": "xxs", "weight": "bold"},
                            {   "type": "button", "style": "secondary", "height": "sm",
                                "action": {"type": "message", "text": "日式料理", "label": "日式料理"}},
                            {"type": "text", "text": " ", "size": "xxs", "weight": "bold"},
                            {   "type": "button", "style": "secondary", "height": "sm",
                                "action": {"type": "message", "text": "美式料理", "label": "美式料理"}},
                            {"type": "text", "text": " ", "size": "xxs", "weight": "bold"},
                            {   "type": "button", "style": "secondary", "height": "sm",
                                "action": {"type": "message", "text": "義式料理", "label": "義式料理"}},
                            {"type": "text", "text": " ", "size": "xl", "weight": "bold"},
                            {"type": "text", "text": "沒有您的選項嗎？也可以直接輸入喔～", "size": "sm", "weight": "bold", "color": "#aaaaaa"},
                        ]
                    }
                }
        line_bot_api = LineBotApi(channel_access_token)        
        line_bot_api.reply_message(
            reply_token,
            FlexSendMessage(
                alt_text = "您想吃什麼呢～",
                contents = contents
            )
        )
        return True
    except :
        return False

def send_image_flex(reply_token, target) :
    try :
        random_img_url = get_img_url(img_source = 'google', target = (target))
        contents = prepare_img_search_flex("您想吃... ", target + " !", random_img_url)
        line_bot_api = LineBotApi(channel_access_token)        
        line_bot_api.reply_message(
            reply_token,
            FlexSendMessage(
                alt_text = "小幫手幫您找到囉!",
                contents = contents
            )
        )
        return True
    except :
        return False

def send_and_recommand(event) :
    data = search_table()[0]

    max_index = []
    for i in range(1, 5) :
        if data[i] == max(data[1:]) :
            max_index.append(i)
            i = i + 1
    index = random.choice(max_index)

    text = "根據您過去的吃飯紀錄，\n小幫手推薦您 ...\n\n\t"
    if index == 1 :
        text += "中式料理！"
    elif index == 2 :
        text += "日式料理！"
    elif index == 3 :
        text += "美式料理！"
    elif index == 4 :
        text += "義式料理！"

    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = text))

def send_ask_record_flex(reply_token) :
    try :
        contents = {    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "為您做紀錄！您吃了 ...", "size": "md", "weight": "bold"}
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "spacer", "size": "xxl"},
                            {   "type": "button", "style": "secondary", "height": "sm",
                                "action": {"type": "message", "text": "中式料理", "label": "中式料理"}},
                            {"type": "text", "text": " ", "size": "xxs", "weight": "bold"},
                            {   "type": "button", "style": "secondary", "height": "sm",
                                "action": {"type": "message", "text": "日式料理", "label": "日式料理"}},
                            {"type": "text", "text": " ", "size": "xxs", "weight": "bold"},
                            {   "type": "button", "style": "secondary", "height": "sm",
                                "action": {"type": "message", "text": "美式料理", "label": "美式料理"}},
                            {"type": "text", "text": " ", "size": "xxs", "weight": "bold"},
                            {   "type": "button", "style": "secondary", "height": "sm",
                                "action": {"type": "message", "text": "義式料理", "label": "義式料理"}},
                            {"type": "text", "text": " ", "size": "xl", "weight": "bold"},
                            {"type": "text", "text": "沒有您的選項嗎？也可以直接輸入喔～", "size": "sm", "weight": "bold", "color": "#aaaaaa"},
                        ]
                    }
                }
        line_bot_api = LineBotApi(channel_access_token)        
        line_bot_api.reply_message(
            reply_token,
            FlexSendMessage(
                alt_text = "您吃了什麼呢～",
                contents = contents
            )
        )
        return True
    except :
        return False

def send_and_watch_record(event) :
    data = search_table()

    text = "您曾經吃過...\n\n\t"
    text += "中式料理 " + str(data[0][1]) + " 次\n\t"
    text += "日式料理 " + str(data[0][2]) + " 次\n\t"
    text += "美式料理 " + str(data[0][3]) + " 次\n\t"
    text += "義式料理 " + str(data[0][4]) + " 次\n\t"
    text += "其他料理 " + str(data[0][5]) + " 次"

    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = text))

def send_and_record(event) :
    data = search_table()

    index = 5
    if event.message.text == "中式料理" :
        index = 1
    elif event.message.text == "日式料理" :
        index = 2
    elif event.message.text == "美式料理" :
        index = 3
    elif event.message.text == "義式料理" :
        index = 4

    update_table(index, str(data[0][index] + 1))
    
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "成功紀錄囉！"))


def get_img_url(img_source, target):
    img_source_dict = {
        'google': [f"https://www.google.com/search?{urllib.parse.urlencode(dict([['tbm', 'isch'], ['q', target]]))}/",
                   'img data-src="\S*"',
                   14,
                   -1],
        'pixabay': [f"https://pixabay.com/images/search/{urllib.parse.urlencode(dict([['q', target]]))[2:]}/",
                    'img srcset="\S*\s\w*,',
                    12,
                    -4],
        'unsplash': [f"https://unsplash.com/s/photos/{urllib.parse.urlencode(dict([['q', target]]))[2:]}/",
                     'srcSet="\S* ',
                     8,
                     -1]}
    
    url = img_source_dict[img_source][0]
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
            
    req = urllib.request.Request(url, headers = headers)
    conn = urllib.request.urlopen(req)

    print('fetch page finish')

    img_list = []

    for match in re.finditer(img_source_dict[img_source][1], str(conn.read())):
        img_list.append(match.group()[img_source_dict[img_source][2]:img_source_dict[img_source][3]])

    if (len(img_list) == 0) :
        target = "cuisine"
        random_img_url =  get_img_url('google', target)
    else :
        random_img_url = random.choice(img_list)
        #random_img_url = img_list[0]
    
    print('fetch img url finish')
    print(random_img_url)
    
    return random_img_url

def prepare_img_search_flex(text_title, target, random_img_url):
    contents = {    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": text_title, "size": "sm", "color": "#aaaaaa", "align": "end", "gravity": "bottom"},
                            {"type": "text", "text": target, "size": "md", "weight": "bold"}
                        ]
                    },
                    "hero": {
                        "type": "image",
                        "url": random_img_url,
                        "size": "full",
                        "aspect_ratio": "3:2",
                        "aspect_mode": "cover"
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "spacer", "size": "xxl"},
                            {"type": "button", "style": "primary", "color": "#905c44",
                                    "action": { "type": "uri", "label": "看看原圖", "uri": random_img_url}
                            },
                            {"type": "text", "text": " ", "size": "xxs", "weight": "bold"},
                            {"type": "button", "style": "primary", "color": "#905c44",
                                    "action": { "type": "uri", "label": "前往地圖", "uri": "https://www.google.com.tw/maps"}
                            }
                        ]
                    }
                }
    return contents


def create_table() :
    drop_table()
    #DATABASE_URL = os.environ['DATABASE_URL']
    DATABASE_URL = os.popen("heroku config:get DATABASE_URL -a toc-project-what-to-eat").read()[:-1]
    
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    create_table_query = '''CREATE TABLE eat_record(
           record_no serial PRIMARY KEY,
           chinese Integer,
           japanese Integer,
           american Integer,
           italian Integer,
           others Integer
        );'''
    cursor.execute(create_table_query)
    conn.commit()

    cursor.close()
    conn.close()
    insert_table()

def drop_table() :
    #DATABASE_URL = os.environ['DATABASE_URL']
    DATABASE_URL = os.popen("heroku config:get DATABASE_URL -a toc-project-what-to-eat").read()[:-1]
    
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    delete_table_query = '''DROP TABLE IF EXISTS eat_record'''
    cursor.execute(delete_table_query)
    conn.commit()

    cursor.close()
    conn.close()

def insert_table():
    #DATABASE_URL = os.environ['DATABASE_URL']
    DATABASE_URL = os.popen("heroku config:get DATABASE_URL -a toc-project-what-to-eat").read()[:-1]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    record = ('0', '0', '0', '0', '0')
    table_columns = '(chinese, japanese, american, italian, others)'
    postgres_insert_query = f"""INSERT INTO eat_record {table_columns} VALUES (%s, %s, %s, %s, %s);"""

    cursor.execute(postgres_insert_query, record)
    conn.commit()

    count = cursor.rowcount

    message = f"恭喜您！ {cursor.rowcount} 筆資料成功匯入表單！"
    print(message)

    cursor.close()
    conn.close()

def update_table(index, count):
    #DATABASE_URL = os.environ['DATABASE_URL']
    DATABASE_URL = os.popen("heroku config:get DATABASE_URL -a toc-project-what-to-eat").read()[:-1]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    if index == 1 :
        update_table_query = f"""UPDATE eat_record SET chinese = %s"""
    elif index == 2 :
        update_table_query = f"""UPDATE eat_record SET japanese = %s"""
    elif index == 3 :
        update_table_query = f"""UPDATE eat_record SET american = %s"""
    elif index == 4 :
        update_table_query = f"""UPDATE eat_record SET italian = %s"""
    else :
        update_table_query = f"""UPDATE eat_record SET others = %s"""
    
    cursor.execute(update_table_query, (count,))
    conn.commit()

    cursor.close()
    conn.close()

    message = f"恭喜您！{cursor.rowcount} 筆資料成功匯入！"
    print(message)

def search_table():
    #DATABASE_URL = os.environ['DATABASE_URL']
    DATABASE_URL = os.popen("heroku config:get DATABASE_URL -a toc-project-what-to-eat").read()[:-1]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    postgres_select_query = f"""SELECT * FROM eat_record"""
    cursor.execute(postgres_select_query)
    
    data = []
    while True:
        temp = cursor.fetchone()
        if temp:
            data.append(temp)
        else:
            break
    print("表單資料：", data)

    cursor.close()
    conn.close()

    return data
