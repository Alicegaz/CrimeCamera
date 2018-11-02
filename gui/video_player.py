import cv2

from PyQt5.QtCore import QThread, pyqtSignal

import logging
import time

logging.basicConfig(level=logging.DEBUG)


class VideoPlayer(QThread):
    _signal = pyqtSignal(int, object)

    def __init__(self, video_path):
        super().__init__()
        self._video_path = video_path
        self._subscr_func = None
        self._is_playing = False
        self._frame_idx = 0
        self._cap = None

    def add_subscriber(self, subscr_func):
        self._signal.connect(subscr_func)

    def notify_subscribers(self, frame_idx, img):
        if self._signal is not None:
            self._signal.emit(frame_idx, img)

    def play(self):
        if self._is_playing:
            return

        self._is_playing = True
        self.start()
        logging.info('Started video playback')

    def pause(self):
        self._is_playing = False
        self._stop_playing_thread()
        logging.info('Paused video playback')

    def stop(self):
        self.pause()
        if self._cap is not None:
            self._cap.release()
        self._cap = None
        self._frame_idx = 0

        logging.info('Stopped video playback')

    def _stop_playing_thread(self):
        self.wait()

    def open_video_capture(self):
        if self._cap is None:
            self._cap = cv2.VideoCapture(self._video_path)
            self._frame_idx = 0

        if not self._cap.isOpened():
            logging.error('Cannot open video capture. Check the video path')
            return False

        logging.info('Video capture was successfully opened')

        return True

    def run(self):
        is_opened = self.open_video_capture()
        if not is_opened:
            return

        while self._is_playing:
            ok, frame = self._cap.read()
            if not ok:
                self._cap.release()
                is_opened = self.open_video_capture()
                if not is_opened:
                    return

            self._frame_idx += 1
            img = frame[..., ::-1].copy()

            # Send to the controller
            self.notify_subscribers(self._frame_idx, img)

            time.sleep(1. / 30.)
