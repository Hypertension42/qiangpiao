import redis 
import mysql.connector

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

db = mysql.connector.connect(
    host="localhost"
    user="root"
    password=""
    database="qiangpiao_db"
    unix_socket="/run/mysqld/mysqld.sock"
)
cursor = db.cursor()


try:
    r.ping()
    print("Redis connected success")
except Exception as e:
    print(f"Redis connecting failed:{e}")

