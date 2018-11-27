from logic.video_player import VideoPlayer
from logic.face_reader import FaceReader
from logic.face_searcher import FaceSearcher

import json

PATH_TO_FACES_DATABASE = './logic/database_config.json'
DEFAULT_VIDEO_IDX = 0


class System:
    def __init__(self):
        self._fdb_conf, db_size = self._load_faces_database_config(PATH_TO_FACES_DATABASE)

        self._video_player = VideoPlayer(self._fdb_conf['video_paths'][DEFAULT_VIDEO_IDX])
        self._face_reader = FaceReader(self._fdb_conf['faces_descriptors'][DEFAULT_VIDEO_IDX],
                                       self._fdb_conf['faces_centroids'][DEFAULT_VIDEO_IDX])
        self._face_searcher = FaceSearcher(self._fdb_conf)
        self._cur_video = DEFAULT_VIDEO_IDX
        self._n_videos = db_size

        self._subscribers_on_video = []
        self._subscribers_on_pool_faces = []

    def subscribe_on_video(self, subscr_func):
        self._apply_subscription_on_video(subscr_func)
        self._subscribers_on_video.append(subscr_func)

    def subscribe_on_pool_faces(self, subscr_func):
        self._apply_subscription_on_pool_faces(subscr_func)
        self._subscribers_on_pool_faces.append(subscr_func)

    def subscribe_on_db_face_adds(self, subscr_func):
        self._face_searcher.add_db_face_adds_subscriber(subscr_func)

    def subscribe_on_key_frame_updates(self, subscr_func):
        self._face_searcher.add_frame_updates_subscriber(subscr_func)

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
        self._video_player = VideoPlayer(self._fdb_conf['video_paths'][video_idx])
        self._face_reader = FaceReader(self._fdb_conf['faces_descriptors'][video_idx],
                                       self._fdb_conf['faces_centroids'][video_idx])
        for subscr_func in self._subscribers_on_video:
            self._apply_subscription_on_video(subscr_func)
        for subscr_func in self._subscribers_on_pool_faces:
            self._apply_subscription_on_pool_faces(subscr_func)

        self.play_video()

    def next_video(self):
        video_seq = [0, 3, 1, 2]
        self._cur_video = (self._cur_video + 1) % self._n_videos
        self.play_another_video(video_seq[self._cur_video])

    def prev_video(self):
        video_seq = [0, 3, 1, 2]
        self._cur_video = self._n_videos - 1 if self._cur_video - 1 < 0 else self._cur_video - 1
        self.play_another_video(video_seq[self._cur_video])

    def load_db_face_imgs(self):
        self._face_searcher.load_best_persons_photos()

    def find_face(self, face_id):
        self._face_searcher.find_face(face_id)

    @staticmethod
    def _load_faces_database_config(path_to_db):
        with open(path_to_db, 'r') as f:
            db = json.load(f)
        db_size = len(db['faces_centroids'])

        return db, db_size
