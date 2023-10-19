#!/usr/bin/env python

from typing import Union
from fastapi import FastAPI, Depends, HTTPException
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request

from models.transaction import Transaction
from api.file_upload.v1 import file_upload_api
from api.user.v1 import user_api
from api.transaction.v1 import transaction_api

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 设置允许的源（可以是特定的，也可以是所有）
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "127.0.0.1:61224",
    # 添加更多的源，或使用通配符 "*" 来允许所有源
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许从这些源发送请求
    allow_credentials=True,  # 允许发送 cookies
    allow_methods=["*"],  # 允许所有方法
    # allow_methods=["POST", "GET"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

app.include_router(file_upload_api.router, prefix="/api/v1/file_upload")
app.include_router(user_api.router, prefix="/api/v1/user")
app.include_router(transaction_api.router, prefix="/api/v1/transaction_api")


@app.get("/")
def read_root(request: Request):
    request.session["key"] = "value"
    print()
    return {"Hello": "World"}