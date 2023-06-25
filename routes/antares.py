from fastapi import APIRouter, Depends, Request, Response
from typing import List
import json
import numpy as np

from repository.user import UserRepository
from services.ml import interpreter
from schemas.notification import Notification
from utils.notification import send_notification


antares = APIRouter(prefix='/antares', tags=['Antares'])


@antares.post('/{user_email}')
async def receive_sensor_data(user_email: str, request: Request, user_repo: UserRepository = Depends(UserRepository)):
    # Print request body
    body = await request.body()
    if body:
        json_body = json.loads(body.decode('utf-8'))
        print(json_body)

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

    ## Get user ##
    user = await user_repo.get_user(user_email)
    if user and user['device_id']:
        response_notif = send_notification(user['device_id'], Notification(
            title='Test', body='This is a notif test'))

        if (response_notif.status_code == 200):
            print(response_notif.json())
        else:
            print('Failed to send notification')
    else:
        print('Failed to find user with email/device id')

    return Response(status_code=200)
