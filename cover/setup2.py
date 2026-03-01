import threading
import time

# --- 1. 实验室器材 ---
redis_stock = 5   # 模拟库存
task_queue = []   # 模拟异步队列
db_records = []   # 模拟数据库账本

# --- 2. 抢票函数：这里定义了 user_id 怎么来 ---
def handle_request(who_is_coming):
    global redis_stock
    
    # 逻辑：先斩后奏
    redis_stock -= 1
    current = redis_stock
    
    if current < 0:
        redis_stock += 1 # 补偿
        print(f"【{who_is_coming}】 抱歉，票卖完了。")
    else:
        # 这里就是你刚才报错的地方！
        # 现在 who_is_coming 这个名字被正确传入并塞进队列了
        task_queue.append(who_is_coming)
        print(f"【{who_is_coming}】 抢到了！系统正在为你占座...")

# --- 3. 后台工人：负责慢慢写账本 ---
def background_worker():
    while True:
        if task_queue:
            # 从队列头部取出一个名字
            name = task_queue.pop(0)
            time.sleep(1) # 模拟写数据库很慢
            db_records.append(name)
            print(f"   [后台消息] 成功为 {name} 生成电子票。当前总销量：{len(db_records)}")
        else:
            time.sleep(0.1)

# --- 4. 实验开始 ---
# 启动后台工人
threading.Thread(target=background_worker, daemon=True).start()

print("--- 抢票大作战开始 ---")
# 模拟 10 个人涌入，循环变量 i 会变成 handle_request 的参数
for i in range(1, 11):
    handle_request(f"用户_编号_{i}")

# 让主程序停 7 秒，看后台工人表演
time.sleep(7)
print(f"--- 最终名单：{db_records} ---")