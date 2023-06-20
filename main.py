import asyncio
import json
import random
import numpy as np
from fastapi import FastAPI, WebSocket, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from routes.routes import router
from repository.pool import PoolRepository
from services.ml import interpreter

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


# Endpoint for Antares subscription
@app.post('/')
async def antares(request: Request):
    # Print request body
    body = await request.body()
    print(body)

    # TODO: Integrate antares body request to ML Model
    # Get input and output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Prepare input data
    # TODO: Change to not use dummy data
    input_data = np.random.uniform(0, 10, size=(35, 2)).astype(
        np.float32)  # Example input array of shape (35, 2)

    # Set input tensor
    interpreter.set_tensor(
        input_details[0]['index'], input_data.reshape(input_details[0]['shape']))

    # Run inference
    interpreter.invoke()

    # Get the output tensor
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # Perform post-processing on the output data if required
    # ...

    # Print the prediction or use it for further processing
    print("Prediction:", output_data)

    return Response(status_code=200)


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
