# coding:utf-8
from flask import Flask, request, abort, render_template
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime, date, timedelta

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

app = Flask(__name__)

line_bot_api = LineBotApi('')
handler = WebhookHandler('')

@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/push_ss', methods=['GET'])
def push_ss(): 
    push_text =str(scrape_ld_blog.scrape().iloc[:,:])
    to = ''
    line_bot_api.push_message(to, TextSendMessage(text=push_text))
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

