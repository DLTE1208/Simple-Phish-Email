# -*- coding: gbk -*-
from dataclasses import dataclass
import os
import json

#负责管理数据的保存和读取
class DataManager:
    __SENDER_REQUIRED_KEY = ['Host', 'Port', 'Email', 'Password']           #发送者数据必须包含的键
    __SENDER_DIR = os.path.join('.', 'Sender')                              #发送者数据文件保存的目录

    __VICTIMS_DIR = os.path.join('.', 'Victims')                            #受害者数据文件保存的目录

    __CONTENT_REQUIRED_KEY = ['Content Type', 'Disguised Name', 'Subject']  #内容数据必须包含的键
    __CONTENT_DIR = os.path.join('.', 'Content')                            #内容数据文件保存的目录

    @classmethod
    def save_sender(cls, data):
        '''
        保存发送方数据到文件。文件名是发送方的邮箱地址。

        参数：
        data (dict): 发送方数据
        '''
        if isinstance(data, dict) and all(key in cls.__SENDER_REQUIRED_KEY for key in data):
            filename = data['email']
            is_success = cls.__save_to_file(cls.__SENDER_DIR, filename, data)
            if is_success:
                return;
        print("Save sender failed.")

    @classmethod
    def save_victims(cls, filename, data):
        '''
        保存受害者数据到文件。

        参数：
        filename (str): 文件名
        data (list): 受害者数据
        '''
        if isinstance(data, list) and len(data) > 0:
            is_success = cls.__save_to_file(cls.__VICTIMS_DIR, filename, data)
            if is_success:
                return;
        print("Save victims failed.")

    @classmethod
    def save_content(cls, filename, data):
        '''
        保存内容数据到文件。

        参数：
        filename (str): 文件名
        data (dict): 内容数据
        '''
        if isinstance(data, dict) and all(key in data for key in cls.__CONTENT_REQUIRED_KEY):
            is_success = cls.__save_to_file(cls.__CONTENT_DIR, filename, data)
            if is_success:
                return;
        print("Save content failed.")


    @classmethod
    def get_sender(cls, filename):
        '''
        获取发送方数据。

        参数：
        filename (str): 文件名

        返回：
        dict: 发送方数据，如果获取失败则返回None
        '''
        data = cls.__load_from_file(cls.__SENDER_DIR, filename)
        if data is not None and isinstance(data, dict) and all(key in cls.__SENDER_REQUIRED_KEY for key in data):
            return data
        else:
            print("Get sender failed.")
            return None

    @classmethod
    def get_victims(cls, filename):
        '''
        获取受害者数据。

        参数：
        filename (str): 文件名

        返回：
        list: 受害者数据，如果获取失败则返回None
        '''
        data = cls.__load_from_file(cls.__VICTIMS_DIR, filename)
        if data is not None and isinstance(data, list) and len(data) > 0:
            return data
        else:
            print("Get victims failed.")
            return None

    @classmethod
    def get_content(cls, filename):
        '''
        获取内容数据。

        参数：
        filename (str): 文件名

        返回：
        dict: 内容数据，如果获取失败则返回None
        '''
        data = cls.__load_from_file(cls.__CONTENT_DIR, filename)
        if data is not None and isinstance(data, dict) and all(key in data for key in cls.__CONTENT_REQUIRED_KEY):
            return data
        else:
            print("Get content failed.")
            return None


    @classmethod
    def get_all_senders_dic(cls):
        '''
        获取所有发送方数据文件的名字，并赋予编号。

        返回：
        dict: 包含编号和文件名的字典
        '''
        return_dic = cls.__get_dic_from_dir(cls.__SENDER_DIR)
        if return_dic is None:
            print("Get all senders dic failed.")
        return return_dic

    @classmethod
    def get_all_victims_dic(cls):
        '''
        获取所有受害者数据文件的名字，并赋予编号。

        返回：
        dict：包含编号和文件名的字典
        '''
        return_dic = cls.__get_dic_from_dir(cls.__VICTIMS_DIR)
        if return_dic is None:
            print("Get all victims dic failed.")
        return return_dic

    @classmethod
    def get_all_contents_dic(cls):
        '''
        获取所有内容数据文件的名字，并赋予编号。

        返回：
        dict：包含编号和文件名的字典
        '''
        return_dic = cls.__get_dic_from_dir(cls.__CONTENT_DIR)
        if return_dic is None:
            print("Get all contents dic failed.")
        return return_dic


    @classmethod
    def __save_to_file(cls, dir, filename, data):
        '''
        保存数据到文件，保存为json文件，后缀为.data。

        参数：
        dir (str): 目录
        filename (str): 文件名
        data (dict or list): 数据

        返回：
        bool: 保存成功返回True，否则返回False
        '''
        if not os.path.exists(dir):
            os.makedirs(dir)
        filepath = os.path.join(dir, f"{filename}.data")
        with open(filepath, 'w', encoding='utf-8') as file:
            try:
                json.dump(data, file, ensure_ascii=False, indent=4)
                return True
            except Exception as exception:
                print(f"Save to file failed.\n{exception}")
                return False

    @classmethod
    def __load_from_file(cls, dir, filename):
        '''
        从文件加载数据，以json的形式读取后缀为.data文件。

        参数：
        dir (str): 目录
        filename（str）：文件名

        返回：
        dict or list: 数据，如果加载失败则返回None
        '''
        filepath = os.path.join(dir, f"{filename}.data")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                    return data
                except Exception as exception:
                    print(f"Load from file failed.\n{exception}")
        return None

    @classmethod
    def __get_dic_from_dir(cls, dir):
        '''
        从目录下获取所有后缀为.data的文件名，并赋予编号。

        参数：
        dir (str): 目录

        返回：
        dict: 包含编号和文件名的字典，如果目录不存在则返回None
        '''
        if os.path.exists(dir):
            filenames = os.listdir(dir)
            return_dic = {i+1: os.path.splitext(filename)[0] for i, filename in enumerate(filenames) if filename.endswith('.data')}
            return return_dic
        else: return None