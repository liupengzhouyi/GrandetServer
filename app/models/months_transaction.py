import json
import logging

from models.transaction import Transaction
from models.days_transaction import DaysTransaction
from settings import log_file_path


logging.basicConfig(filename=log_file_path,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MonthsTransaction:
    
    def __init__(self, year: int, month: int) -> None:
        
        self.year = year
        self.month = month
        self.transactions = []
        self.day_transcations = {}
        
        # 支出交易计数
        self.transaction_count = 0
        # 支出交易计数
        self.pay_expenses_count = 0
        # 收入交易计数
        self.take_in_count = 0
        # 不计入收支交易计数
        self.no_include_count = 0
        # 支出交易金额
        self.pay_expenses = 0.0
        # 收入交易金额
        self.take_in = 0.0
        # 不计入收支交易金额
        self.no_include = 0.0
        
    
    def to_json(self, simple: bool=True) -> dict:
        
        day_transcations_json = {}
        for day_transcations_key in self.day_transcations.keys():
            day_transactions = self.day_transcations.get(day_transcations_key)
            if isinstance(day_transactions, DaysTransaction):
                day_transcations_json[day_transcations_key] = day_transactions.to_json(simple=simple)
                
        return {
            "year": self.year,
            "month": self.month,
            "transaction_count": self.transaction_count,
            "pay_expenses_count": self.pay_expenses_count,
            "take_in_count": self.take_in_count,
            "no_include_count": self.no_include_count,
            "pay_expenses": self.pay_expenses,
            "take_in": self.take_in,
            "no_include": self.no_include,
            "day_transcations": day_transcations_json,
        }
    
    def analysis_transaction(self, transaction: Transaction):
        """更新补全每月账单信息

        Args:
            transaction (Transaction): 交易对象
        """
        
        self.transaction_count += 1
        
        # 将交易金额转换为浮点数
        try:
            transaction_amount = float(transaction.amount)
        except ValueError:
            transaction_amount = 0.0
        
        # 根据交易类型更新计数和金额
        if "支出" in transaction.income_expense:
            self.pay_expenses_count += 1
            self.pay_expenses += transaction_amount
        elif "收入" in transaction.income_expense:
            self.take_in_count += 1
            self.take_in += transaction_amount
        else:
            self.no_include_count += 1
            self.no_include += transaction_amount


    def add_transaction(self, transaction: Transaction):
        
        check_month = transaction.get_datetime().month == self.month
        check_year = transaction.get_datetime().year == self.year
        if check_month and check_year:
            self.analysis_transaction(transaction=transaction)
            day_value = transaction.get_datetime().day
            if day_value not in self.day_transcations.keys():
                self.day_transcations[day_value] = DaysTransaction(year=self.year, month=self.month, day=day_value)
            temp_day_transcation = self.day_transcations[day_value]
            if isinstance(temp_day_transcation, DaysTransaction):
                temp_day_transcation.add_transaction(transaction=transaction)
            self.transactions.append(transaction)
    
    
    def to_DaysTransaction(self) -> dict:
        
        logger.info("Begin set every days transactions.")
        days = []
        result = {}
        for transaction in self.transactions:
            if not isinstance(transaction, Transaction):
                continue
            year = str(transaction.get_datetime().year)
            month = str(transaction.get_datetime().month)
            day = str(transaction.get_datetime().day)
            if day not in days:
                days.append(day)
                result[day] = DaysTransaction(year=int(year), month=int(month), day=int(day))
                result[day].add_transaction(transaction)
            else:
                result[day].add_transaction(transaction)
        
        logger.info(f"days number: {len(result.keys())}")
        
        for day in result.keys():
            item = result[day]
            if isinstance(item, MonthsTransaction):
                logger.info(f"{str(day)}: {str(item.year)}-{str(item.month)}")
            # print_log(f"{year} year {month} month has {len(result.get(year).transactions)} transactions.")
        
        logger.info("Set every years transactions over.")
        return result
