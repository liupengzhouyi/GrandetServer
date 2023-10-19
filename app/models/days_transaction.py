#/bin/bash python3

import json

from models.transaction import Transaction


class DaysTransaction():
    
    def __init__(self, year: int, month: int, day: int) -> None:
        
        self.year = year
        self.month = month
        self.day = day
        self.transactions = []
        
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
        
        day_transactions4json = {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "transaction_count": self.transaction_count,
            "pay_expenses_count": self.pay_expenses_count,
            "take_in_count": self.take_in_count,
            "no_include_count": self.no_include_count,
            "pay_expenses": self.pay_expenses,
            "take_in": self.take_in,
            "no_include": self.no_include,
        }
        transactions4json = []
        if not simple:
            for transaction in self.transactions:
                if isinstance(transaction, Transaction):
                    transactions4json.append(transaction.to_json())
        day_transactions4json["transactions"] = transactions4json
        return day_transactions4json
            

    
    def analysis_transaction(self, transaction: Transaction):
        """更新补全每日账单信息

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
        
        check_day = transaction.get_datetime().day == self.day
        check_month = transaction.get_datetime().month == self.month
        check_year = transaction.get_datetime().year == self.year
        if check_day and check_month and check_year:
            self.analysis_transaction(transaction=transaction)  
            self.transactions.append(transaction)
    
    
    def get_target_transactions(self, target_day: int) -> list:
        
        target_transactions = []
        for transaction in self.transactions:
            check_day = transaction.get_datetime().day == self.day
            check_month = transaction.get_datetime().month == self.month
            check_year = transaction.get_datetime().year == self.year
            if check_day and check_month and check_year:
                target_transactions.append(transaction)
                self.analysis_transction(transaction=transaction)
        return target_transactions
