from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    @task(2)
    def view_post_image_1mb(self):
        self.client.get("/post-with-1mb-image")  # Rota para post com imagem de 1 MB

    @task(2)
    def view_post_text_400kb(self):
        self.client.get("/post-with-400kb-text")  # Rota para post com texto de 400 KB

    @task(1)
    def view_post_image_300kb(self):
        self.client.get("/post-with-300kb-image")  # Rota para post com imagem de 300 KB

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 3)  # Tempo de espera entre as requisições
