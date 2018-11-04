from gui_core.gui_utils import cvt_numpy_to_qscene

from PyQt5 import QtCore, QtWidgets, QtGui

FACE_IMG_SIZE = (128, 128)
FRAME_IMG_SIZE = (216, 162)


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
            faceView.setFixedWidth(FACE_IMG_SIZE[0])
            faceView.setFixedHeight(FACE_IMG_SIZE[1])

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

    def empty_container(self):
        for i in reversed(range(self.scrollLayout.count())):
            self.scrollLayout.itemAt(i).widget().deleteLater()
        self._face_pools = {}


class DBFaceGroup(QtWidgets.QFrame):
    def __init__(self, face_id, face_img, parent=None):
        super(DBFaceGroup, self).__init__(parent)
        self._face_id = face_id
        self._face_img = face_img

        self.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setLineWidth(1)

        main_layout = QtWidgets.QHBoxLayout(parent)
        main_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.setLayout(main_layout)

        face_view = QtWidgets.QGraphicsView(self)
        face_view.setFixedWidth(FACE_IMG_SIZE[0])
        face_view.setFixedHeight(FACE_IMG_SIZE[1])
        scene = cvt_numpy_to_qscene(face_img)
        face_view.setScene(scene)
        main_layout.addWidget(face_view)

        inner_layout = QtWidgets.QVBoxLayout(self)
        inner_layout.setAlignment(QtCore.Qt.AlignVCenter)
        inner_widget = QtWidgets.QWidget(self)
        inner_widget.setLayout(inner_layout)
        main_layout.addWidget(inner_widget)

        label = QtWidgets.QLabel(inner_widget)
        label.setText('Person # {}'.format(face_id))
        label.setMargin(10)
        font = QtGui.QFont()
        font.setPointSize(15)
        label.setFont(font)
        inner_layout.addWidget(label)

        self.search_btn = QtWidgets.QPushButton(inner_widget)
        self.search_btn.setText('Search')
        font = QtGui.QFont()
        font.setPointSize(12)
        self.search_btn.setFont(font)
        inner_layout.addWidget(self.search_btn)


class DBFacesContainer(QtWidgets.QWidget):
    def __init__(self, key_frames_high_container, parent=None):
        super(DBFacesContainer, self).__init__(parent)

        self._key_frames_high_container = key_frames_high_container

        self.scrollLayout = QtWidgets.QVBoxLayout()
        self.scrollLayout.setAlignment(QtCore.Qt.AlignTop)
        self.scrollWidget = QtWidgets.QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        self._face_groups = {}
        self._fg_click_subscr_funcs = []

    def add_person(self, face_id, face_img):
        print('Adding person {}'.format(face_id))
        face_group = DBFaceGroup(face_id, face_img)
        for subscr_func in self._fg_click_subscr_funcs:
            face_group.search_btn.clicked.connect(lambda: subscr_func(face_id))
            face_group.search_btn.clicked.connect(
                lambda: self._key_frames_high_container.update_person_label(face_id))

        self._face_groups[face_id] = face_group
        self.scrollLayout.addWidget(face_group)

    def subscribe_on_face_group_click(self, subscr_func):
        self._fg_click_subscr_funcs.append(subscr_func)


class KeyFramesContainer(QtWidgets.QWidget):
    def __init__(self, video_path, parent=None):
        super(KeyFramesContainer, self).__init__(parent)

        self._video_path = video_path

        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Fixed)
        size_policy.setVerticalStretch(0)
        self.setSizePolicy(size_policy)

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.setLayout(self.main_layout)

        self.scrollLayout = QtWidgets.QHBoxLayout()
        self.scrollLayout.setAlignment(QtCore.Qt.AlignLeft)
        self.scrollWidget = QtWidgets.QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)
        # self.scrollWidget.setSizePolicy(size_policy)

        # self.groupBox = QtWidgets.QGroupBox(parent)
        # self.groupBox.setTitle('{}'.format(video_path))
        # self.groupBox.setLayout(self.scrollLayout)
        # self.main_layout.addWidget(self.groupBox)

        self.scrollArea = QtWidgets.QScrollArea(self)
        # self.scrollArea.setGeometry(QtCore.QRect(200, 200, 591, 751))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setSizePolicy(size_policy)
        self.scrollWidget.setSizePolicy(size_policy)
        self.main_layout.addWidget(self.scrollArea)

        # self.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self._frame_group = {}

    def add_key_frame(self, frame_idx, frame):
        if frame_idx not in self._frame_group:
            frame_view = QtWidgets.QGraphicsView(self)
            frame_view.setFixedWidth(FRAME_IMG_SIZE[0])
            frame_view.setFixedHeight(FRAME_IMG_SIZE[1])
            scene = cvt_numpy_to_qscene(frame)
            frame_view.setScene(scene)
            self.scrollLayout.addWidget(frame_view)
            self._frame_group[frame_idx] = frame_view


class KeyFramesHighContainer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(KeyFramesHighContainer, self).__init__(parent)

        main_layout = QtWidgets.QVBoxLayout(parent)
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(main_layout)

        self.person_label = QtWidgets.QLabel(self)
        # self.person_label.setHidden(True)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.person_label.setFont(font)
        main_layout.addWidget(self.person_label)

        self.scrollLayout = QtWidgets.QVBoxLayout()
        self.scrollLayout.setAlignment(QtCore.Qt.AlignTop)
        self.scrollWidget = QtWidgets.QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)
        main_layout.addWidget(self.scrollWidget)

        self._frame_groups = {}

    def update_person_label(self, face_id):
        self.person_label.setText('Person # {} appeared at:'.format(face_id))
        # self.person_label.setHidden(False)

    def add_key_frame(self, video_path, frame_idx, frame):
        print('Got notification. frame_idx: {}'.format(frame_idx))
        if video_path not in self._frame_groups:
            frame_group = KeyFramesContainer(video_path, self)
            self.scrollLayout.addWidget(frame_group)
            self._frame_groups[video_path] = frame_group

        self._frame_groups[video_path].add_key_frame(frame_idx, frame)

    def empty_container(self):
        for i in reversed(range(self.scrollLayout.count())):
            self.scrollLayout.itemAt(i).widget().deleteLater()
        self._frame_groups = {}
        # self.person_label.setHidden(True)
