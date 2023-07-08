from locust import HttpUser, task, between
from schemas.user import UserLogin
import json


class PerformanceTests(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def test_login(self):
        login = UserLogin(email="pengujian@email.com",
                          password="pass", device_id="22")
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}
        res = self.client.post(
            '/user/login', data=json.dumps(login.dict()), headers=headers)
        # print("res", res.json())
