import asyncio
import json
import numpy as np
from fastapi import FastAPI, WebSocket, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from routes.routes import router
from repository.pool import PoolRepository
from services.ml import interpreter
from schemas.notification import Notification
from utils.notification import send_notification

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


async def get_dummy_data(data):
    return json.dumps(data)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, pool_repo: PoolRepository = Depends(PoolRepository)):
    await websocket.accept()
    pool_id = await websocket.receive_text()
    pool_data = await pool_repo.get_pool_by_id(pool_id)

    if pool_data is None:
        await websocket.send_text("Pool data not found")
        await websocket.close()
        return

    sensor_data = pool_data["sensor"]

    while True:
        result = await get_dummy_data(sensor_data)
        await websocket.send_text(f"Results: {result}")
        await asyncio.sleep(10)
