# Inserting data for recording the entry of client
import json
import sqlite3
import db_operation.get_data as gd

# import get_data as gd
from db_operation.insert_data import insert_transaction_log
# from db_operation.get_data import get_one_free_seat,get_travel_time_difference, get_seat_by_sid,get_travel_log_by_cid
from db_operation.update_data import toggle_seat_status

DB_FILE = "./db_operation/database.db"


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
            seats_data = json.loads(gd.get_one_free_seat())
            seat_data = seats_data[0]
            seat_id = seat_data["sid"]
            # seat_name = seat_data["seatname"]
            # print(seat_id)
            
            cursor.execute("INSERT INTO travel_log (cid,sid) VALUES (?,?)", (str(cid),str(seat_id)))
            conn.commit()
            toggle_seat_status(seat_id)
            
            conn.commit()
            return seat_data
            # print("Reserved new seat")
            # print(get_seat_by_sid(seat_id))
         except TypeError as e:
            print("Seat not available: ",e )
            return "No seat Available"

      else:
            print("Record already Entered")

      conn.commit()
      conn.close()
      # return False
   
   except sqlite3.Error as e:
      print(f"Error: {e}")
      conn.rollback()  # Rollback the changes if an error occurs
      # return False
      return f"Error: {e}"
   finally:
      conn.close()
      # return f"Finally"

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

         travel_logs = json.loads(gd.get_travel_log_by_cid(cid))
         travel_log = travel_logs[0]
         travel_id = travel_log["tid"]
         seat_id = travel_log["sid"]
         # print(seat_id)
         # print(travel_id)

         # travel_time_difference = 10
         # try:
         travel_time_difference = gd.get_travel_time_difference(travel_id)
         print("Time in seconds ",travel_time_difference)
         fare = travel_time_difference * 2
         fare = int(fare)
         # print("Fare in" ,fare)

         # cursor.execute(f"UPDATE travel_log SET fare = {fare} WHERE tid = ? ", (travel_id,))
      
         insert_transaction_log(cid,"DEBIT",fare)
         conn.commit()

            # print(seat_id)
         # except sqlite3.Error as e:
         #    print("2 Error ",e)
         
         try:
            if toggle_seat_status(seat_id):
               conn.commit()
               print("Released seat", gd.get_seat_by_sid(seat_id))
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

