#!/usr/bin/env python3
#!coding=utf-8

import logging
from tabulate import tabulate

from settings import log_file_path
from models.transaction import Transaction
from models.transaction_date_time import TransactionDateTime
from tools.transaction_datetime_tools import TransactionDateTimeTools


logging.basicConfig(filename=log_file_path,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TransactionTools:
    
    @classmethod
    def create_transaction(cls, infos: list) -> Transaction:
    
        transaction = Transaction()
        transaction.init_by_list(infos)
        return transaction


    @classmethod
    def init_by_list(cls, transaction: Transaction, infos: list) -> Transaction:
        
        # print(f"Infos length: {str(len(infos))}")
        time_ = ''
        type_ = ''
        counterparty = ''
        counterparty_number = ''
        product = ''
        income_expense = ''
        amount = ''
        payment_method = ''
        current_status = ''
        transaction_number = ''
        merchant_number = ''
        remark = ''
        
        #alipay
        if len(infos) == 13:
            time_ = infos[0]
            type_ = infos[1]
            counterparty = infos[2]
            counterparty_number = infos[3]
            product = infos[4]
            income_expense = infos[5]
            amount = infos[6]
            payment_method = infos[7]
            current_status = infos[8]
            transaction_number = infos[9]
            merchant_number = infos[10]
            
            if len(infos) >= 12:
                remark = infos[11]
            else:
                remark = ''
        # wechat
        if len(infos) == 11:
            time_ = infos[0]
            type_ = infos[1]
            counterparty = infos[2]
            counterparty_number = ''
            product = infos[3]
            income_expense = infos[4]
            amount = float(str(infos[5]).replace("¥", ""))
            payment_method = infos[6]
            current_status = infos[7]
            transaction_number = infos[8]
            merchant_number = infos[9]
            
            if len(infos) >= 11:
                remark = infos[10]
            else:
                remark = ''
                
        temp_time = TransactionDateTime()
        TransactionDateTimeTools.inject_datetime_str(transaction_datetime=temp_time, datetime_str=time_)
        transaction.time_ = temp_time
        transaction.type_ = str(type_)
        transaction.counterparty = str(counterparty)
        transaction.counterparty_number = str(counterparty_number)
        transaction.product = str(product)
        transaction.income_expense = str(income_expense)
        transaction.amount = str(amount)
        transaction.payment_method = str(payment_method)
        transaction.current_status = str(current_status)
        transaction.transaction_number = str(transaction_number)
        transaction.merchant_number = str(merchant_number)
        transaction.remark = str(remark)
        transaction.source = 'alipay'
        
        return transaction
    
    
    @classmethod
    def get_transaction_number(cls, transaction: Transaction) -> str:
        
        return str(transaction.transaction_number)
    
    
    @classmethod
    def show_transaction(cls, transaction: Transaction):

        headers = ["Field", "Value"]
        data = [
            ["Time", TransactionDateTimeTools.get_v_ser(transaction.time_)],
            ["Type", transaction.type_],
            ["Counterparty", transaction.counterparty],
            ["CounterpartyNumber", transaction.counterparty_number],
            ["Product", transaction.product],
            ["Income/Expense", transaction.income_expense],
            ["Amount", transaction.amount],
            ["Payment Method", transaction.payment_method],
            ["Current Status", transaction.current_status],
            ["Transaction Number", transaction.transaction_number],
            ["Merchant Number", transaction.merchant_number],
            ["Remark", transaction.remark],
            ["Source", transaction.source]
        ]
        
        print(tabulate(data, headers, tablefmt="simple"))