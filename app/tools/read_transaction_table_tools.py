# /bin/bash python3

import pandas as pd
import csv
import os
import logging

from models.transaction import Transaction
from tools.transaction_tools import TransactionTools
from tools.inject_style import InjectStyle
from settings import log_file_path


logging.basicConfig(filename=log_file_path,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ReadTransactionTable:

    
    def __init__(self) -> None:
        pass
    
    @classmethod
    def extract_all_file_path(cls, folder_path: str) -> list:
        
        all_file_paths = []
        try:
            for filename in os.listdir(folder_path):
                
                temp_path = os.path.join(folder_path, filename)
                if os.path.isfile(temp_path):
                    all_file_paths.append(temp_path)
                else:
                    temp_files = cls.extract_all_file_path(temp_path)
                    for item in temp_files:
                        all_file_paths.append(os.path.join(folder_path, item))
        except Exception:
            logging.error("Can't open fodler:" + folder_path)
            return all_file_paths
        return all_file_paths
    
    
    @classmethod
    def extract_csv_file_path(cls, folder_path: str) -> list:
        
        csv_file_paths = []
        try:
            for filename in os.listdir(folder_path):
                
                temp_path = os.path.join(folder_path, filename)
                if os.path.isfile(temp_path):
                    csv_file_paths.append(temp_path)
                else:
                    temp_files = cls.extract_csv_file_path(temp_path)
                    for item in temp_files:
                        csv_file_paths.append(os.path.join(folder_path, item))
        except Exception:
            logging.error("Can't open fodler:" + folder_path)
            return csv_file_paths
        return csv_file_paths


    @classmethod
    def flitter_csv_file(cls, csv_files: list) -> list:
        
        target_csv_files = []
        for item in csv_files:
            file_name = os.path.basename(item)
            if file_name.endswith(".csv") and not file_name.startswith("alipay_record"):
                target_csv_files.append(item)
        return target_csv_files


    @classmethod
    def read_table(cls, input_file: str, output_file: str):
        """
        Reads a table from the input file and writes it to the output file.

        Parameters:
            input_file (str): The path to the input file.
            output_file (str): The path to the output file.

        Returns:
            None
        """
        df = pd.read_csv(input_file)
        df.to_csv(output_file, index=False)


    @classmethod
    def read_csv_head(cls, csv_file_path: str, frist_line_word="") -> list:
        
        heads = []
        with open(csv_file_path, 'r') as f:
            reader = csv.reader(f)
            begin = False
            target = frist_line_word
            for row in reader:
                # print(row)
                if not begin:
                    if len(row) == 0 or target != row[0]:
                        continue
                    else:
                        begin = True
                if begin:
                    heads = row
                    break
        return heads


    @classmethod
    def alipay_or_wechat(cls, csv_file_path: str) -> str:
        
        alipay_word = '-------支付宝（中国）网络技术有限公司  电子客户回单'
        wechat_word = "-------微信支付账单明细列表------"
        source="alipay"
        for line in open(csv_file_path):
            if wechat_word in line:
                # print(line)
                source = "wechat"
                break
            if alipay_word in line:
                # print(line)
                source = "alipay"
                break
        return source


    @classmethod
    def open_csv(cls, csv_file_path: str, head=False, frist_line_word="") -> list:
        
        infos = []
        with open(csv_file_path, 'r') as f:
            reader = csv.reader(f)
            head_ = head
            begin = False
            target = frist_line_word
            for row in reader:
                if not begin:
                    if len(row) == 0 or target != row[0]:
                        continue
                    else:
                        begin = True    
                if not head_:
                    head_ = True
                    continue
                infos.append(row)
                
            logging.info(f"Read over. Size: {str(len(infos))} line.")
        return infos
        
