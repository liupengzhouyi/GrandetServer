# ./api/v1/endpoints/user.py

import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from pathlib import Path
from starlette.requests import Request
import logging

from settings import app_root_path
from settings import upload_folder
from settings import log_file_path

from tools.read_transaction_table_tools import ReadTransactionTable


router = APIRouter()

logging.basicConfig(filename=log_file_path,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_user_directory(upload_folder: str, user_name: str):
    # 创建主文件存储目录（如果不存在）
    main_location = Path(upload_folder)
    main_location.mkdir(exist_ok=True)

    # 在主目录下为用户创建子目录
    user_directory = main_location / user_name
    user_directory.mkdir(exist_ok=True)

    return user_directory  # 返回用户目录的路径，以便后续使用


@router.post("/get_upload_folder/", tags=["file_operation"])
def get_user_folder_path(request: Request):
    """
    获取当前登录用户的文件夹路径。

    :param request: FastAPI 的请求对象，用于获取 session 数据。
    :return: 包含 status, reason 和 folder_path 的字典。
    """
    
    # 初始化返回结果
    result = {
        "status": False,
        "reason": "",
        "folder_path": ""
    }

    # 从 session 获取用户信息
    # user_name = request.session.get("user_name")
    # login_status = request.session.get("login_status")
    user_name = request.cookies.get("user_name")
    login_status = request.cookies.get("login_status")

    # 检查用户是否登录
    if not login_status:
        result["reason"] = "User not logged in."
        logger.info(f"Attempt to access folder path without logging in.")
        return result

    # 获取用户文件夹路径
    user_directory = Path(upload_folder) / user_name

    # 检查文件夹是否存在
    if not user_directory.exists():
        result["reason"] = f"Folder for user {user_name} does not exist."
        logger.warning(f"Attempt to access non-existent folder for user {user_name}.")
        return result

    # 更新返回结果
    result["status"] = True
    result["reason"] = "Success"
    result["folder_path"] = str(user_directory)
    logger.info(f"Successfully retrieved folder path for user {user_name}.")
    
    return result


@router.post("/uploadfile/", tags=["file_operation"])
async def upload_file(request: Request, file: UploadFile = File(...), user_name: str="", login_status: bool=False):
    
    log_info = f"Begin upload file."
    logger.info(log_info)
    upload_file_result = {"upload_file_status": False, "message": "File uploaded failed!", "file_name": ""}
    # user_name = request.session.get("user_name")
    # login_status = request.session.get("login_status")
    
    user_name = request.cookies.get("user_name")
    login_status = request.cookies.get("login_status")
    
    if not login_status:
        log_info = "User not longin, Please login."
        logger.info(log_info)
        upload_file_result["upload_file_status"] = False
        upload_file_result["message"] = "User not longin, Please login."
        return upload_file_result
    try:
        user_directory = create_user_directory(upload_folder=upload_folder, user_name=user_name)
        if not os.path.exists(user_directory):
            log_info = f"Path: {user_directory} was not existed."
            upload_file_result["file_name"] = file.filename
            upload_file_result["upload_file_status"] = False
            upload_file_result["message"] = "Folder not existed!"
        else:
            # 写入文件
            with (user_directory / file.filename).open("wb+") as buffer:
                buffer.write(file.file.read())
            upload_file_result["file_name"] = file.filename
            upload_file_result["upload_file_status"] = True
            upload_file_result["message"] = "File uploaded successfully!"
            log_info = f"User: {user_name} upload file: {file.filename} to {user_directory}."
        logger.info(log_info)
        return upload_file_result
    except Exception as e:
        log_info = ""
        raise HTTPException(status_code=400, detail=f"File upload failed!")


@router.post("/get_user_all_files/", tags=["file_operation"])
def get_all_user_files(request: Request, user_name: str="", login_status: bool=False) -> dict:
    """
    获取指定用户文件夹下的所有文件。

    :param request: FastAPI 的请求对象，用于获取 session 数据。
    :param upload_folder: 主上传文件夹的路径。
    :return: 包含 status, reason 和 file_paths 的字典。
    """
    
    # 初始化返回结果
    result = {
        "status": False,
        "reason": "",
        "file_paths": []
    }

    # 从 session 获取用户信息
    # user_name = request.session.get("user_name")
    # login_status = request.session.get("login_status")
    # user_name = request.cookies.get("user_name")
    # login_status = request.cookies.get("login_status")

    # 检查用户是否登录
    if not login_status:
        result["reason"] = "User not logged in."
        logger.info(f"Attempt to access files without logging in.")
        return result

    # 获取用户文件夹路径
    user_directory = os.path.join(str(app_root_path), upload_folder, user_name)

    # 检查文件夹是否存在
    if not os.path.exists(user_directory):
        result["reason"] = f"Folder for user {user_name} does not exist."
        logger.warning(f"Attempt to access non-existent folder for user {user_name}.")
        return result

    # 获取文件夹下的所有文件
    all_files = ReadTransactionTable.extract_all_file_path(user_directory)

    # 更新返回结果
    result["status"] = True
    result["reason"] = "Success"
    result["file_paths"] = [str(f) for f in all_files]
    logger.info(f"Successfully retrieved files for user {user_name}.")
    
    return result


@router.post("/get_user_all_bills_files/", tags=["file_operation"])
def get_user_all_bills_files(request: Request, user_name: str="", login_status: bool=False, simple: bool=True) -> dict:
    
    """
    获取指定用户文件夹下的所有账单文件。

    :param request: FastAPI 的请求对象，用于获取 session 数据。
    :return: 包含 status, reason 和 file_paths 的字典。
    """
    
    result = get_user_all_bills_files_core(request=request, user_name=user_name, login_status=login_status, simple=simple)
    return JSONResponse(content=result, media_type="application/json; charset=utf-8")
    
    

@router.post("/get_user_all_bills_files_core/", tags=["file_operation"])
def get_user_all_bills_files_core(request: Request, user_name: str="", login_status: bool=False, simple: bool=True) -> dict:
    
    """
    获取指定用户文件夹下的所有账单文件。

    :param request: FastAPI 的请求对象，用于获取 session 数据。
    :return: 包含 status, reason 和 file_paths 的字典。
    """
    
    # 初始化返回结果
    result = {
        "status": False,
        "reason": "",
        "file_paths": []
    }
    
    # 从 session 获取用户信息
    # user_name = request.session.get("user_name")
    # login_status = request.session.get("login_status")
    # user_name = request.cookies.get("user_name")
    # login_status = request.cookies.get("login_status")

    # 检查用户是否登录
    if not login_status:
        result["reason"] = "User not logged in."
        logger.info(f"Attempt to access files without logging in.")
        return result

    # 获取用户文件夹路径
    user_directory = os.path.join(str(app_root_path), upload_folder, user_name)

    # 检查文件夹是否存在
    if not os.path.exists(user_directory):
        result["reason"] = f"Folder for user {user_name} does not exist."
        logger.warning(f"Attempt to access non-existent folder for user {user_name}.")
        return result

    # 获取文件夹下的所有文件
    all_files = ReadTransactionTable.extract_all_file_path(user_directory)
    target_csv_files = ReadTransactionTable.flitter_csv_file(all_files)
    
    # 更新返回结果
    result["status"] = True
    result["reason"] = "Success"
    if simple:
        result["file_paths"] = [os.path.basename(str(f)) for f in target_csv_files]
    else:
        result["file_paths"] = [str(f) for f in target_csv_files]
    # print(result["file_paths"])
    logger.info(f"Successfully retrieved files for user {user_name}.")
    return result