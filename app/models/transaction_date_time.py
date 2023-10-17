#/bin/bash python3

from datetime import datetime
from pydantic import BaseModel

class TransactionDateTime(BaseModel):
    year: str = ''
    month: str = ''
    day: str = ''
    hour: str = ''
    minute: str = ''
    second: str = ''


# class TransactionDateTime:
#     """
#     TransactionDateTime 类用于处理交易的时间信息。

#     Attributes:
#         year (str): 年份。
#         month (str): 月份。
#         day (str): 日。
#         hour (str): 时。
#         minute (str): 分。
#         second (str): 秒。
#     """

#     def __init__(self):
#         """
#         初始化 TransactionDateTime 类的属性。
#         """
#         self.year = ''
#         self.month = ''
#         self.day = ''
#         self.hour = ''
#         self.minute = ''
#         self.second = ''

#     def inject_datetime_str(self, datetime_str: str):
#         """
#         从日期时间字符串中提取时间信息并注入到类属性中。

#         Args:
#             datetime_str (str): 日期时间字符串，格式为 "%Y-%m-%d %H:%M:%S"。

#         Example:
#             inject_datetime_str("2021-11-28 16:05:38")
#         """
#         # 解析日期时间字符串并注入到类属性
#         date_format = "%Y-%m-%d %H:%M:%S"
#         date_object = datetime.strptime(datetime_str, date_format)
#         self.year = date_object.year
#         self.month = date_object.month
#         self.day = date_object.day
#         self.hour = date_object.hour
#         self.minute = date_object.minute
#         self.second = date_object.second

#     def __str__(self):
#         """
#         将对象的属性转换为字符串表示。

#         Returns:
#             str: 对象的字符串表示。
#         """
#         return str(self.__dict__)

#     def get_v_str(self) -> str:
#         """
#         获取日期时间的字符串表示，格式为 "%Y-%m-%d %H:%M:%S"。

#         Returns:
#             str: 日期时间的字符串表示。
#         """
#         return f"{self.year}-{self.month}-{self.day} {self.hour}:{self.minute}:{self.second}"

#     def get_date_info_as_str(self) -> str:
#         """
#         获取日期信息的字符串表示，格式为 "%Y-%m-%d"。

#         Returns:
#             str: 日期信息的字符串表示。
#         """
#         month_ = str(self.month)
#         day_ = str(self.day)
#         if len(str(self.month)) == 1:
#             month_ = "0" + str(self.month)
#         if len(str(self.day)) == 1:
#             day_ = "0" + str(self.day)
#         return f"{self.year}-{month_}-{day_}"

#     def get_time_info_as_number(self) -> float:
#         """
#         获取时间信息的数字表示，格式为小时、分钟和秒的小数形式。

#         Returns:
#             float: 时间信息的数字表示。
#         """
#         return (self.hour * 10000 + self.minute * 100 + self.second) / 10000

#     def show(self):
#         """
#         在控制台中显示对象的时间属性。
#         """
#         print(f"Year: {self.year}")
#         print(f"Month: {self.month}")
#         print(f"Day: {self.day}")
#         print(f"Hour: {self.hour}")
#         print(f"Minute: {self.minute}")
#         print(f"Second: {self.second}")

#     def is_target_day(self, year: int, month: int, day: int) -> bool:
#         """
#         检查对象的时间是否与指定日期匹配。

#         Args:
#             year (int): 指定的年份。
#             month (int): 指定的月份。
#             day (int): 指定的日。

#         Returns:
#             bool: 如果时间匹配指定日期，则返回 True；否则返回 False。
#         """
#         return self.year == year and self.month == month and self.day == day

#     def is_target_month(self, year: int, month: int) -> bool:
#         """
#         检查对象的时间是否与指定年份和月份匹配。

#         Args:
#             year (int): 指定的年份。
#             month (int): 指定的月份。

#         Returns:
#             bool: 如果时间匹配指定年份和月份，则返回 True；否则返回 False。
#         """
#         return self.year == year and self.month == month

#     def is_target_year(self, year: int, month: int) -> bool:
#         """
#         检查对象的时间是否与指定年份匹配。

#         Args:
#             year (int): 指定的年份。
#             month (int): 指定的月份。

#         Returns:
#             bool: 如果时间匹配指定年份，则返回 True；否则返回 False。
#         """
#         return self.year == year
