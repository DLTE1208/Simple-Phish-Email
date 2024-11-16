# -*- coding: gbk -*-
from dataclasses import dataclass
import os
import json

#����������ݵı���Ͷ�ȡ
class DataManager:
    __SENDER_REQUIRED_KEY = ['Host', 'Port', 'Email', 'Password']           #���������ݱ�������ļ�
    __SENDER_DIR = os.path.join('.', 'Sender')                              #�����������ļ������Ŀ¼

    __VICTIMS_DIR = os.path.join('.', 'Victims')                            #�ܺ��������ļ������Ŀ¼

    __CONTENT_REQUIRED_KEY = ['Content Type', 'Disguised Name', 'Subject']  #�������ݱ�������ļ�
    __CONTENT_DIR = os.path.join('.', 'Content')                            #���������ļ������Ŀ¼

    @classmethod
    def save_sender(cls, data):
        '''
        ���淢�ͷ����ݵ��ļ����ļ����Ƿ��ͷ��������ַ��

        ������
        data (dict): ���ͷ�����
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
        �����ܺ������ݵ��ļ���

        ������
        filename (str): �ļ���
        data (list): �ܺ�������
        '''
        if isinstance(data, list) and len(data) > 0:
            is_success = cls.__save_to_file(cls.__VICTIMS_DIR, filename, data)
            if is_success:
                return;
        print("Save victims failed.")

    @classmethod
    def save_content(cls, filename, data):
        '''
        �����������ݵ��ļ���

        ������
        filename (str): �ļ���
        data (dict): ��������
        '''
        if isinstance(data, dict) and all(key in data for key in cls.__CONTENT_REQUIRED_KEY):
            is_success = cls.__save_to_file(cls.__CONTENT_DIR, filename, data)
            if is_success:
                return;
        print("Save content failed.")


    @classmethod
    def get_sender(cls, filename):
        '''
        ��ȡ���ͷ����ݡ�

        ������
        filename (str): �ļ���

        ���أ�
        dict: ���ͷ����ݣ������ȡʧ���򷵻�None
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
        ��ȡ�ܺ������ݡ�

        ������
        filename (str): �ļ���

        ���أ�
        list: �ܺ������ݣ������ȡʧ���򷵻�None
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
        ��ȡ�������ݡ�

        ������
        filename (str): �ļ���

        ���أ�
        dict: �������ݣ������ȡʧ���򷵻�None
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
        ��ȡ���з��ͷ������ļ������֣��������š�

        ���أ�
        dict: ������ź��ļ������ֵ�
        '''
        return_dic = cls.__get_dic_from_dir(cls.__SENDER_DIR)
        if return_dic is None:
            print("Get all senders dic failed.")
        return return_dic

    @classmethod
    def get_all_victims_dic(cls):
        '''
        ��ȡ�����ܺ��������ļ������֣��������š�

        ���أ�
        dict��������ź��ļ������ֵ�
        '''
        return_dic = cls.__get_dic_from_dir(cls.__VICTIMS_DIR)
        if return_dic is None:
            print("Get all victims dic failed.")
        return return_dic

    @classmethod
    def get_all_contents_dic(cls):
        '''
        ��ȡ�������������ļ������֣��������š�

        ���أ�
        dict��������ź��ļ������ֵ�
        '''
        return_dic = cls.__get_dic_from_dir(cls.__CONTENT_DIR)
        if return_dic is None:
            print("Get all contents dic failed.")
        return return_dic


    @classmethod
    def __save_to_file(cls, dir, filename, data):
        '''
        �������ݵ��ļ�������Ϊjson�ļ�����׺Ϊ.data��

        ������
        dir (str): Ŀ¼
        filename (str): �ļ���
        data (dict or list): ����

        ���أ�
        bool: ����ɹ�����True�����򷵻�False
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
        ���ļ��������ݣ���json����ʽ��ȡ��׺Ϊ.data�ļ���

        ������
        dir (str): Ŀ¼
        filename��str�����ļ���

        ���أ�
        dict or list: ���ݣ��������ʧ���򷵻�None
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
        ��Ŀ¼�»�ȡ���к�׺Ϊ.data���ļ������������š�

        ������
        dir (str): Ŀ¼

        ���أ�
        dict: ������ź��ļ������ֵ䣬���Ŀ¼�������򷵻�None
        '''
        if os.path.exists(dir):
            filenames = os.listdir(dir)
            return_dic = {i+1: os.path.splitext(filename)[0] for i, filename in enumerate(filenames) if filename.endswith('.data')}
            return return_dic
        else: return None