from datetime import datetime
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
# print(result

def get_all_seats():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM seat")
    results = cursor.fetchall()
    data_list = [dict(zip(['sid','seatname', 'seattype', 'isfree'], row)) for row in results ]
    results_json = json.dumps(data_list, indent=2)
    conn.close()
    return results_json

# result = get_all_seats()
# print(result)

def get_all_free_seats():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM seat WHERE is_occupied = 0")
    results = cursor.fetchall()
    data_list = [dict(zip(['sid','seatname', 'seattype', 'isfree'], row)) for row in results ]
    results_json = json.dumps(data_list, indent=2)
    conn.close()
    return results_json

def get_one_free_seat():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM seat WHERE is_occupied = 0")
        try:
            result = cursor.fetchone()
            data_list = [dict(zip(['sid','seatname', 'seattype', 'is_occupied'], result)) ]
            results_json = json.dumps(data_list, indent=2)
        
            conn.close()
            return results_json
        except TypeError as e:
            print("No Seat Available")
    except sqlite3.Error as e:
        print("Error  ",e)
    finally:
        conn.close()
# print(get_one_free_seat())

# result = get_one_free_seat()
# print(result)

def get_seat_by_sid(sid: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM seat WHERE sid = ?", str(sid))
    result = cursor.fetchone()
    data_list = [dict(zip(['sid','seatname', 'seattype', 'isfree'], result)) ]
    results_json = json.dumps(data_list, indent=2)
    conn.close()
    return results_json

# result = get_seat_by_sid(3)
# print(result)

# Gives all the log of travel_data
def get_travel_log():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM travel_log")
    results = cursor.fetchall()
    data_list = [dict(zip(['tid','cid', 'entry_time','fare','sid', 'exit_time'], row)) for row in results ]
    results_json = json.dumps(data_list, indent=2)
    conn.close()
    return results_json


# Gives travel log search by cid
def get_travel_log_by_cid(cid: int):
    """ cid: int """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM travel_log WHERE cid=?", (str(cid)))
    results = cursor.fetchall()
    data_list = [dict(zip(['tid','cid', 'entry_time','fare','sid', 'exit_time'], row)) for row in results ]
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
    cursor.execute("SELECT * FROM travel_log WHERE tid=?", (tid,))
    result = cursor.fetchone()
    data_list = [dict(zip(['tid','cid', 'entry_time','fare','sid', 'exit_time'], result)) ]
    results_json = json.dumps(data_list, indent=2)
    conn.close()
    return results_json

# result = get_travel_log_by_tid(2)  
# print(result)

# Gives payment log search by cid
def get_payment_log_by_cid(cid: int):
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

def is_valid_rfid(rfid_id: str):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM client WHERE rfid_id ='{rfid_id}'")
        result = cursor.fetchone()
        if result:
            return True

        else:
            return False
        
    except sqlite3.Error as e:
        print("Error ",e)
        return False
    finally:
        conn.close()


def get_client_by_rfid(rfid_id: str):
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM client WHERE rfid_id ='{rfid_id}'")
        result = cursor.fetchone()
        data_list = [dict(zip(['cid', 'name', 'phone','rfid_id','amount'], result)) ]
        results_json = json.dumps(data_list, indent=2)
        conn.close()
        return results_json
    except sqlite3.Error as e:
        print("Error ",e)
        return False
    finally:
        conn.close()



def get_travel_time_difference(tid: int):
    travel_datas = json.loads(get_travel_log_by_tid(tid))
    travel_data = travel_datas[0]
    entry_time = travel_data["entry_time"]
    exit_time = travel_data["exit_time"]
    
    entry_time = datetime.strptime(entry_time, "%Y-%m-%d %H:%M:%S")
    exit_time = datetime.strptime(exit_time, "%Y-%m-%d %H:%M:%S")
    
    # print(entry_time)
    # print(exit_time)

    difference = exit_time - entry_time
    # difference =  int(difference.total_seconds())

    total_seconds = difference.total_seconds()
    hours, remainder = divmod(int(total_seconds), 3600)
    minutes, seconds = divmod(remainder, 60)

    return (seconds + 60*minutes)
    
