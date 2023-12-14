import os
from dotenv import load_dotenv
import time
import multiprocessing
import random
import string
import aiohttp
import asyncio
import json
import fcntl

def gen_log_str() -> str:
    """_summary_
        generate log_str in format '{ip} {http_method} {uri} {http_status}'
    Returns:
        str: _description_
        log_str
    """
    ip = generate_random_ip()
    http_method = generate_randop_http_method()
    uri = generate_random_uri()
    http_code = gen_http_code()
    return f"{ip} {http_method} {uri} {http_code}"


def gen_http_code() -> int:
    return random.randint(1, 1000)


def generate_random_uri() -> str:
    """_summary_
        generate random true or false uri
    Returns:
        str: _description_
        uri
    """
    if random.randint(0, 2) == 0:
        return f"https://{generate_random_string(4,6)}.{generate_random_string(3,4)}/{generate_random_string(5,9)}"
    else:
        return f"{generate_random_string(4,6)}/{generate_random_string(5,9)}"


def generate_randop_http_method() -> str:
    """_summary_
    generate_random_http_method
    Returns:
        str: _description_
        http_method
    """
    http_methods = ['OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT',
                    'options', 'get', 'head', 'post', 'put', 'delete', 'trace', 'connect']
    if random.randint(0, 100) < 70:
        return random.choice(http_methods)
    else:
        return generate_random_string(3, 5)


def generate_random_string(len_min, len_max) -> str:
    length = random.randint(len_min, len_max)
    characters = string.ascii_letters
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def generate_random_ip() -> str:
    """_summary_
    gen random_api
    Returns:
        str: _description_
        random api
    """
    octet_count = random.randint(4, 5)
    octets = []
    for _ in range(octet_count):
        octets.append(str(random.randint(0, 300)))
    return ".".join(octets)


async def send_log_str_to_api(log_str):
    api_url = "http://fastapi-app:8080/logs/"
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'log': log_str})
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, data=data, headers=headers) as response:
            if response.status == 201:
                print(f"Log string successfully sent to API: {log_str}")
            else:
                print(
                    f"Failed to send log string to API. HTTP status code: {response.status}")


def write_to_file(file_path, time_sleep):
    count = 0
    while True:
        with open(file_path, 'a') as file:
            log_str = gen_log_str()
            fcntl.flock(file, fcntl.LOCK_EX)
            file.write(f"{log_str}\n")
            fcntl.flock(file, fcntl.LOCK_UN)  
            count += 1
            asyncio.run(send_log_str_to_api(log_str))
            time.sleep(time_sleep/1000.0)


if __name__ == '__main__':
    load_dotenv()
    PROCESS_COUNT = int(os.getenv("PROCESS_COUNT"))
    SLEEP_TIME_MS = int(os.getenv("SLEEP_TIME_MS"))
    file_path = 'writer_logs.txt'
    processes = []

    for i in range(0, PROCESS_COUNT):  # Количество процессов
        process = multiprocessing.Process(
            target=write_to_file, args=(file_path, SLEEP_TIME_MS))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()  # Ждем завершения всех процессов

    print("All processes have finished writing to the file.")
# Загрузить переменные окружения из файла .env
