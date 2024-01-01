import sqlite3

DB_FILE = "./db_operation/database.db"


def update_client(cid: int, name: str, phone: str, rfid_id:str):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("UPDATE client SET name=?, phone=?, rfid_id=? WHERE cid=?", (name, phone, rfid_id, str(cid) ))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("Error ",e)
    finally:
        conn.close()

# update_client(1,"Bipin","11111","9845665")