from gui_core.gui_utils import cvt_numpy_to_qscene

from PyQt5 import QtCore, QtWidgets, QtGui

IMG_SIZE = (128, 128)


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
            faceView.setFixedWidth(IMG_SIZE[0])
            faceView.setFixedHeight(IMG_SIZE[1])

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


class DBFaceGroup(QtWidgets.QFrame):
    def __init__(self, face_id, face_img, parent=None):
        super(DBFaceGroup, self).__init__(parent)
        self._face_id = face_id
        self._face_img = face_img

        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setLineWidth(2)

        main_layout = QtWidgets.QHBoxLayout(parent)
        main_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.setLayout(main_layout)

        face_view = QtWidgets.QGraphicsView(self)
        face_view.setFixedWidth(IMG_SIZE[0])
        face_view.setFixedHeight(IMG_SIZE[1])
        scene = cvt_numpy_to_qscene(face_img)
        face_view.setScene(scene)
        main_layout.addWidget(face_view)

        label = QtWidgets.QLabel(self)
        label.setText('Person # {}'.format(face_id))
        label.setMargin(10)
        font = QtGui.QFont()
        font.setPointSize(15)
        label.setFont(font)
        main_layout.addWidget(label)


class DBFacesContainer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(DBFacesContainer, self).__init__(parent)

        self.scrollLayout = QtWidgets.QVBoxLayout()
        self.scrollLayout.setAlignment(QtCore.Qt.AlignTop)
        self.scrollWidget = QtWidgets.QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        self._face_groups = {}

    def add_person(self, face_id, face_img):
        print('Adding person {}'.format(face_id))
        face_group = DBFaceGroup(face_id, face_img)
        self._face_groups[face_id] = face_group
        self.scrollLayout.addWidget(face_group)
