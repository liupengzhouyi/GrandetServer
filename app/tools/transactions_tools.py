#!/usr/bin/env python3
#!coding=utf-8

import logging
import csv
from datetime import datetime
from functools import cmp_to_key

from settings import log_file_path
from settings import bill_No1_line
from models.transaction_date_time import TransactionDateTime
from models.transaction import Transaction

from tools.inject_style import InjectStyle
from tools.transaction_tools import TransactionTools
from tools.read_transaction_table_tools import ReadTransactionTable
from tools.transaction_datetime_tools import TransactionDateTimeTools


logging.basicConfig(filename=log_file_path,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TransactionsTools:
    
    @classmethod
    def sort_transactions(cls, transactions: list) -> list:
        
        transactions.sort(key=cmp_to_key(cls.cmp_transaction_by_datetime))
        return transactions
    
    
    @classmethod
    def delete_same_transaction(cls, transactions: list) -> list:
        """
        从交易列表中删除具有相同交易号的交易对象，并返回新的交易列表。

        Args:
            transactions (list): 包含交易对象的列表。

        Returns:
            list: 不包含相同交易号交易的新列表。
        """
        new_transactions = []  # 存储不包含相同交易号的新交易列表
        transaction_ids = []  # 存储已经处理过的交易号

        for item in transactions:
            
            if isinstance(item, Transaction) or True:
                # print(item.transaction_number)
                # 获取交易的交易号并去除空格和制表符
                # transaction_id = str(item.transaction_number).replace(" ", "").replace("\t", "")get_transaction_number
                transaction_id = TransactionTools.get_transaction_number(transaction=item).replace(" ", "").replace("\t", "")
                # print(f"transaction_id: {transaction_id}")
                if transaction_id not in transaction_ids:
                    # 如果交易号不在已处理列表中，将该交易添加到新列表中
                    transaction_ids.append(transaction_id)
                    new_transactions.append(item)
                else:
                    # 如果交易号已经存在于已处理列表中，记录日志并不添加该交易
                    datetime_info = TransactionDateTimeTools.get_v_ser(transaction_datetime=item.time_)
                    logger.info(f"{datetime_info}: {transaction_id}, has same transaction number.")
        return new_transactions
        
    @classmethod
    def read_csv_head(cls, csv_file_path: str, frist_line_word="") -> list:
        
        heads = []
        with open(csv_file_path, 'r') as f:
            reader = csv.reader(f)
            begin = False
            target = frist_line_word
            for row in reader:
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
    def check_dt1_dt2(cls, dt1: TransactionDateTime, dt2: TransactionDateTime) -> bool:
        """
        比较两个 TransactionDateTime 对象的时间先后顺序。

        Args:
            dt1 (TransactionDateTime): 第一个 TransactionDateTime 对象。
            dt2 (TransactionDateTime): 第二个 TransactionDateTime 对象。

        Returns:
            bool: 如果 dt1 晚于 dt2,则返回 False;如果 dt1 早于或等于 dt2,则返回 True。
        """
        
        dt1_bigger_than_dt2 = False
        # 创建 datetime 对象以便比较
        dt_1 = datetime(dt1.year, dt1.month, dt1.day, dt1.hour, dt1.minute, dt1.second)
        dt_2 = datetime(dt2.year, dt2.month, dt2.day, dt2.hour, dt2.minute, dt2.second)

        if dt_1 > dt_2:
            # dt1 晚于 dt2
            dt1_bigger_than_dt2 = False
        elif dt_1 < dt_2:
            # dt1 早于 dt2
            dt1_bigger_than_dt2 = True
        else:
            # dt1 等于 dt2
            dt1_bigger_than_dt2 = True

        return dt1_bigger_than_dt2


    @classmethod
    def cmp_transaction_by_datetime(cls, x: Transaction, y: Transaction) -> int:
        """
        比较两个交易对象的时间先后顺序。

        Args:
            x (Transaction): 第一个交易对象。
            y (Transaction): 第二个交易对象。

        Returns:
            int: 如果 x 的时间晚于 y，则返回 1；如果 x 的时间早于 y，则返回 -1。
        """
        if cls.check_dt1_dt2(x.time_, y.time_):
            # x 的时间晚于 y
            return 1
        else:
            # x 的时间早于 y
            return -1
    
    # @staticmethod
    @classmethod
    def init_transactions_by_file(cls, file_path: str) -> list:
        
        log_info = f"Gentateion transcations by file {file_path}."
        logger.info(log_info)
        transaction_infos = ReadTransactionTable.open_csv(csv_file_path=file_path, head=False, frist_line_word=bill_No1_line)
        log_info = f"transcations num: {str(len(transaction_infos))}."
        logger.info(log_info)
        transactions = []
        source = ReadTransactionTable.alipay_or_wechat(csv_file_path=file_path)
        for row in transaction_infos:
            temp = Transaction(time_=TransactionDateTime())
            temp = TransactionTools().init_by_list(transaction=temp, infos=row)
            temp_transaction_with_source = InjectStyle.add_source(transaction=temp, source=source)
            transactions.append(temp_transaction_with_source)
        return transactions
    
    
    @classmethod
    def init_transactions_by_files(cls, file_paths: list) -> list:
        
        log_info = f"Gentateion transcations by target files."
        logger.info(log_info)
        all_transactions = []
        for bill_file in file_paths:
            # 打开 CSV 文件并获取交易数据
            transactions = cls.init_transactions_by_file(file_path=bill_file)
            # 将获取的交易数据扩展到所有交易数据列表中
            all_transactions.extend(transactions)
            all_transactions = all_transactions + transactions
            logger.info(str(len(transactions)) + "--------" + str(len(all_transactions)))
        # 根据交易时间对所有交易数据进行排序
        all_transactions = cls.sort_transactions(transactions=all_transactions)
        logger.info("--------" + str(len(all_transactions)))
        # 删除具有相同交易号的交易，并获取新的交易列表
        target_transactions = cls.delete_same_transaction(all_transactions)
        logger.info("--------" + str(len(target_transactions)))
        log_info = f"All transcations num: {str(len(target_transactions))}."
        logger.info(log_info)
        return target_transactions