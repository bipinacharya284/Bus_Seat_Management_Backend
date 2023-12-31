import sqlite3
from typing import List, Optional


DB_FILE = "database.db"



def create_table_client():
   try:
      conn = sqlite3.connect(DB_FILE)
      cursor = conn.cursor()
      cursor.execute("""
         CREATE TABLE client (
               cid INTEGER PRIMARY KEY AUTOINCREMENT,
               name VARCHAR(40) NOT NULL,
               phone VARCHAR(10) NOT NULL,
               rfid_id VARCHAR(50) NOT NULL UNIQUE,
               amount INTEGER NOT NULL,
               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP      
         )
      """)
      conn.commit()
      conn.close()
   except sqlite3.Error as e:
      print(f"Error: {e}")
      conn.rollback()  # Rollback the changes if an error occurs
   finally:
      conn.close()

def create_table_travel_log():
   try:
      conn = sqlite3.connect(DB_FILE)
      cursor = conn.cursor()
      cursor.execute("""
         CREATE TABLE travel_log (
               tid INTEGER PRIMARY KEY AUTOINCREMENT,
               cid INTEGER ,
               entry_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               exit_time TIMESTAMP,
               FOREIGN KEY (cid) REFERENCES client (cid)
         )
      """)
      conn.commit()
      conn.close()
   except sqlite3.Error as e:
      print(f"Error: {e}")
      conn.rollback()  # Rollback the changes if an error occurs
   finally:
      conn.close()


def create_table_payment_log():
   try:
      conn = sqlite3.connect(DB_FILE)
      cursor = conn.cursor()
      cursor.execute("""
         CREATE TABLE payment_log (
               pid INTEGER PRIMARY KEY AUTOINCREMENT,
               cid INTEGER NOT NULL,
               trans_type VARCHAR(10),
               trans_amt INTEGER,
               trans_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               FOREIGN KEY (cid) REFERENCES client (cid)
         )
      """)
      conn.commit()
      conn.close()
   except sqlite3.Error as e:
      print(f"Error: {e}")
      conn.rollback()  # Rollback the changes if an error occurs
   finally:
      conn.close()


# create_table_client()
# create_table_travel_log()
# create_table_payment_log()

def insert_into_client(name: str, phone: str, rfid_id: str, amount : int):
   try:
      conn = sqlite3.connect(DB_FILE)
      cursor = conn.cursor()
      cursor.execute("INSERT INTO client (name, phone, rfid_id,amount) VALUES (?, ?,?,?)", (name, phone,rfid_id,amount))
      conn.commit()
      conn.close()
   except sqlite3.Error as e:
      print(f"Error: {e}")
      conn.rollback()  # Rollback the changes if an error occurs
   finally:
      conn.close()

# insert_into_client('Hari','9444545','66:44:7A',500)

# IF NOT EXISTS (SELECT 1 FROM items WHERE name = 'your_name_to_check') THEN
    
#     INSERT INTO items (name, description) VALUES ('your_name_to_check', 'your_description');
# END IF;

def entry_travel_log(cid: int):
   try:
      conn = sqlite3.connect(DB_FILE)
      cursor = conn.cursor()
      cursor.execute("PRAGMA foreign_keys = ON")
      # Check if a record with cid and exit_time=NULL already exists
      cursor.execute("SELECT cid FROM travel_log WHERE cid = ? AND exit_time IS NULL", (cid,))
      existing_record = cursor.fetchone()

      if not existing_record:
         # Insert a new record only if no matching record exists
         cursor.execute("INSERT INTO travel_log (cid) VALUES (?)", (cid,))
      else:
         print("Already on entry")
      conn.commit()
      conn.close()
   except sqlite3.Error as e:
      print(f"Error: {e}")
      conn.rollback()  # Rollback the changes if an error occurs
   finally:
      conn.close()


# entry_travel_log(1)
# entry_travel_log(2)

def exit_travel_log(cid:int):
   try:
      conn = sqlite3.connect(DB_FILE)
      cursor = conn.cursor()
      cursor.execute("SELECT cid FROM travel_log WHERE cid = ? AND exit_time IS NULL", (cid,))
      existing_record = cursor.fetchone()
      if existing_record:
         cursor.execute("UPDATE travel_log SET exit_time = CURRENT_TIMESTAMP WHERE cid=?", (str(cid)))
         conn.commit()
         conn.close()
      else:
         print("No Record to exit")
   except sqlite3.Error as e:
      print(f"Error: {e}")
      conn.rollback()  # Rollback the changes if an error occurs
   finally:
      conn.close()

# exit_travel_log(2)


# def get_all_items() -> List[tuple]:
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM items")
#     results = cursor.fetchall()
#     conn.close()
#     return results

# def get_item(item_id: int) -> Optional[tuple]:
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM items WHERE id=?", (item_id,))
#     result = cursor.fetchone()
#     conn.close()
#     return result

# def update_item(item_id: int, name: str, description: str):
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("UPDATE items SET name=?, description=? WHERE id=?", (name, description, item_id))
#     conn.commit()
#     conn.close()

# def delete_item(item_id: int):
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
#     conn.commit()
#     conn.close()
