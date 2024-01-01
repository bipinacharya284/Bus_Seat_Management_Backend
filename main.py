import json
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from db_operation.insert_data import insert_into_client,insert_transaction_log,exit_travel_log,entry_travel_log
from db_operation.get_data import get_all_clients,get_client,get_payment_log_by_pid,get_payment_log_cid,get_travel_log_by_cid,get_travel_log_by_tid
# from db_operation.get_data import get_payment_log_cid

app = FastAPI()

@app.post("/client/")
async def create_client(name: str, phone: str, rfid_id: str, amount:int):
    if insert_into_client(name, phone, rfid_id, amount):
        return {"status": "Data inserted successfully", "code": 200}
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/clients/")
async def read_clients():
    json_string = get_all_clients()
    json_data = json.loads(json_string)
    return json_data


@app.get("/client/{client_id}")
async def read_client(client_id: int):
    json_string = get_client(client_id)
    json_data = json.loads(json_string)
    return json_data
     
# @app.get("/items/{item_id}", response_model=dict)
# async def read_item(item_id: int):
#     item = get_item(item_id)
#     if item:
#         return item
#     else:
#         raise HTTPException(status_code=404, detail="Item not found")

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, name: str, description: str):
#     existing_item = get_item(item_id)
#     if existing_item:
#         update_item(item_id, name, description)
#         return {"message": "Item updated successfully"}
#     else:
#         raise HTTPException(status_code=404, detail="Item not found")

# @app.delete("/items/{item_id}")
# async def delete_item_route(item_id: int):
#     existing_item = get_item(item_id)
#     if existing_item:
#         delete_item(item_id)
#         return {"message": "Item deleted successfully"}
#     else:
#         raise HTTPException(status_code=404, detail="Item not found")
