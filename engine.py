import store

def handle_request(user_id):

    if store.r.sadd("purchased_users", user_id) == 0:
        print(f"refuse {user_id}: repeat looting")
        return
    
    current = store.r.decr("tickets")

    if current < 0:
        store.r.incr("tickets")
        print(f"user {user_id}: Empty tickets")

    else:
        store.r.rpush("task_queue",user_id)
        print(f"user{user_id}: purchased successful, queuing...")
TO














    if user_id in store.purchased_users:
        print(f"refuse {user_id}")
        return
    
    store.redis_stock -= 1 
    current = store.redis_stock
    
    if current < 0:
        store.redis_stock += 1
        print(f"{user} there is no ticket.")
    else:
        store.purchased_users.add(user_id)
        store.task_queue.append(user_id)
        print(f"user {user_id}: succcess!")


