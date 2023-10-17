
from pydantic import BaseModel


class MonthsTransaction(BaseModel):
    year: int = -1
    month:int = -1
    transactions: list = []
  
# class MonthsTransaction:
    
#     def __init__(self, year: int, month: int) -> None:
        
#         self.year = year
#         self.month = month
#         self.transactions = []


#     def add_transaction(self, transaction: Transaction):
        
#         self.transactions.append(transaction)
    
    
#     def to_DaysTransaction(self) -> dict:
        
#         print_log("Begin set every days transactions.")
#         days = []
#         result = {}
#         for transaction in self.transactions:
#             if not isinstance(transaction, Transaction):
#                 continue
#             year = str(transaction.get_datetime().year)
#             month = str(transaction.get_datetime().month)
#             day = str(transaction.get_datetime().day)
#             if day not in days:
#                 days.append(day)
#                 result[day] = DaysTransaction(year=int(year), month=int(month), day=int(day))
#                 result[day].add_transaction(transaction)
#             else:
#                 result[day].add_transaction(transaction)
        
#         print_log(f"days number: {len(result.keys())}")
        
#         for day in result.keys():
#             item = result[day]
#             if isinstance(item, MonthsTransaction):
#                 print_log(f"{str(day)}: {str(item.year)}-{str(item.month)}")
#             # print_log(f"{year} year {month} month has {len(result.get(year).transactions)} transactions.")
        
#         print_log("Set every years transactions over.")
#         return result
