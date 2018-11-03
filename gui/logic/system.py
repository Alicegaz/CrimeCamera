from logic.video_player import VideoPlayer
from logic.face_reader import FaceReader

VIDEO_PATH = '../data/faces/detected_faces4.mp4'
FACES_DUMP_PATH = '../descriptors/faces4.npy'
FACES_CENTROIDS_PATH = '../descriptors/faces3_centroids.npy'

PATHS_CONFIG = [
    ('../data/faces/detected_faces4.mp4',
     '../descriptors/faces4.npy',
     '../descriptors/faces3_centroids.npy'),
    ('../data/faces/detected_faces1.mp4',
     '../descriptors/faces1.npy',
     '../descriptors/faces1_centroids.npy'),
    ('../data/faces/detected_faces2.mp4',
     '../descriptors/faces2.npy',
     '../descriptors/faces2_centroids.npy'),
    ('../data/faces/detected_faces3.mp4',
     '../descriptors/faces3.npy',
     '../descriptors/faces3_centroids.npy')
]

DEFAULT_VIDEO_IDX = 0


class System:
    def __init__(self):
        self._video_player = VideoPlayer(PATHS_CONFIG[DEFAULT_VIDEO_IDX][0])
        self._face_reader = FaceReader(PATHS_CONFIG[DEFAULT_VIDEO_IDX][1],
                                       PATHS_CONFIG[DEFAULT_VIDEO_IDX][2])
        self._cur_video = DEFAULT_VIDEO_IDX
        self._n_videos = len(PATHS_CONFIG)

        self._subscribers_on_video = []
        self._subscribers_on_pool_faces = []

    def subscribe_on_video(self, subscr_func):
        self._apply_subscription_on_video(subscr_func)
        self._subscribers_on_video.append(subscr_func)

    def subscribe_on_pool_faces(self, subscr_func):
        self._apply_subscription_on_pool_faces(subscr_func)
        self._subscribers_on_pool_faces.append(subscr_func)

    def _apply_subscription_on_video(self, subscr_func):
        self._video_player.add_subscriber(subscr_func)

    def _apply_subscription_on_pool_faces(self, subscr_func):
        self._video_player.add_subscriber(self._face_reader.update_face_pool)
        self._face_reader.add_subscriber(subscr_func)

    def play_video(self):
        self._video_player.play()

    def pause_video(self):
        self._video_player.pause()

    def stop_video(self):
        self._video_player.stop()

    def update_playing_speed(self, speed_up):
        self._video_player.update_frame_sleep(speed_up)

    def play_another_video(self, video_idx):
        self._video_player.stop()
        self._video_player = VideoPlayer(PATHS_CONFIG[video_idx][0])
        self._face_reader = FaceReader(PATHS_CONFIG[video_idx][1],
                                       PATHS_CONFIG[video_idx][2])
        for subscr_func in self._subscribers_on_video:
            self._apply_subscription_on_video(subscr_func)
        for subscr_func in self._subscribers_on_pool_faces:
            self._apply_subscription_on_pool_faces(subscr_func)

        self.play_video()

    def next_video(self):
        self._cur_video = (self._cur_video + 1) % self._n_videos
        self.play_another_video(self._cur_video)

    def prev_video(self):
        self._cur_video = self._n_videos - 1 if self._cur_video - 1 < 0 else self._cur_video - 1
        self.play_another_video(self._cur_video)
