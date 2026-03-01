
r.set("tickets",5)
current = r.decr("tickets")

if current < 0 :
    r.incr("tickets")
    print("too slow to get the ticket, Good luck next time!")

queue_push(user_id)


while True:
    if tasks:
        background_worker()
    else:
        sleep(0.1)

def background_worker():
    task = queue.pop()
    try:
        db.insert(task.user_id)
    except Exception:
        r.incr("tickets")



        check task_queue()
if task_queue>0:
    db.insert("INSERT INTO db_records")
else:
    incr("redis_stock")