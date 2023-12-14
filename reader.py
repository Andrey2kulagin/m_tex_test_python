import aiohttp
import time
async def get_logs_from_api(count: int = 50):
    url = "http://127.0.0.1:9000/user/"  # Замените на фактический URL вашего API

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
        print(result)
    else:
        print("Failed to fetch logs data")

# Запуск основной функции
if __name__ == "__main__":
    import asyncio
    while True:
        asyncio.run(main())
        time.sleep(10)