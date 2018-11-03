from gui_core.custom_widgets import FacePoolsContainer
from gui_core.gui_utils import cvt_numpy_to_qscene

import logging

logging.basicConfig(level=logging.DEBUG)


class SlotsHandler:
    def __init__(self, ui, system):
        self._ui = ui
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
        self._ui.facePoolsScrollArea.setWidget(self._face_pools_container.scrollWidget)

        self._system.subscribe_on_video(self.update_video_frame)
        self._system.subscribe_on_pool_faces(self._face_pools_container.update_pools)

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
        logging.info('Got image to show with frame idx: {}'.format(frame_idx))
        scene = cvt_numpy_to_qscene(img)
        self._ui.graphicsView.setScene(scene)
