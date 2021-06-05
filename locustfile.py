import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(0.5, 2.5)
    token = '90cca45e7d7cc3f2ae98832d77ab6bc1978bbf12'
    @task
    def hello_world(self):
        self.client.get("/api/users/", headers={'Authorization': 'token 90cca45e7d7cc3f2ae98832d77ab6bc1978bbf12'}, verify=False)
        # self.client.get("/world")

    # @task(3)
    # def view_items(self):
    #     for item_id in range(10):
    #         self.client.get(f"/item?id={item_id}", name="/item")
    #         time.sleep(1)

    def on_start(self):
        p=self.client.post("/api/auth/", data={'username':'manager', 'password':'ofx@12345'}, verify=False)
        print(p.json())