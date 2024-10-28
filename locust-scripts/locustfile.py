from locust import HttpUser, TaskSet, task, between
import os

class UserBehavior(TaskSet):
    @task(2)
    def view_post_image_1mb(self):
        self.client.get("/wp-content/uploads/2024/10/626311.jpg")  

    @task(2)
    def view_post_text_400kb(self):
        self.client.get("/2024/10/28/post-com-texto-de-400-kb/")  

    @task(1)
    def view_post_image_300kb(self):
        self.client.get("/wp-content/uploads/2024/10/1920x1080-Hd-Pictures-Download-1024x576.jpg")  

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 3)
    host = os.getenv("ATTACKED_HOST") 