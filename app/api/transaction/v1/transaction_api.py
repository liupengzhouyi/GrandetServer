#!/usr/bin/env python3
#!coding=utf-8


from fastapi import APIRouter, Depends
from starlette.requests import Request
import json
import logging


from api.file_upload.v1.file_upload_api import get_user_all_bills_files_core
from models.transaction import Transaction
from tools.transaction_tools import TransactionTools
from tools.transactions_tools import TransactionsTools
from settings import log_file_path


router = APIRouter()


logging.basicConfig(filename=log_file_path,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@router.get("/get_all_transactions", tags=["transaction"])
async def get_all_transaction(request: Request, user: str="", login_status: bool=False) -> dict:
    
    result = {
        "status": False,
        "reason": "",
        "transactions_count": 0,
        "transactions": {}
    }
    login_status = True
    # Step 1: Get the user file paths
    user_files_result = get_user_all_bills_files_core(request=request,
                                                      user_name=user,
                                                      login_status=login_status,
                                                      simple=False)

    if not user_files_result['status']:
        result["reason"] = user_files_result['reason']
        return result
    
    file_paths = user_files_result['file_paths']
    
    # Step 2: Use TransactionTools to get all transactions
    transactions = TransactionsTools.init_transactions_by_files(file_paths)
    
    result["transactions_count"] = len(transactions)
    if len(transactions) != 0:
        result["status"] = True
        
    print(f"transactions len: {str(len(transactions))}")
    
    # transactions = transactions[1:500]
    
    years_transactions = TransactionsTools.genaration_year_transaction(transactions=transactions)
    
    simpor_info = TransactionsTools.years_transactions_to_json(years_transactions=years_transactions, simple=False)
    
    result["transactions"] = simpor_info
    
    
    # Step 3: Return the result
    return result

