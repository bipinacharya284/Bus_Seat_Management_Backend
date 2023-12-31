import json
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from db_operation.insert_data import insert_into_client,insert_transaction_log,insert_into_seat
from db_operation.get_data import get_all_clients,get_client,get_payment_log_by_pid,get_payment_log_by_cid,get_travel_log_by_cid,get_travel_log_by_tid,get_travel_log,get_all_seats
from db_operation.update_data import update_client
# from db_operation.get_data import get_payment_log_cid
from db_operation.travel import entry_travel_log,exit_travel_log
from db_operation.get_data import is_valid_rfid,get_client_by_rfid
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to your actual frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# For Client

@app.post("/client/", tags=["Client"])
async def create_client(name: str, phone: str, rfid_id: str, amount:int):
    if insert_into_client(name, phone, rfid_id, amount):
        return JSONResponse(status_code=200, content="Client Created Successfully")
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/clients/", tags=["Client"])
async def read_clients():
    json_string = get_all_clients()
    json_data = json.loads(json_string)
    return JSONResponse(content=json_data, status_code=200)


@app.get("/client/{client_id}", tags=["Client"])
async def read_client(client_id: int):
    json_string = get_client(client_id)
    json_data = json.loads(json_string)
    return JSONResponse(content=json_data, status_code=200)

@app.put("/client/{client_id}", tags=["Client"])
async def put_client(client_id: int, name: str, phone: str, rfid_id: str):
    existing_client = get_client(client_id)
    if existing_client:
        if update_client(client_id, name, phone, rfid_id):
            return JSONResponse(status_code=200, content="Client Update Successfully")
    else:
        raise HTTPException(status_code=404, detail="Item not found")

# For travel log
    
# @app.post("/travel/", tags=["Travel log"])
# async def create_travel_log(client_id:int):
#     if entry_travel_log(client_id):
#         return JSONResponse(status_code=200, content="Entry Recorded")
#     else:
#         raise HTTPException(status_code=500, detail="Internal Server Error")
    
@app.get("/travellog/", tags=["Travel Log"])
async def read_travel_logs():
    json_string = get_travel_log()
    json_data = json.loads(json_string)
    return JSONResponse(content=json_data, status_code=200)

@app.get("/travellog/{travel_id}", tags=["Travel Log"])
async def read_travel_log_by_tid(travel_id: int):
    json_string = get_travel_log_by_tid(travel_id)
    json_data = json.loads(json_string)
    return JSONResponse(content=json_data, status_code=200)

@app.get("/travellog/client/{client_id}", tags=["Travel Log"])
async def read_travel_log_by_cid(client_id: int):
    json_string = get_travel_log_by_cid(client_id)
    json_data = json.loads(json_string)
    return JSONResponse(content=json_data, status_code=200)

# For payment Log

@app.get("/paymentlog/{payment_id}", tags=["Payment Log"])
async def read_payment_log_by_pid(payment_id: int):
    json_string = get_payment_log_by_pid(payment_id)
    json_data = json.loads(json_string)
    return JSONResponse(content=json_data, status_code=200)

@app.get("/paymentlog/client/{client_id}", tags=["Payment Log"])
async def read_payment_log_by_cid(client_id: int):
    json_string = get_payment_log_by_cid(client_id)
    json_data = json.loads(json_string)
    return JSONResponse(content=json_data, status_code=200)

# For crediting and debiting balance
@app.post("/transaction/", tags=["Transaction"])
async def create_transaction(client_id: int, transaction_type: str, transaction_amount:int):
    if insert_transaction_log(client_id, transaction_type, transaction_amount):
        return JSONResponse(status_code=200, content="Transaction Successful")
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/paymentlog/{pid}", tags=["Transaction"])
async def get_transaction(pid: int):
    json_string = get_payment_log_by_pid(pid)
    return json_string
   

@app.post("/travel/entry", tags=["Travel Log"])
async def create_travel_entry(client_id: int):
    # if entry_travel_log(client_id):
    # return "Response Hit"
    json_string = entry_travel_log(client_id)
    return json_string
   
@app.post("/travel/exit",tags=["Travel Log"])
async def create_travel_exit(client_id:int):
    json_string = exit_travel_log(client_id)
    return json_string

@app.post("/seat",tags=["Seat"])
async def insert_seat(seatname: str, seattype:str):
    json_string = insert_into_seat(seatname, seattype)
    return json_string

@app.get("/valid/{rfid}",tags=["Client"])
async def check_validity(rfid: str):
    if is_valid_rfid(rfid):
        return True
    else:
        return False
    
@app.get("/valid/rfid/{rfid}",tags=["Client"])
async def get_valid_client(rfid: str):
    json_string = get_client_by_rfid(rfid)
    json_data = json.loads(json_string)
    return JSONResponse(content=json_data, status_code=200)


@app.post("/travellog/",tags=["travel"])
async def check_if_client(cid: int):
    entry_return = entry_travel_log(cid)
    if entry_return == "AlreadyExists":
        exit_travel_log(cid)
        return "Seat Released"
    else:
        return entry_return["seatname"]


@app.get("/getallseat/",tags=["Seat"])
async def get_seat():
    # get_all_seats
    json_data = json.loads(get_all_seats())
    return JSONResponse(content=json_data, status_code=200)
    # return get_all_seats

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
