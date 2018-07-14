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
import scrape_ld_blog as scrape_ld_blog

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

@app.route('/check')
def checkId():
    #
    return render_template('hello.html')


@app.route('/push_ss/<url>/<id>', methods=['GET'])
def push_ss(url,id):
    url=str(url).replace('-','/')
    to = os.environ.get(id) 
    line_bot_api.push_message(to, TextSendMessage(text='---今日の更新---'))
    all_list = scrape_ld_blog.scrape(url)
    push_list = []    
    for i, message_list in enumerate(all_list):
        push_list.append(message_list)
        if i==0:
            continue
        if i%4==0:
            line_bot_api.push_message(to, TextSendMessage(text='\r\n'.join(push_list)))
            push_list=[]
    line_bot_api.push_message(to, TextSendMessage(text='\r\n'.join(push_list)))
    line_bot_api.push_message(to, TextSendMessage(text='---ここまで---'))
    return 'OK'

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print (event.source)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
