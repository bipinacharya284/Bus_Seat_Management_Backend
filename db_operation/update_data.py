import sqlite3

DB_FILE = "./db_operation/database.db"


def update_client(cid: int, name: str, phone: str, rfid_id:str):
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("UPDATE client SET name=?, phone=?, rfid_id=? WHERE cid=?", (name, phone, rfid_id, str(cid) ))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error ",e)
        return False
    finally:
        conn.close()

# update_client(1,"Bipin","11111","9845665")
    

def update_seat(sid: int, seatname: str, seattype: str):
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("UPDATE seat SET seatname=?, seattype=? WHERE sid=?", (seatname, seattype, str(sid) ))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error ",e)
        return False
    finally:
        conn.close()

# update_seat(4,"B3","ORDINARY")


def toggle_seat_status(sid: int):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute ("""
            UPDATE seat 
            SET is_occupied = 
                CASE 
                    WHEN is_occupied = 0 THEN 1
                    ELSE is_occupied = 0
                END
            WHERE sid = ? """,str(sid))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error ",e)
        return False
    finally:
        conn.close()
        

# toggle_seat_status(1)
