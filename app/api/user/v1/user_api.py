from fastapi import APIRouter, Depends

from fastapi.responses import JSONResponse

from mysql.connector import cursor
from starlette.requests import Request
import json
import logging

from databases.db_link import get_db
from models.user import User
from tools.user_tools import UserTools
from settings import log_file_path

router = APIRouter()


logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@router.get("/users/", tags=["User"])
async def get_users(db: cursor.MySQLCursor = Depends(get_db)):
    
    query = "SELECT * FROM users"
    db.execute(query)
    result = db.fetchall()
    if result:
        return {"users": result}
    else:
        return {"error": "User not found"}
    
@router.get("/users/{user_id}", tags=["User"])
async def get_user(user_id: int,
                   db: cursor.MySQLCursor = Depends(get_db)):
    query = "SELECT * FROM users WHERE id = %s"
    print(type(db))
    db.execute(query, (user_id,))
    result = db.fetchall()
    
    if result:
        return {"user_id": result[0][0], "username": result[0][1]}
    else:
        return {"error": "User not found"}
    
@router.get("/users/{user_id}", tags=["User"])
async def get_user_by_name(user_name: str, db: cursor.MySQLCursor = Depends(get_db)) -> User:
    
    log_info = "Get user info by username:{}.".format(user_name)
    logger.info(log_info)
    query = "SELECT * FROM users WHERE name = %s"
    db.execute(query, (user_name,))
    result = db.fetchall()
    user = User()
    if result:
        log_info = "Get user:{} info success.".format(user_name)
        logger.info(log_info)
        user.username = result[0][1]
        user.password = result[0][3]
    else:
        log_info = "Get user:{} info failed.".format(user_name)
        logger.info(log_info)
    return user


@router.get("/user_name/{user_name}", tags=["User"])
async def insert_user(request: Request,
                      user_name: str,
                      password_hash: str,
                      db: cursor.MySQLCursor = Depends(get_db)) -> bool:
    
    query = "INSERT INTO users (name, password_hash_value) VALUES (%s, %s)"
    db.execute(query, (user_name, password_hash))
    result = db.fetchone()
    db.execute("COMMIT")
    
    user = await get_user_by_name(user_name=user_name, db=db)
    return UserTools.check_user_existed(user=user)


# @router.post("/login", tags=["User"])
@router.get("/login", tags=["User"])
async def login(request: Request, user_name: str, password: str, db: cursor.MySQLCursor = Depends(get_db)):
    
    log_info = f"User name:{user_name}; Password:{password}."
    logger.info(log_info)
    print(log_info)
    user: User = await get_user_by_name(user_name=user_name, db=db)
    
    if not UserTools.check_user_existed(user=user):
        log_info = f"User not existed."
        logger.info(log_info)
        return {"login_status": False, "login_failed_reason": "User not existed"}
    
    UserTools.show_user(user)
    password_hash_value = UserTools.get_password_hash(password=password)
    logger.info(f"input password_hash_value: {str(password_hash_value)}.", )
    request.session["user_name"] = user_name
    if UserTools.check_password(user=user, password_hash=password_hash_value):
        request.session["login_status"] = True
        log_info = f"Check password success."
    else:
        request.session["login_status"] = False
        log_info = f"Check password failed."
    logger.info(log_info)
    
    login_result = {"user": user_name, "login_status": request.session.get("login_status")}
    
    headers = {"Access-Control-Allow-Origin": "*"}
    return JSONResponse(content=login_result, headers=headers)


@router.post("/register", tags=["User"])
async def register(request: Request,
                   username: str,
                   password: str,
                   check_password: str,
                   db: cursor.MySQLCursor = Depends(get_db)):
    
    log_info = f"Registered user: {username}."
    logger.info(log_info)
    
    register_status = False
    register_failed_reason = ""
    user: User = await get_user_by_name(user_name=username, db=db)
    
    if UserTools.check_user_existed(user=user):
        log_info = f"User was existed."
        logger.info(log_info)
        register_failed_reason = f"User {username} was existed."
        register_reason = {"register_status": register_status, "register_failed_reason": register_failed_reason}
        return register_reason
    
    password_hash_value = UserTools.get_password_hash(password=password)
    check_password_hash_value = UserTools.get_password_hash(password=check_password)
    if password_hash_value != check_password_hash_value:
        log_info = f"Password not match."
        logger.info(log_info)
        register_failed_reason = "Password not match"
    else:
        if await insert_user(request=request, user_name=username, password_hash=check_password_hash_value, db=db):
            log_info = f"Insert user success."
            logger.info(log_info)
            register_status = True
        else:
            log_info = f"Insert user failed."
            logger.info(log_info)
            register_status = False
    
    register_reason = {"register_status": register_status, "register_failed_reason": register_failed_reason}
    return register_reason


@router.delete("/delete-user", tags=["User"])
def delete_user(username: str, password: str):
    
    return {"message": "User deleted successfully"}