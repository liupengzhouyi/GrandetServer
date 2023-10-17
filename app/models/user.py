#！/usr/bin/env python

from pydantic import BaseModel


class User(BaseModel):
    username: str=''
    password: int=''
    token: str=''