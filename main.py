import redis
import mysql.connector
import threading
import time


r = redis.Redis(host='localhost', port=6379,decode_responses=True)
db = mysql.connector.connect(
    host="localhost",
    user="kaisei",
    password="",
    database="qiangpiao_db",
    unix_socket="/run/mysqld/mysqld.sock"
)
cursor = db.cursor()

def handle_request(user_id):
    if r.sadd("bought",user_id) == 0:
        print(f"[{user_id}] refuse: repeating request")
        return
    
    current = r.decr("tickets")
    if current < 0:
        r.incr("tickets")
        print(f"[{user_id}] there is no tickets:(")
    else:
        r.rpush("order_queue",user_id)
        print(f"[{user_id}]purchasing tickets successful") 
    
def mysql_worker():
    while True:
        task = r.blpop("order_queue", timeout=1)
        if task:
            user_id = task[1]
            try:
                sql = "INSERT INTO orders (user_id) VALUES (%s)"
                cursor.execute(sql, (user_id,))
                db.commit()
                print(f"    >>> [DB] successfully insert user{user_id} the ticket")
            except Exception as e:
                print(f"    !!! [DB] insert failed:{e}")
        time.sleep(0.1)

r.set("tickets", 5)
r.delete("bought")

threading.Thread(target=mysql_worker, daemon=True).start()

for i in range(1,11):
    handle_request(f"User_{i}")

time.sleep(5)
print("--- experiment finished ---")








