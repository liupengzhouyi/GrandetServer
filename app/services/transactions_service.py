#/bin/bash python3
#coding: utf-8

import logging

from models.transaction_date_time import TransactionDateTime
from models.transaction import Transaction
from models.years_transaction import YearsTransaction

from tools.transaction_tools import TransactionTools
from tools.transactions_tools import TransactionsTools

from settings import log_file_path


logging.basicConfig(filename=log_file_path,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AnalysisTransactions:
    
    def __init__(self, transactions: list):
        self.transactions = transactions
    
    
    def get_transactions(self) -> list:
        return self.transactions
    
    
    def get_size(self) -> int:
        """get size

        Returns:
            int: _description_
        """
        
        return len(self.transactions)
    
    
    def get_years(self) -> list:
        """_summary_

        Returns:
            list: _description_
        """
        
        years = []
        for transaction in self.transactions:
            year = transaction.get_datetime().year
            if year not in years:
                years.append(year)
        return years
    
    
    def get_months(self, target_year: int) -> list:
        '''
        获取某一年的所有月份
        '''
        
        months = []
        for transaction in self.transactions:
            year = transaction.get_datetime().year
            if year == target_year:
                month = transaction.get_datetime().month
                if month not in months:
                    months.append(month)
        return months


    def get_days(self, target_year: int, target_month: int) -> list:
        days = []
        for transaction in self.transactions:
            year = transaction.get_datetime().year
            if year == target_year:
                month = transaction.get_datetime().month
                if month == target_month:
                    day = transaction.get_datetime().day
                    if day not in days:
                        days.append(day)
        return days
    
    def get_every_years_transactions(self) -> dict:
        
        logger.info("Begin set every years transactions.")
        years = []
        result = {}
        for transaction in self.transactions:
            year = str(transaction.get_datetime().year)
            if year not in years:
                years.append(year)
                result[year] = YearsTransaction(year=int(year))
                result[year].add_transaction(transaction)
            else:
                result[year].add_transaction(transaction)
        
        logger.info(f"years number: {len(result.keys())}")
        
        for year in result.keys():
            logger.info(f"{year} year has {str(TransactionsTools.get_transactions_size(target_transaction=result.get(year)))} transactions.")
        
        logger.info("Set every years transactions over.")
        return result
    
    
    @classmethod
    def analyze_transactions_income(cls, transactions: list) -> tuple:
        
        key_word = "收入"
        count = 0
        money = 0.0
        temp_transactions = []
        for transaction in transactions:
            if isinstance(transaction, Transaction):
                if transaction.income_expense == key_word:
                    count += 1
                    money += float(transaction.amount)
                    temp_transactions.append(transaction)
        logger.info(f"账单收入详情：交易笔数:{str(count)} 金额:{str(money)}.")
        return (count, money, temp_transactions)
    
    
    @classmethod
    def analyze_transactions_expenditure(cls, transactions: list) -> tuple:
        
        key_word = "支出"
        count = 0
        money = 0.0
        temp_transactions = []
        for transaction in transactions:
            if isinstance(transaction, Transaction):
                if transaction.income_expense == key_word:
                    count += 1
                    money += float(transaction.amount)
                    temp_transactions.append(transaction)
        logger.info(f"账单收入详情：交易笔数:{str(count)} 金额:{str(money)}.")
        return (count, money, temp_transactions)

    
    @classmethod
    def analyze_transactions_no_income_and_expenditure(cls, transactions: list) -> tuple:
        
        key_word = "不计收支"
        count = 0
        money = 0.0
        temp_transactions = []
        for transaction in transactions:
            if isinstance(transaction, Transaction):
                logger.info(f"{transaction.income_expense}")
                if transaction.income_expense == key_word:
                    count += 1
                    money += float(transaction.amount)
                    temp_transactions.append(transaction)
        logger.info(f"账单收入详情：交易笔数:{str(count)} 金额:{str(money)}.")
        return (count, money, temp_transactions)
        