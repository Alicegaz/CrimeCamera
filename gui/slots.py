from custom_widgets import FacePoolsContainer
from utils import cvt_numpy_to_qscene

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

        # Face pools
        self._face_pools_container = FacePoolsContainer()
        self._ui.facePoolsScrollArea.setWidget(self._face_pools_container.scrollWidget)
        # self._ui.addWidgetBtn.clicked.connect(self.add_facepool)

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

    # def add_facepool(self):
    #     self._ui.scrollLayout.addWidget(FacePool())
