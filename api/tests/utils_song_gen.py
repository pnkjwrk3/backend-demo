import random
import string
import uuid
from api.models import Song
from api.schemas import SongCreate


def create_random_song():
    song_id = str(uuid.uuid4())
    title = "".join(
        random.choices(string.ascii_letters + string.digits, k=random.randint(5, 20))
    )
    danceability = round(random.uniform(0.0, 1.0), 1)
    energy = round(random.uniform(0.0, 1.0), 1)
    key = random.randint(0, 11)
    loudness = round(random.uniform(-60.0, 0.0), 1)
    mode = random.randint(0, 1)
    acousticness = round(random.uniform(0.0, 1.0), 1)
    instrumentalness = round(random.uniform(0.0, 1.0), 1)
    liveness = round(random.uniform(0.0, 1.0), 1)
    valence = round(random.uniform(0.0, 1.0), 1)
    tempo = round(random.uniform(50.0, 200.0), 1)
    duration_ms = random.randint(30000, 600000)
    time_signature = random.randint(1, 8)
    num_bars = random.randint(50, 200)
    num_sections = random.randint(2, 10)
    num_segments = random.randint(5, 50)
    class_field = random.randint(0, 1)

    song_data = {
        "id": song_id,
        "title": title,
        "danceability": danceability,
        "energy": energy,
        "key": key,
        "loudness": loudness,
        "mode": mode,
        "acousticness": acousticness,
        "instrumentalness": instrumentalness,
        "liveness": liveness,
        "valence": valence,
        "tempo": tempo,
        "duration_ms": duration_ms,
        "time_signature": time_signature,
        "num_bars": num_bars,
        "num_sections": num_sections,
        "num_segments": num_segments,
        "class": class_field,
    }

    return SongCreate(**song_data)


def create_random_song_dict():
    song_id = str(uuid.uuid4())
    title = "".join(
        random.choices(string.ascii_letters + string.digits, k=random.randint(5, 20))
    )
    danceability = round(random.uniform(0.0, 1.0), 1)
    energy = round(random.uniform(0.0, 1.0), 1)
    key = random.randint(0, 11)
    loudness = round(random.uniform(-60.0, 0.0), 1)
    mode = random.randint(0, 1)
    acousticness = round(random.uniform(0.0, 1.0), 1)
    instrumentalness = round(random.uniform(0.0, 1.0), 1)
    liveness = round(random.uniform(0.0, 1.0), 1)
    valence = round(random.uniform(0.0, 1.0), 1)
    tempo = round(random.uniform(50.0, 200.0), 1)
    duration_ms = random.randint(30000, 600000)
    time_signature = random.randint(1, 8)
    num_bars = random.randint(50, 200)
    num_sections = random.randint(2, 10)
    num_segments = random.randint(5, 50)
    class_field = random.randint(0, 1)

    song_data = {
        "id": song_id,
        "title": title,
        "danceability": danceability,
        "energy": energy,
        "key": key,
        "loudness": loudness,
        "mode": mode,
        "acousticness": acousticness,
        "instrumentalness": instrumentalness,
        "liveness": liveness,
        "valence": valence,
        "tempo": tempo,
        "duration_ms": duration_ms,
        "time_signature": time_signature,
        "num_bars": num_bars,
        "num_sections": num_sections,
        "num_segments": num_segments,
        "class": class_field,
    }

    return song_data
