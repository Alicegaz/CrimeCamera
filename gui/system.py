from video_player import VideoPlayer
from face_reader import FaceReader

VIDEO_PATH = '../data/faces/detected_faces4.mp4'
FACES_DUMP_PATH = '../descriptors/faces4.npy'
FACES_CENTROIDS_PATH = '../descriptors/all_descr_centroids.npy'


class System:
    def __init__(self):
        self._video_player = VideoPlayer(VIDEO_PATH)
        self._face_reader = FaceReader(FACES_DUMP_PATH, FACES_CENTROIDS_PATH)

    def subscribe_on_video(self, subscr_func):
        if self._video_player is not None:
            self._video_player.add_subscriber(subscr_func)

    def subscribe_on_pool_faces(self, subscr_func):
        if self._face_reader is not None and self._video_player is not None:
            self._video_player.add_subscriber(self._face_reader.update_face_pool)
            self._face_reader.add_subscriber(subscr_func)

    def play_video(self):
        self._video_player.play()

    def pause_video(self):
        self._video_player.pause()

    def stop_video(self):
        self._video_player.stop()
