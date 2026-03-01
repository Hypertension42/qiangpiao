import asyncio
import httpx
import time

sem = asyncio.Semaphore(100)

async def task(client, i):
    async with sem:
        try:
            await client.get(f"http://127.0.0.1:8000/grab?user_id=user_{i}")
        except Exception:
            pass

async def main():
    limits = httpx.Limits(max_connections=200, max_keepalive_connections=50)
    timeout = httpx.Timeout(30.0)

    async with httpx.AsyncClient(limits = limits, timeout=20.0) as client:
        start = time.time()
        tasks = [task(client, i) for i in range(1000)]
        await asyncio.gather(*tasks)
        end = time.time()
        duration = end - start 

        print(f"1000 diff users purchasing tickets haoshi: {end - start:.2f}s")
        print(f"tuntu value: {1000/(end-start):.2f} QPS")

if __name__ == "__main__":
    asyncio.run(main())