#!/usr/bin/env python

from typing import Union
from fastapi import FastAPI, Depends, HTTPException
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request

from models.transaction import Transaction
from api.file_upload.v1 import file_upload_api
from api.user.v1 import user_api
from api.transaction.v1 import transaction_api

app = FastAPI()
app.include_router(file_upload_api.router, prefix="/api/v1/file_upload")
app.include_router(user_api.router, prefix="/api/v1/user")
app.include_router(transaction_api.router, prefix="/api/v1/transaction_api")

app.add_middleware(SessionMiddleware, secret_key="your-secret-key")


@app.get("/")
def read_root(request: Request):
    request.session["key"] = "value"
    print()
    return {"Hello": "World"}