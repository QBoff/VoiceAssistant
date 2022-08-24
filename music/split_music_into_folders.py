from xml.etree.ElementTree import indent
from yandex_music import Client
import time
import webbrowser
import random
import json


client = Client("AQAAAAAzFLLXAAG8Xu8VhUQ4DU6OuxrMBansI50")
# client.users_likes_tracks()[0].fetch_track().download('example.mp3')
tracks = client.users_likes_tracks()
