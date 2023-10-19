import json
import logging

from models.transaction import Transaction
from models.months_transaction import MonthsTransaction
from settings import log_file_path

logging.basicConfig(filename=log_file_path,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class YearsTransaction:
    
    
    def __init__(self, year: int) -> None:
        
        self.year = year
        self.transactions = []
        self.month_transcations = {}
        
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
        
    
    def to_json(self, simple: bool=True):
        
        month_transcations_json = {}
        for month_transcations_key in self.month_transcations.keys():
            month_transactions = self.month_transcations.get(month_transcations_key)
            if isinstance(month_transactions, MonthsTransaction):
                month_transcations_json[month_transcations_key] = month_transactions.to_json(simple=simple)
                
        return {
            "year": self.year,
            "transaction_count": self.transaction_count,
            "pay_expenses_count": self.pay_expenses_count,
            "take_in_count": self.take_in_count,
            "no_include_count": self.no_include_count,
            "pay_expenses": self.pay_expenses,
            "take_in": self.take_in,
            "no_include": self.no_include,
            "month_transcations": month_transcations_json,
        }
        
        
    def analysis_transaction(self, transaction: Transaction):
        """更新补全每年账单信息

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
        
        check_year = transaction.get_datetime().year == self.year
        if check_year:
            self.analysis_transaction(transaction=transaction)
            self.transactions.append(transaction)
            month = transaction.get_datetime().month
            if month not in self.month_transcations.keys():
                self.month_transcations[month] = MonthsTransaction(year=self.year, month=month)
            temp_month_transcation = self.month_transcations[month]
            if isinstance(temp_month_transcation, MonthsTransaction):
                temp_month_transcation.add_transaction(transaction=transaction)


    def to_MonthsTransaction(self) -> dict:
        
        logger.info("Begin set every years transactions.")
        months = []
        result = {}
        for transaction in self.transactions:
            if not isinstance(transaction, Transaction):
                continue
            year = str(transaction.get_datetime().year)
            month = str(transaction.get_datetime().month)
            if month not in months:
                months.append(month)
                result[month] = MonthsTransaction(year=int(year), month=int(month))
                result[month].add_transaction(transaction)
            else:
                result[month].add_transaction(transaction)
        
        logger.info(f"months number: {len(result.keys())}")
        
        for month in result.keys():
            item = result[month]
            if isinstance(item, MonthsTransaction):
                logger.info(f"{str(month)}: {str(item.year)}-{str(item.month)}")
            # logger.info(f"{year} year {month} month has {len(result.get(year).transactions)} transactions.")
        
        logger.info("Set every years transactions over.")
        return result
