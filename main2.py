from fastapi import FastAPI
import redis
import mysql.connector
import threading
import time

app = FastAPI()

# --- 1. 初始化连接 ---
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
db = mysql.connector.connect(
    host="localhost", user="kaisei", password="", 
    database="qiangpiao_db", unix_socket="/run/mysqld/mysqld.sock"
)
cursor = db.cursor()

# --- 2. 核心 API 接口 ---
@app.get("/grab")
def grab_ticket(user_id: str):
    # A. 唯一性检查
    if r.sadd("bought", user_id) == 0:
        return {"status": "fail", "msg": "Already bought"}

    # B. 原子减库存
    current = r.decr("tickets")
    if current < 0:
        r.incr("tickets")
        return {"status": "fail", "msg": "Sold out"}
    
    # C. 异步入队
    r.rpush("order_queue", user_id)
    return {"status": "success", "msg": f"User {user_id} got it!"}

# --- 3. 后台写库工人 ---
def mysql_worker():
    while True:
        task = r.blpop("order_queue", timeout=1)
        if task:
            user_id = task[1]
            try:
                cursor.execute("INSERT INTO orders (user_id) VALUES (%s)", (user_id,))
                db.commit()
            except Exception as e:
                print(f"DB Error: {e}")
        time.sleep(0.01)

# 启动工人线程
threading.Thread(target=mysql_worker, daemon=True).start()