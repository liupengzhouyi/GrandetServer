#/bin/bash python3


log_file_path = "./../log/log.log"


def print_log(info: str):
    
    log_str = f"log: {info}"
    print(log_str)
    with open(log_file_path, 'a') as f:
        f.write(f"{log_str}\n")
    