from logic.face_loader import FaceLoader

import cv2
import numpy as np
import time

from PyQt5.QtCore import pyqtSignal, QThread

import logging

# minimum number of frames that must be skipped in order to treat face_id as disappeared
FACE_IMG_SIZE = (126, 126)
VIDEO_FRAME_SIZE = (214, 160)
PROCESSING_SIMULATION_SLEEP = 0.1


class FaceSearcher(QThread):
    _frame_updates_signal = pyqtSignal(str, int, object)
    _db_face_adds_signal = pyqtSignal(int, object)

    def __init__(self, fdb_conf):
        super().__init__()
        self._fdb_conf = fdb_conf
        self._face_db = self.load_faces_database()

        self._face_id_to_search = None

    def add_frame_updates_subscriber(self, subscr_func):
        self._frame_updates_signal.connect(subscr_func)

    def notify_frame_updates(self, video_path, frame_idx, frame):
        time.sleep(PROCESSING_SIMULATION_SLEEP)
        if self._frame_updates_signal is not None:
            self._frame_updates_signal.emit(video_path, frame_idx, frame)

    def add_db_face_adds_subscriber(self, subscr_func):
        self._db_face_adds_signal.connect(subscr_func)

    def notify_db_adds(self, face_id, face_img):
        if self._db_face_adds_signal is not None:
            self._db_face_adds_signal.emit(face_id, face_img)

    def load_faces_database(self):
        global_centroids = np.load(self._fdb_conf['global_centroids'])
        n_faces = global_centroids.shape[0]

        faces_db = {'local_fdbs': {}, 'global_centroids': global_centroids,
                    'n_faces': n_faces}
        for video_path, descrs_path, centroids_path in zip(
                self._fdb_conf['video_paths'],
                self._fdb_conf['faces_descriptors'],
                self._fdb_conf['faces_centroids']):
            local_fdb = {'frame_idxs': [], 'face_ids': [],
                         'face_descrs': [], 'face_imgs': []}

            face_loader = FaceLoader(descrs_path, self._fdb_conf['global_centroids'])
            faces, _ = face_loader.load_faces()

            for frame_idx, face in faces.items():
                for face_id, (face_descr, face_img, _) in face.items():
                    local_fdb['frame_idxs'].append(frame_idx)
                    local_fdb['face_ids'].append(face_id)
                    local_fdb['face_descrs'].append(face_descr)
                    local_fdb['face_imgs'].append(face_img)

            faces_db['local_fdbs'][video_path] = local_fdb

        return faces_db

    def load_best_persons_photos(self):
        for face_id in range(self._face_db['n_faces']):
            face_img = self.load_best_person_photo(face_id)
            self.notify_db_adds(face_id, face_img)

    def load_best_person_photo(self, face_id):
        g_centroids = self._face_db['global_centroids']
        assert (face_id >= 0) and (face_id < g_centroids.shape[0]), \
            'face_id must be from range [0, # of centroids - 1]'

        centroid = g_centroids[face_id]
        min_dist = 10.  # FIXME
        best_img = None

        for local_fdb in self._face_db['local_fdbs'].values():
            for cur_face_id, face_descr, face_img in zip(
                    local_fdb['face_ids'], local_fdb['face_descrs'], local_fdb['face_imgs']):
                if cur_face_id != face_id:
                    continue

                dist = np.sum((centroid - face_descr) ** 2)
                if dist < min_dist:
                    best_img = face_img

        best_img = cv2.resize(best_img, FACE_IMG_SIZE)

        return best_img

    def find_face(self, face_id):
        self._face_id_to_search = face_id
        self.start()

    def run(self):
        if self._face_id_to_search is None or \
                self._face_id_to_search >= self._face_db['n_faces'] or \
                self._face_id_to_search < 0:
            logging.warning('Got unexpected face id: {}. Expected in range: [0, {}]'
                            .format(self._face_id_to_search, self._face_db['n_faces']))
            return

        self._find_face(self._face_id_to_search)

    def _find_face(self, face_id):
        for video_path, local_fdb in self._face_db['local_fdbs'].items():
            logging.info('find_face. Reading video {}'.format(video_path))
            found_frames = []
            for cur_face_id, frame_idx in zip(
                    local_fdb['face_ids'], local_fdb['frame_idxs']):
                if cur_face_id != face_id:
                    continue

                found_frames.append(frame_idx)
            if face_id == 0:
                key_frames, _ = self._filter_key_frames(found_frames, window_smoothness=2)
            elif face_id == 1:
                key_frames, _ = self._filter_key_frames(found_frames, window_smoothness=2)
            else:
                key_frames, _ = self._filter_key_frames(found_frames, window_smoothness=10)
            self._notify_key_frame_updates(video_path, key_frames)

    @staticmethod
    def _filter_key_frames(found_frames, wsize=50, unseen_th=100, window_smoothness=30):
        if len(found_frames) <= 1:
            return found_frames

        found_frames = np.array(found_frames)
        frame_diffs = np.diff(found_frames)

        peaks = np.where(frame_diffs > unseen_th)[0]
        peaks = np.hstack([[0], peaks])  # Treat first key frame as a peak

        filtered_peaks = []
        for peak in peaks:
            window_diffs = frame_diffs[peak:peak + wsize]
            # if the diff function in window is smooth enough
            if (window_diffs < window_smoothness).sum() >= wsize - 1:
                filtered_peaks.append(peak)

        filtered_frames = list(found_frames[filtered_peaks])

        return filtered_frames, filtered_peaks

    def _notify_key_frame_updates(self, video_path, key_frames):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logging.warning('Video capture was not open for video path: {}'.format(video_path))

        for key_frame in key_frames:
            cap.set(1, key_frame)
            ok, frame = cap.read()
            if not ok:
                logging.warning('Cannot read {} frame for video: {}'
                                .format(key_frame, video_path))
                continue

            frame = frame[..., ::-1].copy()
            frame = cv2.resize(frame, VIDEO_FRAME_SIZE)
            self.notify_frame_updates(video_path, key_frame, frame)

        cap.release()
