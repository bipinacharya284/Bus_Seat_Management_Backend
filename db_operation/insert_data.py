import sqlite3

# Importing database file
DB_FILE = "./db_operation/database.db"


# Inserting data into client table
def insert_into_client(name: str, phone: str, rfid_id: str, amount : int):
   """ name : str, phone : str, rfid_id : str, amount : int """
   try:
      conn = sqlite3.connect(DB_FILE)
      cursor = conn.cursor()
      cursor.execute("INSERT INTO client (name, phone, rfid_id,amount) VALUES (?, ?,?,?)", (name, phone,rfid_id,amount))
      conn.commit()
      conn.close()
      return True
   except sqlite3.Error as e:
      print(f"Error: {e}")
      conn.rollback()  # Rollback the changes if an error occurs
      return False
   finally:
      conn.close()

# insert_into_client('Kumar','9444545','66:44:7A:55',500)
# insert_into_client('Hari','9444545','66:55:Q6',500)


# Inserting data for recording the entry of client
def entry_travel_log(cid: int): 
   """ cid : int """
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

# Inserting data for recording the exit of client
def exit_travel_log(cid:int):
   """ cid : int """
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

# exit_travel_log(1)

# Inserting the transaction log
def insert_transaction_log(cid:int, trans_type:str, trans_amt:int ):
   """ cid : int, trans_type : str, trans_amt : int """
   try:
      conn = sqlite3.connect(DB_FILE)
      cursor = conn.cursor()
      cursor.execute("PRAGMA foreign_keys = ON")
      cursor.execute("INSERT INTO payment_log(cid, trans_type, trans_amt) VALUES (?, ?,?)", (str(cid), trans_type, str(trans_amt)))
      if cursor.rowcount >0:
         if(trans_type == "credit"):    
            cursor.execute("UPDATE client SET amount = amount + ? WHERE cid=?", (str(trans_amt),str(cid)))
         if(trans_type == "debit"):
            cursor.execute("UPDATE client SET amount = amount - ? WHERE cid=?", (str(trans_amt),str(cid)))
         conn.commit()
         conn.close()
      else:
         print("No Row Inserted")
   except sqlite3.Error as e:
      print(f"Error: {e}")
      conn.rollback()  # Rollback the changes if an error occurs
   finally:
      conn.close()

# insert_transaction_log(1,"credit",500)


# def delete_item(item_id: int):
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
#     conn.commit()
#     conn.close()
