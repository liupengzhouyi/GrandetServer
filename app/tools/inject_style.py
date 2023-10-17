#/bin/bash python3

from models.transaction import Transaction


class InjectStyle:
    """
    用于在交易数据中注入样式信息的辅助类。
    """

    def __init__(self, style: str):
        """
        初始化一个注入样式信息的对象。

        Args:
            style (str): 要注入的样式信息。
        """
        self.style = style

    @classmethod
    def add_source_in_head(cls, transaction_head: list, source: str) -> list:
        """
        在交易数据表头中添加来源信息。

        Args:
            transaction_head (list): 交易数据表头字段名列表。
            source (str): 要添加的来源信息。

        Returns:
            list: 更新后的交易数据表头字段名列表。
        """
        transaction_head.append(source)
        return transaction_head

    @classmethod
    def add_source(cls, transaction: Transaction, source: str) -> Transaction:
        """
        在交易对象中添加来源信息。

        Args:
            transaction (Transaction): 要添加来源信息的交易对象。
            source (str): 要添加的来源信息。

        Returns:
            Transaction: 更新后的交易对象。
        """
        transaction.source = source
        return transaction

        
    
        