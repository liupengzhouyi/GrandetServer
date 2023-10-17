#/bin/bash python3


from pydantic import BaseModel

from core.log4py import print_log
from models.transaction import Transaction


class DaysTransaction(BaseModel):
    year: int = -1
    month:int = -1
    day: int = -1
    transactions: list = []
    
    # def __init__(self, year: int, month: int, day: int) -> None:
        
    #     self.year = year
    #     self.month = year
    #     self.day = day
    #     self.transactions = []


    # def add_transaction(self, transaction: Transaction):
        
    #     self.transactions.append(transaction)
        
    # def get_target_transactions(self, target_day: int) -> list:
        
    #     target_transactions = []
    #     for transaction in self.transactions:
    #         if transaction.get_datetime().day == target_day:
    #             target_transactions.append(transaction)
    #     return target_transactions
