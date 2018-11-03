from gui_core.gui_utils import cvt_numpy_to_qscene

from PyQt5 import QtCore, QtGui, QtWidgets


class FacePool(QtWidgets.QGroupBox):
    def __init__(self, person_id, parent=None):
        super(FacePool, self).__init__(parent)

        n_slots = 4
        self._n_slots = n_slots
        self._size = 0

        self.layout = QtWidgets.QHBoxLayout()
        self.setTitle('Person # {}'.format(person_id))
        self.faceViews = []
        for i in range(self._n_slots):
            faceView = QtWidgets.QGraphicsView(parent)
            faceView.setFixedWidth(128)
            faceView.setFixedHeight(128)

            self.faceViews.append(faceView)
            self.layout.addWidget(faceView)

        self.setLayout(self.layout)

    def push_face_img(self, face_img):
        if self._n_slots <= 0:
            return

        new_scene = cvt_numpy_to_qscene(face_img)

        if self._size < self._n_slots:
            self.faceViews[self._size].setScene(new_scene)
            self._size += 1
            return

        for i in range(0, self._n_slots - 1):
            cur_scene = self.faceViews[i + 1].scene()
            self.faceViews[i].setScene(cur_scene)

        self.faceViews[-1].setScene(new_scene)


class FacePoolsContainer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(FacePoolsContainer, self).__init__(parent)

        self.scrollLayout = QtWidgets.QVBoxLayout()
        self.scrollLayout.setAlignment(QtCore.Qt.AlignTop)
        self.scrollWidget = QtWidgets.QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        self._face_pools = {}

    def update_pools(self, frame_faces):
        for face_id, face_img in frame_faces.items():
            if face_id not in self._face_pools:
                face_pool = FacePool(len(self._face_pools) + 1)
                self._face_pools[face_id] = face_pool
                self.scrollLayout.addWidget(face_pool)

            self._face_pools[face_id].push_face_img(face_img)
