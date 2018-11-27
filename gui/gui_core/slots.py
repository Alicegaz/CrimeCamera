from gui_core.custom_widgets import FacePoolsContainer,\
    DBFacesContainer, KeyFramesHighContainer
from gui_core.gui_utils import cvt_numpy_to_qscene

import logging

logging.basicConfig(level=logging.DEBUG)


class SlotsHandler:
    def __init__(self, ui, tab_widget, system):
        self._ui = ui
        self._tab_widget = tab_widget
        self._system = system
        self.init_ui()

    def init_ui(self):
        self._ui.playBtn.clicked.connect(self.play_video)
        self._ui.pauseBtn.clicked.connect(self.pause_video)
        self._ui.stopBtn.clicked.connect(self.stop_video)

        self._ui.speedUp4.clicked.connect(lambda: self._system.update_playing_speed('4x'))
        self._ui.speedUp2.clicked.connect(lambda: self._system.update_playing_speed('2x'))
        self._ui.speedUp1.clicked.connect(lambda: self._system.update_playing_speed('1x'))
        self._ui.slowDown2.clicked.connect(lambda: self._system.update_playing_speed('0.5x'))
        self._ui.slowDown4.clicked.connect(lambda: self._system.update_playing_speed('0.25x'))

        self._ui.prevVideoBtn.clicked.connect(self._system.prev_video)
        self._ui.nextVideoBtn.clicked.connect(self._system.next_video)

        # Face pools
        self._face_pools_container = FacePoolsContainer()
        self._ui.prevVideoBtn.clicked.connect(self._face_pools_container.empty_container)
        self._ui.nextVideoBtn.clicked.connect(self._face_pools_container.empty_container)
        self._ui.stopBtn.clicked.connect(self._face_pools_container.empty_container)
        self._ui.facePoolsScrollArea.setWidget(self._face_pools_container.scrollWidget)

        self._system.subscribe_on_video(self.update_video_frame)
        self._system.subscribe_on_pool_faces(self._face_pools_container.update_pools)

        self._frames_high_container = KeyFramesHighContainer(self._ui.personLabel)
        self._ui.keyFramesScrollArea.setWidget(self._frames_high_container.scrollWidget)
        self._system.subscribe_on_key_frame_updates(self._frames_high_container.add_key_frame)

        self._db_face_container = DBFacesContainer(self._frames_high_container)
        self._ui.facesScrollArea.setWidget(self._db_face_container.scrollWidget)
        self._system.subscribe_on_db_face_adds(self._db_face_container.add_person)
        self._db_face_container.subscribe_on_face_group_click(self.on_face_group_click)
        self._tab_widget.currentChanged.connect(lambda i: self._system.load_db_face_imgs() if i == 1 else None)

        self._ui.clearKeyFramesBtn.clicked.connect(self._frames_high_container.empty_container)

        logging.info('Slots handler initialized')

    def play_video(self):
        logging.info('Play button clicked')
        self._system.play_video()

    def pause_video(self):
        logging.info('Pause button clicked')
        self._system.pause_video()

    def stop_video(self):
        logging.info('Stop button clicked')
        self._system.stop_video()

    def update_video_frame(self, frame_idx, img):
        scene = cvt_numpy_to_qscene(img)
        self._ui.graphicsView.setScene(scene)

    def on_face_group_click(self, face_id):
        logging.info('Face group {} is clicked'.format(face_id))
        self._system.find_face(face_id)
