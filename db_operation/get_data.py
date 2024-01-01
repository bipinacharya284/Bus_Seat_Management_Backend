import sqlite3
from typing import List, Optional
import json

# Importing database file
DB_FILE = "./db_operation/database.db"


# Gives inforamtion of all clients
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

# Gives data of only one client
def get_client(cid: int):
    """ cid: int """
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

# Gives travel log search by cid
def get_travel_log_by_cid(cid: int):
    """ cid: int """
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

# Gives travel log search by tid
def get_travel_log_by_tid(tid: int):
    """ tid : int """
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

# Gives payment log search by cid
def get_payment_log_cid(cid: int):
    """ cid: int """
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


# Gives payment log search by pid
def get_payment_log_by_pid(pid: int):
    """pid: int"""
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