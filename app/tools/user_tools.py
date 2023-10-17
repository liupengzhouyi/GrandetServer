#!/usr/bin/env python3

import logging

from core.consistent_hash import ConsistentHash
from models.user import User
from settings import log_file_path

logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UserTools:
    
    @classmethod
    def show_user(cls, user: User):
        print(f"username: {user.username}")
        print(f"password hash: {user.password}")


    @classmethod
    def get_password_hash(cls, password: str) -> int:
        
        ch = ConsistentHash()
        return ch.hash(str(password))
    
    
    @classmethod
    def check_password(cls, user: User, password_hash: str) -> bool:
        
        logger.info(f"The password hash value in DB is: {str(user.password)}")
        return int(user.password) == int(password_hash)
    
    @classmethod
    def check_user_existed(cls, user: User) -> bool:
        
        if not user.username:
            return False
        return True