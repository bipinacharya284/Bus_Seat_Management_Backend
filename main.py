import json
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from db_operation.insert_data import insert_into_client,insert_transaction_log,exit_travel_log,entry_travel_log
from db_operation.get_data import get_all_clients,get_client,get_payment_log_by_pid,get_payment_log_by_cid,get_travel_log_by_cid,get_travel_log_by_tid,get_travel_log
from db_operation.update_data import update_client
# from db_operation.get_data import get_payment_log_cid

app = FastAPI()

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