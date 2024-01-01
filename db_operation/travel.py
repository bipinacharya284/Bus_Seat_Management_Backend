# Inserting data for recording the entry of client
import sqlite3

DB_FILE = "./db_operation/database.db"

def entry_exit_log(cid: int):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        # Check if a record with cid and exit_time=NULL already exists
        cursor.execute("SELECT * FROM travel_log WHERE cid = ? AND exit_time IS NULL", (cid,))
        existing_record = cursor.fetchone()

        if not existing_record:
            # Insert a new record only if no matching record exists
            cursor.execute("INSERT INTO travel_log (cid) VALUES (?)", (cid,))
        else:
            print("Already on entry")
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error: {e}")
        conn.rollback()  # Rollback the changes if an error occurs
        return False
    finally:
        conn.close()

    


def entry_travel_log(cid: int): 
   try:
      conn = sqlite3.connect(DB_FILE)
      cursor = conn.cursor()
      cursor.execute("PRAGMA foreign_keys = ON")
      # Check if a record with cid and exit_time=NULL already exists
      cursor.execute("SELECT * FROM travel_log WHERE cid = ? AND exit_time IS NULL", (cid,))
      existing_record = cursor.fetchone()
      
      if not existing_record:
                # Insert a new record only if no matching record exists
          cursor.execute("""
                INSERT INTO travel_log (cid,)

            """)
            # cursor.execute("INSERT INTO travel_log (cid) VALUES (?)", (cid,))
      else:
            cursor.execute("UPDATE travel_log SET exit_time = CURRENT_TIMESTAMP WHERE cid=?", (str(cid)))

      conn.commit()
      conn.close()
      return True
   except sqlite3.Error as e:
      print(f"Error: {e}")
      conn.rollback()  # Rollback the changes if an error occurs
      return False
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