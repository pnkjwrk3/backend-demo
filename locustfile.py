import random
from locust import HttpUser, task, between
from api.tests.utils_song_gen import create_random_song_dict


class APIUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.song_id = None
        self.create_song()

    def create_song(self):
        """Create a song and store its ID for later use."""
        song_data = create_random_song_dict()
        song_data["title"] = f"Song {random.randint(1, 10000)}"
        response = self.client.post("/songs/", json=song_data)
        if response.status_code == 200:
            self.song_id = response.json()["id"]

    @task(1)
    def get_songs(self):
        """Retrieve songs."""
        page = random.randint(1, 10)
        limit = random.randint(1, 50)
        self.client.get(f"/songs/?page={page}&limit={limit}")

    @task(2)
    def search_songs(self):
        """Search for songs by random title."""
        title = f"Song {random.randint(1, 10000)}"
        self.client.get(f"/songs/search/?title={title}")

    @task(1)
    def rate_song(self):
        """Rate a song."""
        if self.song_id:
            rating_data = {"rating": random.uniform(0, 5)}
            self.client.post(f"/songs/{self.song_id}/rate/", json=rating_data)

    @task(1)
    def get_song(self):
        """Retrieve a specific song by its ID."""
        if self.song_id:
            self.client.get(f"/songs/{self.song_id}/")


# Command: locust -f locustfile.py --host=http://127.0.0.1:8000
