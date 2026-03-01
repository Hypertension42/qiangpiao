# High-Concurrency Seckill System (MVP)

A high-performance ticket purchasing system prototype built with FastAPI, Redis, and MariaDB.

## Performance 
- - **Throughput:** 506.83 QPS (Tested on Arch Linux)
- **Concurrency:** Handled 1000 requests in 1.97s
- **Reliability:** 100% Data Consistency (Verified via MySQL audit)

## 🏗️ Architecture
- **FastAPI:** High-performance web interface.
- **Redis:** Atomic inventory management & idempotent request filtering.
- **Asynchronous Worker:** Decoupled database persistence to prevent IO blocking.
- **Semaphore Control:** Client-side concurrency smoothing during stress tests.

## 🛠️ How to run
1. Start Redis & MariaDB
2. `pip install -r requirements.txt`
3. `uvicorn main:app --workers 4`