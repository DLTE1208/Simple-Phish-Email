# -*- coding: gbk -*-
from data_manager import DataManager
from phish_email import PhishEmail
from phish_website import PhishWebsite
from threading import Thread
from time import sleep


def check_return_list_and_print(return_list):
    '''
    检查返回列表并打印结果，判断邮件是否发送成功。

    参数:
    return_list (list): 包含发送结果的列表。
    '''
    if return_list is not None and len(return_list) >= 2:
        print("发送成功!")
        print(f'发送方邮箱：\n[0]{return_list[0]}')
        print('受害者邮箱：')
        for index in range(1, len(return_list)):
            print(f'[{index}] {return_list[index]}', end='\t')
            if index % 2 == 0:
                print()
        print()
    elif return_list is not None and len(return_list) == 1:
        print("未发送!")
        print(f'发送者邮箱：\n{return_list[0]}')
    else:
        print("发送失败!")


def show_dic(dic):
    '''
    展示字典，用于选择数据文件。

    参数：
    dic (dict): 被展示的字典
    '''
    for i, (key, value) in enumerate(dic.items()):
        if i % 2 == 0 and i != 0: print()
        print(f'[{key}] {value}', end='\t')
    print()


def show_data(data):
    '''
    展示数据，用于浏览数据内容。

    参数：
    data (dict or list): 被展示的数据
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
        print('设置发送方数据：')
        dic = DataManager.get_all_senders_dic()
        show_dic(dic)
        choose = int(input("选择："))
        if choose in dic.keys():
            sender_data = DataManager.get_sender(dic[choose])
        else:
            print('无效输入，重新选择')
        print()

    while victims_data is None:
        print('设置受害者数据：')
        dic = DataManager.get_all_victims_dic()
        show_dic(dic)
        choose = int(input("选择："))
        if choose in dic.keys():
            victims_data = DataManager.get_victims(dic[choose])
        else:
            print('无效输入，重新选择')
        print()

    while content_data is None:
        print('设置内容数据：')
        dic = DataManager.get_all_contents_dic()
        show_dic(dic)
        choose = int(input("选择："))
        if choose in dic.keys():
            content_data = DataManager.get_content(dic[choose])
            if content_data['Content Type'] == 'URL' or content_data['Content Type'] == 'HTML':
                print("启动钓鱼网站中……")
                website_thread = Thread(target=PhishWebsite.run)
                website_thread.start()
                is_phish_website_running = True
                sleep(0.5)
        else:
            print('无效输入，重新选择')
        print()

    phish_email = PhishEmail(sender_data, victims_data, content_data)
    if is_phish_website_running: PhishWebsite.set_phish_email(phish_email)

    while True:
        print('菜单：\n[1] 浏览发送方数据\n[2] 浏览受害者数据\n[3] 浏览内容数据\n[4] 发送钓鱼邮件\n[0] 放弃发送邮件')
        choose = int(input("选择："))
        if choose == 1:
            show_data(sender_data)
        elif choose == 2:
            show_data(victims_data)
        elif choose == 3:
            show_data(content_data)
        elif choose == 4:
            print("发送中……")
            return_list = phish_email.send()    #在这里可以控制发射钓鱼邮件的数量，默认为向所有受害者发送
            check_return_list_and_print(return_list)
            break
        elif choose == 0:
            print("放弃发送邮件")
            break
        else:
            print('无效输入，重新选择')

    print()
    if is_phish_website_running:
        choose = input('钓鱼网站运行中……')
        print()
    choose = input('按任意键退出程序')
