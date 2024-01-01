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

def insert_seat(seatname: str, seattype: str):
   try:
      conn = sqlite3.connect(DB_FILE)
      cursor = conn.cursor()
      cursor.execute("INSERT INTO seat (seatname, seattype) VALUES (?, ?)", (seatname,seattype))
      conn.commit()
      conn.close()
      return True
   except sqlite3.Error as e:
      print(f"Error: {e}")
      conn.rollback()  # Rollback the changes if an error occurs
      return False
   finally:
      conn.close()

# insert_seat("A1","Women")

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
         return True
      else:
         print("No Row Inserted")
   except sqlite3.Error as e:
      print(f"Error: {e}")
      conn.rollback()  # Rollback the changes if an error occurs
      return False
   finally:
      conn.close()

# insert_transaction_log(1,"credit",500)


# def delete_item(item_id: int):
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
#     conn.commit()
#     conn.close()
