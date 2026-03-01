import threading
import time
import random
redis_stock = 5
task_queue = []
db_records = []

def handle_request(user_id):
    global redis_stock
    redis_stock = redis_stock - 1
    current = redis_stock
if redis_stock > 0:
    task_queue.append(user_id)
    pass

def worker():
    while True:
        if task_queue:
            user_id = task_queue.pop(0)
            print(f"worker: successfully get the ticket for user {user_id}")
        time.sleep(0.5)

threading.Thread(target=worker, daemon=True).start()

for i in range(10):
    handle_request(f"user-{i}")
    time.sleep(0.1)











