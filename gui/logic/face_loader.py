import numpy as np
from collections import defaultdict

FACE_SIMILARITY_THRESHOLD = 0.36  # square of Euclidean norm


class FaceLoader:
    def __init__(self, faces_dump_path, faces_centroids_path):
        self._faces_dump_path = faces_dump_path
        self._faces_centroids_path = faces_centroids_path

    def load_faces(self):
        centroids = np.load(self._faces_centroids_path)

        faces = np.load(self._faces_dump_path)
        faces_dict = defaultdict(dict)
        for face in faces:
            frame_idx = int(face[0])
            face_descr = face[1:129]
            face_rect = tuple(map(int, face[129:133]))
            face_id = self._find_closest_centroid(centroids, face_descr)
            face_img = face[133:].reshape(48, 48, 3).astype(np.uint8)
            faces_dict[frame_idx][face_id] = (face_descr, face_img, face_rect)

        return faces_dict, centroids

    @staticmethod
    def _find_closest_centroid(centroids, descriptor):
        # Omit sqrt for speed
        distances = np.sum((centroids - descriptor) ** 2, axis=1)
        closest_centroid_idx = np.argmin(distances)
        if distances[closest_centroid_idx] > FACE_SIMILARITY_THRESHOLD:
            return -1

        return closest_centroid_idx
