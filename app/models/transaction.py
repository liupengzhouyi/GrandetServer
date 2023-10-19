#/bin/bash python3

from pydantic import BaseModel
from tabulate import tabulate
import json

from models.transaction_date_time import TransactionDateTime

    
class Transaction():
    
    def __init__(self):
        
        self.time_ = TransactionDateTime()
        self.type_ = ''
        self.counterparty = ''
        self.counterparty_number = ''
        self.product = ''
        self.income_expense = ''
        self.amount = ''
        self.payment_method = ''
        self.current_status = ''
        self.transaction_number = ''
        self.merchant_number = ''
        self.remark = ''
        self.source = ''
        self.class_level_1 = ''
        self.class_level_2 = ''
        
        
    def get_datetime(self) -> TransactionDateTime:
        
        return self.time_
    
    def get_value_str_by_name(self, name: str) -> str:

        # 交易时间,交易分类,交易对方,对方账号,商品说明,收/支,金额,    收/付款方式,交易状态,交易订单号,商家订单号,备注,
        # 交易时间,交易类型,交易对方,        商品,   收/支,金额(元),支付方式,   当前状态,交易单号,  商户单号,  备注
        value = ''
        if name  == "交易时间":
            value = self.time_.get_v_str()
        elif name == "交易分类" or name == "交易类型":
            value = self.type_
        elif name == "交易对方":
            value = self.counterparty.replace(" ", "")
        elif name == "对方账号":
            value = self.amount_counter
        elif name == "商品说明" or name == "商品":
            value = self.product
        elif name == "收/支" or name == "收支":
            value = self.income_expense
        elif name == "金额" or name == "金额(元)":
            value = self.amount
        elif name == "收/付款方式" or name == "支付方式":
            value = self.payment_method
        elif name == "交易状态" or name == "当前状态":
            value = self.current_status
        elif name == "交易订单号" or name == "交易单号":
            value = self.transaction_number
        elif name == "商家订单号" or name == "商家单号":
            value = self.merchant_number
        elif name == "备注":
            value = self.remark
        elif name == "来源":
            value = self.source
        elif name == "分类1":
            value = self.class_level_1
        elif name == "分类2":
            value = self.class_level_2
            
        return value
    
    def get_date_info_as_str(self) -> str:
        
        return self.time_.get_date_info_as_str()
        
    
    def get_transaction_number(self) -> str:

        return self.transaction_number
    
    
    def init_by_list(self, infos: list):
        
        # print(f"Infos length: {str(len(infos))}")
        time_ = ''
        type_ = ''
        counterparty = ''
        counterparty_number = ''
        product = ''
        income_expense = ''
        amount = ''
        payment_method = ''
        current_status = ''
        transaction_number = ''
        merchant_number = ''
        remark = ''
        
        #alipay
        if len(infos) == 13:
            time_ = infos[0]
            type_ = infos[1]
            counterparty = infos[2]
            counterparty_number = infos[3]
            product = infos[4]
            income_expense = infos[5]
            amount = infos[6]
            payment_method = infos[7]
            current_status = infos[8]
            transaction_number = infos[9]
            merchant_number = infos[10]
            
            if len(infos) >= 12:
                remark = infos[11]
            else:
                remark = ''
        # wechat
        if len(infos) == 11:
            time_ = infos[0]
            type_ = infos[1]
            counterparty = infos[2]
            counterparty_number = ''
            product = infos[3]
            income_expense = infos[4]
            amount = float(str(infos[5]).replace("¥", ""))
            payment_method = infos[6]
            current_status = infos[7]
            transaction_number = infos[8]
            merchant_number = infos[9]
            
            if len(infos) >= 11:
                remark = infos[10]
            else:
                remark = ''
        
        self.time_.inject_datetime_str(time_)
        self.type_ = type_
        self.counterparty = counterparty
        self.counterparty_number = counterparty_number
        self.product = product
        self.income_expense = income_expense
        self.amount = amount
        self.payment_method = payment_method
        self.current_status = current_status
        self.transaction_number = transaction_number
        self.merchant_number = merchant_number
        self.remark = remark
        self.source = 'alipay'
        
        
    def set_source(self, source):
        
        self.source = source
        
        
    def __str__(self):
        
        return str(self.__dict__)


    def show(self):

        headers = ["Field", "Value"]
        data = [
            ["Time", self.time_.get_v_str()],
            ["Type", self.type_],
            ["Counterparty", self.counterparty],
            ["CounterpartyNumber", self.counterparty_number],
            ["Product", self.product],
            ["Income/Expense", self.income_expense],
            ["Amount", self.amount],
            ["Payment Method", self.payment_method],
            ["Current Status", self.current_status],
            ["Transaction Number", self.transaction_number],
            ["Merchant Number", self.merchant_number],
            ["Remark", self.remark],
            ["Source", self.source]
        ]
        
        print(tabulate(data, headers, tablefmt="simple"))
        
    
    def to_list(self) -> list:
        
        return [self.time_.get_v_str(),
                self.type_,
                self.counterparty,
                self.counterparty_number,
                self.product,
                self.income_expense,
                self.amount,
                self.payment_method,
                self.current_status,
                self.transaction_number,
                self.merchant_number,
                self.remark,
                self.source]
        
    def to_json(self) -> dict:
        
        def serialize(obj):
            if isinstance(obj, TransactionDateTime):
                return obj.get_v_str()  # 或者其他自定义的序列化逻辑
            return obj.__dict__

        return json.loads(json.dumps(self, default=serialize, ensure_ascii=False, indent=4))