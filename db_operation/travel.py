# Inserting data for recording the entry of client
import json
import sqlite3
from turtle import delay
from insert_data import insert_transaction_log
from get_data import get_one_free_seat,get_travel_time_difference, get_seat_by_sid,get_travel_log_by_cid
from update_data import toggle_seat_status

DB_FILE = "./db_operation/database.db"

# print(seat_id)

# result = get_one_free_seat()
# print(result)

# toggle_seat_status(1)

# def entry_exit_log(cid: int):
#     try:
#         conn = sqlite3.connect(DB_FILE)
#         cursor = conn.cursor()
#         cursor.execute("PRAGMA foreign_keys = ON")
#         # Check if a record with cid and exit_time=NULL already exists
#         cursor.execute("SELECT * FROM travel_log WHERE cid = ? AND exit_time IS NULL", (cid,))
#         existing_record = cursor.fetchone()

#         if not existing_record:
#             # Insert a new record only if no matching record exists
#             seats_data = json.loads(get_one_free_seat())
#             seat_data = seats_data[0]
#             seat_id = seat_data["sid"]
#             cursor.execute("INSERT INTO travel_log (cid,sid) VALUES (?,?)", (str(cid),str(seat_id)))
#             toggle_seat_status(seat_id)
#             print("Reserved new seat", get_seat_by_sid(seat_id))
#         else:
#             cursor.execute("UPDATE travel_log SET exit_time = CURRENT_TIMESTAMP WHERE cid=?", (str(cid)))
            
#             travel_logs = json.loads(get_travel_log_by_cid(cid))
#             travel_log = travel_logs[0]
#             travel_id = travel_log["tid"]
            
#             travel_time_difference = get_travel_time_difference(travel_id)
#             fare = travel_time_difference * 10
#             cursor.execute("UPDATE travel_log SET fare = ? WHERE cid=?", (str(fare),str(cid)))
#             toggle_seat_status(seat_id)
#             print("Released seat", get_seat_by_sid(seat_id))
#         conn.commit()
#         conn.close()
#         return True
#     except sqlite3.Error as e:
#         print(f"Error: {e}")
#         conn.rollback()  # Rollback the changes if an error occurs
#         return False
#     finally:
#         conn.close()

# if entry_exit_log(5):
#     print("Success")
# else:
#     print("Error")


def entry_travel_log(cid: int): 
   try:
      conn = sqlite3.connect(DB_FILE)
      cursor = conn.cursor()
      cursor.execute("PRAGMA foreign_keys = ON")
      # Check if a record with cid and exit_time=NULL already exists
      cursor.execute("SELECT * FROM travel_log WHERE cid = ? AND exit_time IS NULL", (cid,))
      existing_record = cursor.fetchone()
      
      if not existing_record:
         
         try:
            seats_data = json.loads(get_one_free_seat())
            seat_data = seats_data[0]
            seat_id = seat_data["sid"]
            # print(seat_id)
            
            cursor.execute("INSERT INTO travel_log (cid,sid) VALUES (?,?)", (str(cid),str(seat_id)))
            conn.commit()
            toggle_seat_status(seat_id)
            
            conn.commit()
            print("Reserved new seat")
            print(get_seat_by_sid(seat_id))
         except TypeError as e:
            print("Seat not available: ",e )

      else:
            print("Record already Entered")

      conn.commit()
      conn.close()
      return True
   except sqlite3.Error as e:
      print(f"Error: {e}")
      conn.rollback()  # Rollback the changes if an error occurs
      return False
   finally:
      conn.close()


entry_travel_log(5)
# entry_travel_log(2)

# Inserting data for recording the exit of client
def exit_travel_log(cid:int):

   try:
      conn = sqlite3.connect(DB_FILE)
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM travel_log WHERE cid = ? AND exit_time IS NULL", str(cid))
      existing_record = cursor.fetchone()
      # print(existing_record)
      if existing_record:
         conn.commit()

         # cursor.execute("UPDATE travel_log SET exit_time = CURRENT_TIMESTAMP WHERE cid=? AND exit_time = NULL", str(cid))
         cursor.execute("UPDATE travel_log SET exit_time = CURRENT_TIMESTAMP WHERE cid=? AND exit_time IS NULL", (cid,))

         conn.commit()

         travel_logs = json.loads(get_travel_log_by_cid(cid))
         travel_log = travel_logs[0]
         travel_id = travel_log["tid"]
         seat_id = travel_log["sid"]
         # print(seat_id)
         # print(travel_id)

         # travel_time_difference = 10
         try:
            travel_time_difference = get_travel_time_difference(travel_id)
            print("Time in seconds ",travel_time_difference)
            fare = travel_time_difference * 2
            print("Fare in" ,fare)

            cursor.execute("UPDATE travel_log SET fare = ? WHERE tid = ? ", (fare, travel_id))
         
            conn.commit()
            insert_transaction_log(cid,"DEBIT",fare)

            # print(seat_id)
         except sqlite3.Error as e:
            print("2 Error ",e)
         
         try:
            if toggle_seat_status(seat_id):
               conn.commit()
               print("Released seat", get_seat_by_sid(seat_id))
            else:
               print("seat not toggled")
         except sqlite3.Error as e:
            print("3 Error ",e)
      else:
         print("No Record to exit")
   except sqlite3.Error as e:
      print(f"Error: {e}")
      conn.rollback()  # Rollback the changes if an error occurs
   finally:
      conn.close()

exit_travel_log(5)