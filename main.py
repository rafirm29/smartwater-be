import asyncio
import json
from fastapi import FastAPI, WebSocket, Depends
from fastapi.middleware.cors import CORSMiddleware

from routes.routes import router
from repository.pool import PoolRepository
from repository.history import HistoryRepository

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(router)


@app.get('/')
async def home(history_repo: HistoryRepository = Depends(HistoryRepository)):
    latest_data = await history_repo.get_latest_data("6496a55d73845826da0f1069")
    new_dict = {key: value for key, value in latest_data.items() if key in [
        'temperature', 'ph']}
    json_string = json.dumps(new_dict)
    print(json_string)
    return {"data": "hello"}


async def send_data_periodically(websocket: WebSocket, pool_id):
    try:
        while True:
            await websocket.send_text("This is data sent every 10 secs")
            await asyncio.sleep(10)  # Sleep for 10 secs
    except asyncio.CancelledError:
        pass


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, pool_repo: PoolRepository = Depends(PoolRepository), history_repo: HistoryRepository = Depends(HistoryRepository)):
    await websocket.accept()
    client_id = id(websocket)
    print(
        f"Client connected. Client ID: {client_id}. Waiting to receive pool_id...")
    pool_id = await websocket.receive_text()
    pool_data = await pool_repo.get_pool_by_id(pool_id)

    if pool_data is None:
        await websocket.send_text("Pool data not found")
        await websocket.close()
        return

    try:
        while True:
            latest_data = await history_repo.get_latest_data(pool_id)
            data_dict = {key: value for key, value in latest_data.items() if key in [
                'temperature', 'ph']}
            data_stringified = json.dumps(data_dict)
            await websocket.send_text(data_stringified)
            await asyncio.sleep(900)  # Interval 15 minutes
    except Exception as e:
        print(f"Client ID {client_id} disconnected. Reason: {str(e)}")
