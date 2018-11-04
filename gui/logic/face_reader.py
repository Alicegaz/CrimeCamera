from logic.face_loader import FaceLoader

import cv2
from PyQt5.QtCore import pyqtSignal, QObject

FACE_IMG_SIZE = (126, 126)


class FaceReader(QObject):
    _face_pool_update_signal = pyqtSignal(object)

    def __init__(self, faces_dump_path, faces_centroids_path):
        super().__init__()
        face_loader = FaceLoader(faces_dump_path, faces_centroids_path)
        self._faces, _ = face_loader.load_faces()

    def add_subscriber(self, subscr_func):
        self._face_pool_update_signal.connect(subscr_func)

    def notify_face_pool_updates(self, frame_faces):
        if self._face_pool_update_signal is not None:
            self._face_pool_update_signal.emit(frame_faces)

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
