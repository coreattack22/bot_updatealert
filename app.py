# coding:utf-8
from flask import Flask, request, abort, render_template
import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime, date, timedelta
import os
from os.path import join, dirname
from dotenv import load_dotenv
import scrape_livedoorblog as scrape_livedoorblog
import scrape_wantedly as scrape_wantedly

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET"))

@app.route('/')
def hello():
    return render_template('hello.html')

#対象サイトごとに処理
@app.route('/push_livedoorblog/<url>/<id>', methods=['GET'])
def push_livedoorblog(url,id):
    url=str(url).replace('-','/')
    push_list = scrape_livedoorblog.scrape(url)
    push_update(push_list,id)

@app.route('/push_wantedly/<url>/<id>', methods=['GET'])
def push_wantedly(url,id):
    url=str(url).replace('-','/')
    push_list = scrape_wantedly.scrape(url)
    push_update(push_list,id)


def push_update(push_list,to):
    line_bot_api.push_message(to, TextSendMessage(text='---今日の更新---'))
    for i, message_list in enumerate(push_list):
        push_list.append(message_list)
        if i==0:
            continue
        if i%4==0:
            line_bot_api.push_message(to, TextSendMessage(text='\r\n'.join(message_list)))
            message_list=[]
    line_bot_api.push_message(to, TextSendMessage(text='\r\n'.join(message_list)))
    line_bot_api.push_message(to, TextSendMessage(text='---ここまで---'))
    return 'OK'

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='このトークのIDは'+str(event.source)+'です'))



if __name__ == "__main__":
    app.run()
