

from datetime import datetime
from models.transaction_date_time import TransactionDateTime


class TransactionDateTimeTools:
    
    @classmethod
    def inject_datetime_str(cls, transaction_datetime: TransactionDateTime, datetime_str: str):
        """
        从日期时间字符串中提取时间信息并注入到类属性中。

        Args:
            datetime_str (str): 日期时间字符串，格式为 "%Y-%m-%d %H:%M:%S"。

        Example:
            inject_datetime_str("2021-11-28 16:05:38")
        """
        # 解析日期时间字符串并注入到类属性
        date_format = "%Y-%m-%d %H:%M:%S"
        date_object = datetime.strptime(datetime_str, date_format)
        transaction_datetime.year = date_object.year
        transaction_datetime.month = date_object.month
        transaction_datetime.day = date_object.day
        transaction_datetime.hour = date_object.hour
        transaction_datetime.minute = date_object.minute
        transaction_datetime.second = date_object.second
        
        
    @classmethod
    def get_v_ser(cls, transaction_datetime: TransactionDateTime) -> str:
        
        """
        获取日期时间的字符串表示，格式为 "%Y-%m-%d %H:%M:%S"。

        Returns:
            str: 日期时间的字符串表示。
        """
        return f"{transaction_datetime.year}-{transaction_datetime.month}-{transaction_datetime.day} {transaction_datetime.hour}:{transaction_datetime.minute}:{transaction_datetime.second}"