import aiohttp
import time
import fcntl
async def get_logs_from_api(count: int = 50):
    url = "http://fastapi-app:8080/logs/"  # Замените на фактический URL вашего API

    params = {"count": count}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                # Обработка ошибок, если необходимо
                return None
async def logs_handler(logs_data):
    success_count = 0
    for log_data in logs_data:
        status = log_data["log"]["status_code"]
        if int(status)-200<100:
            success_count += 1
    return round(success_count/len(logs_data)*100, 2)
# Пример использования
async def main():
    logs_data = await get_logs_from_api()
    if logs_data:
        result = await logs_handler(logs_data)
        with open("handler_results.txt", "a") as file:
            fcntl.flock(file, fcntl.LOCK_EX)
            file.write(f"The percentage of successful responses among the last 50 that were recorded on the server is {result} %\n")
            fcntl.flock(file, fcntl.LOCK_UN)

        print(result)
    else:
        print("Failed to fetch logs data")

# Запуск основной функции
if __name__ == "__main__":
    """_summary_
    calculate persent success http response
    """
    import asyncio
    while True:
        asyncio.run(main())
        time.sleep(10)