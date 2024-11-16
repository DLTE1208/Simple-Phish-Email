# -*- coding: gbk -*-
from data_manager import DataManager
from phish_email import PhishEmail
from phish_website import PhishWebsite
from threading import Thread
from time import sleep


def check_return_list_and_print(return_list):
    '''
    ��鷵���б���ӡ������ж��ʼ��Ƿ��ͳɹ���

    ����:
    return_list (list): �������ͽ�����б�
    '''
    if return_list is not None and len(return_list) >= 2:
        print("���ͳɹ�!")
        print(f'���ͷ����䣺\n[0]{return_list[0]}')
        print('�ܺ������䣺')
        for index in range(1, len(return_list)):
            print(f'[{index}] {return_list[index]}', end='\t')
            if index % 2 == 0:
                print()
        print()
    elif return_list is not None and len(return_list) == 1:
        print("δ����!")
        print(f'���������䣺\n{return_list[0]}')
    else:
        print("����ʧ��!")


def show_dic(dic):
    '''
    չʾ�ֵ䣬����ѡ�������ļ���

    ������
    dic (dict): ��չʾ���ֵ�
    '''
    for i, (key, value) in enumerate(dic.items()):
        if i % 2 == 0 and i != 0: print()
        print(f'[{key}] {value}', end='\t')
    print()


def show_data(data):
    '''
    չʾ���ݣ���������������ݡ�

    ������
    data (dict or list): ��չʾ������
    '''
    if isinstance(data, dict):
        for key, value in data.items():
            print(f'[{key}] {value}')
    elif isinstance(data, list):
        for i, value in enumerate(data, start=1):
            print(f'[{i}] {value}')
    print()


if __name__ == '__main__':
    sender_data = None
    victims_data = None
    content_data = None
    phish_email = None
    is_phish_website_running = False
    website_thread = None

    while sender_data is None:
        print('���÷��ͷ����ݣ�')
        dic = DataManager.get_all_senders_dic()
        show_dic(dic)
        choose = int(input("ѡ��"))
        if choose in dic.keys():
            sender_data = DataManager.get_sender(dic[choose])
        else:
            print('��Ч���룬����ѡ��')
        print()

    while victims_data is None:
        print('�����ܺ������ݣ�')
        dic = DataManager.get_all_victims_dic()
        show_dic(dic)
        choose = int(input("ѡ��"))
        if choose in dic.keys():
            victims_data = DataManager.get_victims(dic[choose])
        else:
            print('��Ч���룬����ѡ��')
        print()

    while content_data is None:
        print('�����������ݣ�')
        dic = DataManager.get_all_contents_dic()
        show_dic(dic)
        choose = int(input("ѡ��"))
        if choose in dic.keys():
            content_data = DataManager.get_content(dic[choose])
            if content_data['Content Type'] == 'URL' or content_data['Content Type'] == 'HTML':
                print("����������վ�С���")
                website_thread = Thread(target=PhishWebsite.run)
                website_thread.start()
                is_phish_website_running = True
                sleep(0.5)
        else:
            print('��Ч���룬����ѡ��')
        print()

    phish_email = PhishEmail(sender_data, victims_data, content_data)
    if is_phish_website_running: PhishWebsite.set_phish_email(phish_email)

    while True:
        print('�˵���\n[1] ������ͷ�����\n[2] ����ܺ�������\n[3] �����������\n[4] ���͵����ʼ�\n[0] ���������ʼ�')
        choose = int(input("ѡ��"))
        if choose == 1:
            show_data(sender_data)
        elif choose == 2:
            show_data(victims_data)
        elif choose == 3:
            show_data(content_data)
        elif choose == 4:
            print("�����С���")
            return_list = phish_email.send(1)
            check_return_list_and_print(return_list)
            break
        elif choose == 0:
            print("���������ʼ�")
            break
        else:
            print('��Ч���룬����ѡ��')

    print()
    if is_phish_website_running:
        choose = input('������վ�����С���')
        print()
    choose = input('��������˳�����')
