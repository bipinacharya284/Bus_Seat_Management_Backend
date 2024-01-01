from fastapi import FastAPI, HTTPException
# from insert_data import create_table, insert_item, get_all_items, get_item, update_item, delete_item

# from db_operation.get_data import get_payment_log_cid

app = FastAPI()

# Create the table if not exists
create_table()

@app.post("/items/")
async def create_item(name: str, description: str):
    insert_item(name, description)
    return {"message": "Item created successfully"}

@app.get("/items/", response_model=list)
async def read_items():
    return get_all_items()

@app.get("/items/{item_id}", response_model=dict)
async def read_item(item_id: int):
    item = get_item(item_id)
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}")
async def update_item(item_id: int, name: str, description: str):
    existing_item = get_item(item_id)
    if existing_item:
        update_item(item_id, name, description)
        return {"message": "Item updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
async def delete_item_route(item_id: int):
    existing_item = get_item(item_id)
    if existing_item:
        delete_item(item_id)
        return {"message": "Item deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")
