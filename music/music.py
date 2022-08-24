from yandex_music import Client
import time
import webbrowser
import random


client = Client("AQAAAAAzFLLXAAG8Xu8VhUQ4DU6OuxrMBansI50")
# client.users_likes_tracks()[0].fetch_track().download('example.mp3')
tracks = client.users_likes_tracks()
# print(tracks[1].fetch_track().duration_ms / 1000 / 60)
recurring_tracks = []
index_of_track = random.randint(0, len(tracks) - 1)
path = "music/track.mp3"
sec = 0


def play_music():
    global index_of_track, sec
    if len(recurring_tracks) == len(tracks):
        return "Стоп"

    # for _ in range(10):
    while index_of_track in recurring_tracks:
        index_of_track = random.randint(0, len(tracks) - 1)

    track_now = tracks[index_of_track].fetch_track().download(path)

    recurring_tracks.append(index_of_track)
    time.sleep(1)
    webbrowser.open("D:\\MyProjects\\VoiceAssistant\\music\\track.mp3")

    ind_now = index_of_track
    # sec = int(tracks[index_of_track].fetch_track().duration_ms / 1000)
    # time.sleep(tracks[index_of_track].fetch_track().duration_ms / 1000)

    # if index_of_track == ind_now:
    #     return "Я переключила трэк."
    # else:
    #     return "Переключите трэк"


def play_next_track():
    tracks[index_of_track].fetch_track().download(path)
    time.sleep(2)
    webbrowser.open("D:\\MyProjects\\VoiceAssistant\\music\\track.mp3")


def next_track():
    global index_of_track

    while index_of_track in recurring_tracks:
        index_of_track = random.randint(0, len(tracks) - 1)
    recurring_tracks.append(index_of_track)

    return index_of_track


def prev_track():
    pass
