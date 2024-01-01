import sqlite3
from typing import List, Optional
import json


DB_FILE = "./db_operation/database.db"



def get_all_clients():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM client")
    results = cursor.fetchall()
    data_list = [dict(zip(['cid', 'name', 'phone','rfid_id','amount'], row)) for row in results]
    results_json = json.dumps(data_list, indent=2)
    conn.close()
    return results_json

# results = get_all_clients()
# print(results)

def get_client(cid: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM client WHERE cid=?", (str(cid)))
    result = cursor.fetchone()
    data_list = [dict(zip(['cid', 'name', 'phone','rfid_id','amount'], result)) ]
    results_json = json.dumps(data_list, indent=2)
    conn.close()
    return results_json

# result = get_client(1)  
# print(result)


def get_travel_log_by_cid(cid: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM travel_log WHERE cid=?", (str(cid)))
    results = cursor.fetchall()
    data_list = [dict(zip(['tid','cid', 'entry_time', 'exit_time'], row)) for row in results ]
    results_json = json.dumps(data_list, indent=2)
    conn.close()
    return results_json

# result = get_travel_log_by_cid(1)  
# print(result)


def get_travel_log_by_tid(tid: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM travel_log WHERE tid=?", (str(tid)))
    result = cursor.fetchone()
    data_list = [dict(zip(['tid','cid', 'entry_time', 'exit_time'], result)) ]
    results_json = json.dumps(data_list, indent=2)
    conn.close()
    return results_json

# result = get_travel_log_by_tid(2)  
# print(result)


def get_payment_log_cid(cid: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM payment_log WHERE cid=?", (str(cid)))
    results = cursor.fetchall()
    data_list = [dict(zip(['pid','cid', 'trans_type', 'trans_amt','trans_time'], row)) for row in results ]
    results_json = json.dumps(data_list, indent=2)
    conn.close()
    return results_json

# result = get_payment_log_cid(1)  
# print(result)

def get_payment_log_by_pid(pid: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM payment_log WHERE pid=?", (str(pid)))
    result = cursor.fetchone()
    data_list = [dict(zip(['pid','cid', 'trans_type', 'trans_amt','trans_time'], result)) ]
    results_json = json.dumps(data_list, indent=2)
    conn.close()
    return results_json

# result = get_payment_log_by_pid(1)  
# print(result)