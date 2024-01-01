import sqlite3

# Importing database file
DB_FILE = "./db_operation/database.db"

# For creating client table
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

# Create travel_log table
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


# Create payment_log table
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