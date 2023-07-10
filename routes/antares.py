from fastapi import APIRouter, Depends, Request, Response
import json
import numpy as np

from repository.user import UserRepository
from repository.pool import PoolRepository
from repository.history import HistoryRepository
from services.ml import interpreter
from models.history import DataPoint
from schemas.notification import Notification
from services.notification import send_notification
from services.recommendation import get_recommendation


antares = APIRouter(prefix='/antares', tags=['Antares'])

pool_id_global = "6496a55d73845826da0f1069"


@antares.post('/{user_email}')
async def receive_sensor_data(user_email: str, request: Request, user_repo: UserRepository = Depends(UserRepository), pool_repo: PoolRepository = Depends(PoolRepository), history_repo: HistoryRepository = Depends(HistoryRepository)):
    # Decode request body
    body = await request.body()

    if not body:
        print('No request body found')
        return Response(status_code=200)

    # Check for body params
    json_body = json.loads(body.decode('utf-8'))
    print("-- JSON Body --")
    print(json_body)
    # if not ('ph' in json_body and 'temp' in json_body):
    #     print('No required fields found')
    #     return Response(status_code=200)
    latest_ph = None
    latest_temp = None

    if not ('m2m:sgn' in json_body and 'm2m:nev' in json_body['m2m:sgn'] and 'm2m:rep' in json_body['m2m:sgn']['m2m:nev'] and 'm2m:cin' in json_body['m2m:sgn']['m2m:nev']['m2m:rep'] and 'con' in json_body['m2m:sgn']['m2m:nev']['m2m:rep']['m2m:cin']):
        # One or more required keys are missing
        print("One or more required keys are missing to access the 'data' key.")
        return Response(status_code=200)

    raw_data = json_body['m2m:sgn']['m2m:nev']['m2m:rep']['m2m:cin']['con']['data']

    data_list = raw_data.split(",")

    data_dict = {
        "temperature": float(data_list[0]),
        "do": float(data_list[1]),
        "turbidity": float(data_list[2]),
        "ph": float(data_list[3]),
        "temperature_air": float(data_list[4]),
        "humidity": float(data_list[5]),
        "volt_battery": float(data_list[6]),
        "volt_solar": float(data_list[7]),
        "tds": float(data_list[8])
    }

    latest_ph = float(data_dict['ph'])
    latest_temp = float(data_dict['temperature'])

    user = await user_repo.get_user(user_email)

    # User found
    if user and user['device_id']:
        ### Immediate ###
        recommendation = get_recommendation(latest_ph, latest_temp)

        if recommendation['ph']:
            response_notif = send_notification(user['device_id'], Notification(
                title='Anomali kolam: pH', body=recommendation['ph']))

            await pool_repo.add_anomaly(pool_id_global, 'ph', recommendation['ph'], 'danger')

            if (response_notif.status_code != 200):
                print('Failed to send notification')
                print(response_notif.json())

        if recommendation['temp']:
            response_notif = send_notification(user['device_id'], Notification(
                title='Anomali kolam: temperatur', body=recommendation['temp']))

            await pool_repo.add_anomaly(pool_id_global, 'temperature', recommendation['temp'], 'danger')

            if (response_notif.status_code != 200):
                print('Failed to send notification')
                print(response_notif.json())

        ### Predictive ###
        # Get input and output details
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        # Prepare input data
        # Insert latest sensor dara
        new_record = DataPoint(**data_dict)

        await history_repo.add_record(pool_id_global, new_record)
        # Get 15 latest data
        history_data = await history_repo.get_70_latest_data(pool_id_global)

        temperatures = [entry['temperature'] for entry in history_data]
        ph_values = [entry['ph'] for entry in history_data]

        # Create a NumPy 2-dimensional array
        input_data = np.column_stack((temperatures, ph_values))
        input_data = input_data.astype(np.float32)

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

            await pool_repo.add_anomaly(pool_id_global, 'ph', recommendation_pred['ph'] + ' dalam 15 menit', 'warning')

            if (response_notif.status_code != 200):
                print('Failed to send notification')
                print(response_notif.json())

        if (not recommendation['temp'] and recommendation_pred['temp']):
            response_notif = send_notification(user['device_id'], Notification(
                title='Prediksi anomali kolam: temperatur', body=recommendation_pred['temp'] + ' dalam 15 menit'))

            await pool_repo.add_anomaly(pool_id_global, 'temperature', recommendation_pred['temp'] + ' dalam 15 menit', 'warning')

            if (response_notif.status_code != 200):
                print('Failed to send notification')
                print(response_notif.json())

    # User not found
    else:
        print('Failed to find user with email/device id')

    return Response(status_code=200)
