from fastapi import APIRouter, Depends, Request, Response
import json
import numpy as np

from repository.user import UserRepository
from repository.history import HistoryRepository
from services.ml import interpreter
from schemas.notification import Notification
from services.notification import send_notification
from services.recommendation import get_recommendation


antares = APIRouter(prefix='/antares', tags=['Antares'])


@antares.post('/{user_email}')
async def receive_sensor_data(user_email: str, request: Request, user_repo: UserRepository = Depends(UserRepository), history_repo: HistoryRepository = Depends(HistoryRepository)):
    # Decode request body
    # TODO: Integrate antares body request
    body = await request.body()

    if not body:
        print('No request body found')
        return Response(status_code=200)

    # Check for body params
    json_body = json.loads(body.decode('utf-8'))
    if (not json_body['ph']) or (not json_body['temp']):
        print('No required fields found')
        return Response(status_code=200)

    latest_ph = float(json_body['ph'])
    latest_temp = float(json_body['temp'])

    user = await user_repo.get_user(user_email)

    # User found
    if user and user['device_id']:
        ### Immediate ###
        recommendation = get_recommendation(latest_ph, latest_temp)

        if recommendation['ph']:
            response_notif = send_notification(user['device_id'], Notification(
                title='Anomali kolam: pH', body=recommendation['ph']))

            if (response_notif.status_code != 200):
                print('Failed to send notification')
                print(response_notif.json())

        if recommendation['temp']:
            response_notif = send_notification(user['device_id'], Notification(
                title='Anomali kolam: temperatur', body=recommendation['temp']))

            if (response_notif.status_code != 200):
                print('Failed to send notification')
                print(response_notif.json())

        ### Predictive ###
        # Get input and output details
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        # Prepare input data
        # Get 15 latest data
        history_data = await history_repo.get_15_latest_data("64900a4ad1fbe076bfb6e9c9")

        temperatures = [entry['temperature'] for entry in history_data]
        ph_values = [entry['ph'] for entry in history_data]

        # Create a NumPy 2-dimensional array
        input_data = np.column_stack((temperatures, ph_values))
        input_data = input_data.astype(np.float32)
        print(input_data)

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

        # Get recommendation based on prediction
        temp_pred = output_data[0][0]
        ph_pred = output_data[0][1]
        recommendation_pred = get_recommendation(ph_pred, temp_pred)

        # Send notif prediction ONLY IF there's no immediate recommendation
        if (not recommendation['ph'] and recommendation_pred['ph']):
            response_notif = send_notification(user['device_id'], Notification(
                title='Prediksi anomali kolam: pH', body=recommendation_pred['ph'] + ' dalam 15 menit'))

            if (response_notif.status_code != 200):
                print('Failed to send notification')
                print(response_notif.json())

        if (not recommendation['temp'] and recommendation_pred['temp']):
            response_notif = send_notification(user['device_id'], Notification(
                title='Prediksi anomali kolam: temperatur', body=recommendation_pred['temp'] + ' dalam 15 menit'))

            if (response_notif.status_code != 200):
                print('Failed to send notification')
                print(response_notif.json())

    # User not found
    else:
        print('Failed to find user with email/device id')

    return Response(status_code=200)
