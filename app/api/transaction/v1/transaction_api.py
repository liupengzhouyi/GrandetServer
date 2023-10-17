#!/usr/bin/env python3
#!coding=utf-8


from fastapi import APIRouter, Depends
from starlette.requests import Request
import json
import logging


from api.file_upload.v1.file_upload_api import get_user_all_bills_files
from models.transaction import Transaction
from tools.transaction_tools import TransactionTools
from tools.transactions_tools import TransactionsTools
from settings import log_file_path


router = APIRouter()


logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@router.get("/get_all_transactions")
async def get_all_transaction(request: Request) -> dict:
    
    result = {
        "status": False,
        "reason": "",
        "transactions": []
    }
    
    # Step 1: Get the user file paths
    user_files_result = get_user_all_bills_files(request)
    
    if not user_files_result['status']:
        result["reason"] = user_files_result['reason']
        return result
    
    file_paths = user_files_result['file_paths']
    
    # Step 2: Use TransactionTools to get all transactions
    transactions = TransactionsTools.init_transactions_by_files(file_paths)
    result["transactions"] = transactions[78:100]
    
    print(f"transactions len: {str(len(transactions))}")
    
    # Step 3: Return the result
    return result

