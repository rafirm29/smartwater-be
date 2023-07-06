import asyncio
import json
from fastapi import FastAPI, WebSocket, Depends
from fastapi.middleware.cors import CORSMiddleware

from routes.routes import router
from repository.pool import PoolRepository

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
def home():
    return {"data": "hello"}


async def send_data_periodically(websocket: WebSocket, pool_id):
    try:
        while True:
            await websocket.send_text("This is data sent every 10 secs")
            await asyncio.sleep(10)  # Sleep for 10 secs
    except asyncio.CancelledError:
        pass


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, pool_repo: PoolRepository = Depends(PoolRepository)):
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
        # Start the periodic sending coroutine
        print(f"Pool id received. Sending periodic data...")
        send_task = asyncio.create_task(
            send_data_periodically(websocket, pool_id))

        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"You said: {data}")
    except Exception as e:
        print(f"Client ID {client_id} disconnected. Reason: {str(e)}")
    finally:
        # Cancel the periodic sending coroutine when the client disconnects
        send_task.cancel()
