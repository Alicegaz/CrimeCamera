import cv2
import numpy as np
from PyQt5.QtCore import pyqtSignal, QObject

from collections import defaultdict

FACE_IMG_SIZE = (126, 126)
FACE_SIMILARITY_THRESHOLD = 0.36    # square of Euclidean norm


class FaceReader(QObject):
    _face_pool_update_signal = pyqtSignal(object)

    def __init__(self, faces_dump_path, faces_centroids_path):
        super().__init__()
        self._faces_dump_path = faces_dump_path
        self._faces_centroids_path = faces_centroids_path
        self._centroids = np.load(faces_centroids_path)
        self._faces = self._load_faces(faces_dump_path)

    def add_subscriber(self, subscr_func):
        self._face_pool_update_signal.connect(subscr_func)

    def notify_face_pool_updates(self, frame_faces):
        if self._face_pool_update_signal is not None:
            self._face_pool_update_signal.emit(frame_faces)

    def _load_faces(self, faces_dump_path):
        faces = np.load(faces_dump_path)
        faces_dict = defaultdict(dict)
        for face in faces:
            frame_idx = int(face[0])
            face_descr = face[1:129]
            face_rect = tuple(map(int, face[129:133]))
            face_id = self._find_closest_centroid(face_descr)
            face_img = face[133:].reshape(48, 48, 3).astype(np.uint8)
            faces_dict[frame_idx][face_id] = (face_descr, face_img, face_rect)

        return faces_dict

    def _find_closest_centroid(self, descriptor):
        # Omit sqrt for speed
        distances = np.sum((self._centroids - descriptor) ** 2, axis=1)
        closest_centroid_idx = np.argmin(distances)
        if distances[closest_centroid_idx] > FACE_SIMILARITY_THRESHOLD:
            return -1

        return closest_centroid_idx

    @staticmethod
    def _get_photo_of_person(face_info, img):
        face_img = face_info[1]
        face_img = cv2.resize(face_img, FACE_IMG_SIZE)

        return face_img

    def _get_photos_of_people_on_frame(self, frame_idx, img):
        frame_faces_dict = self._faces[frame_idx]
        frame_faces = {}
        for face_id, face_info in frame_faces_dict.items():
            face_img = self._get_photo_of_person(face_info, img)
            frame_faces[face_id] = face_img

        if -1 in frame_faces:
            del frame_faces[-1]

        return frame_faces

    def update_face_pool(self, frame_idx, img):
        frame_faces = self._get_photos_of_people_on_frame(frame_idx, img)
        self.notify_face_pool_updates(frame_faces)
