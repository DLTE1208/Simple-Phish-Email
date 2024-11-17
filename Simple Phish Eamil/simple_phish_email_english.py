# -*- coding: gbk -*-
from data_manager import DataManager
from phish_email import PhishEmail
from phish_website import PhishWebsite
from threading import Thread
from time import sleep
from simple_phish_email import show_dic, show_data, check_return_list_and_print

if __name__ == '__main__':
    sender_data = None
    victims_data = None
    content_data = None
    phish_email = None
    is_phish_website_running = False
    website_thread = None

    while sender_data is None:
        print('Set sender data:')
        dic = DataManager.get_all_senders_dic()
        show_dic(dic)
        choose = int(input("Select:"))
        if choose in dic.keys():
            sender_data = DataManager.get_sender(dic[choose])
        else:
            print('Invalid input, select again')
        print()

    while victims_data is None:
        print('Set victims data:')
        dic = DataManager.get_all_victims_dic()
        show_dic(dic)
        choose = int(input("Select:"))
        if choose in dic.keys():
            victims_data = DataManager.get_victims(dic[choose])
        else:
            print('Invalid input, select again')
        print()

    while content_data is None:
        print('Set content data:')
        dic = DataManager.get_all_contents_dic()
        show_dic(dic)
        choose = int(input("Select:"))
        if choose in dic.keys():
            content_data = DataManager.get_content(dic[choose])
            if content_data['Content Type'] == 'URL' or content_data['Content Type'] == 'HTML':
                print("Launch Phish Website in...")
                website_thread = Thread(target=PhishWebsite.run)
                website_thread.start()
                is_phish_website_running = True
                sleep(0.5)
        else:
            print('Invalid input, select again')
        print()

    phish_email = PhishEmail(sender_data, victims_data, content_data)
    if is_phish_website_running: PhishWebsite.set_phish_email(phish_email, True)

    while True:
        print('Menu:\n[1]Browse sender data\n[2]Browse victim data\n[3]Browse content data\n[4]Send Phish Email\n[0]Drop email')
        choose = int(input("Select:"))
        if choose == 1:
            show_data(sender_data)
        elif choose == 2:
            show_data(victims_data)
        elif choose == 3:
            show_data(content_data)
        elif choose == 4:
            print("Sending...")
            return_list = phish_email.send()    #Here can control the number of phish emails sent, the default is sent to all victims
            check_return_list_and_print(return_list)
            break
        elif choose == 0:
            print("Drop email")
            break
        else:
            print('Invalid input, select again')

    print()
    if is_phish_website_running:
        choose = input("Phish Website running...")
        print()
    choose = input('Press any key to exit the program')
