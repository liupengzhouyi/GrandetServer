
from pydantic import BaseModel


class YearsTransaction(BaseModel):
    year: int = -1
    transactions: list = []
    

# class YearsTransaction:
    
    
#     def __init__(self, year: int) -> None:
        
#         self.year = year
#         self.transactions = []


#     def add_transaction(self, transaction: Transaction):
        
#         self.transactions.append(transaction)


#     def to_MonthsTransaction(self) -> dict:
        
#         print_log("Begin set every years transactions.")
#         months = []
#         result = {}
#         for transaction in self.transactions:
#             if not isinstance(transaction, Transaction):
#                 continue
#             year = str(transaction.get_datetime().year)
#             month = str(transaction.get_datetime().month)
#             if month not in months:
#                 months.append(month)
#                 result[month] = MonthsTransaction(year=int(year), month=int(month))
#                 result[month].add_transaction(transaction)
#             else:
#                 result[month].add_transaction(transaction)
        
#         print_log(f"months number: {len(result.keys())}")
        
#         for month in result.keys():
#             item = result[month]
#             if isinstance(item, MonthsTransaction):
#                 print_log(f"{str(month)}: {str(item.year)}-{str(item.month)}")
#             # print_log(f"{year} year {month} month has {len(result.get(year).transactions)} transactions.")
        
#         print_log("Set every years transactions over.")
#         return result
