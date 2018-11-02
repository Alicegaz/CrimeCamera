import cv2

from PyQt5.QtCore import QThread, pyqtSignal

import logging
import time

logging.basicConfig(level=logging.DEBUG)

DEFAULT_FRAME_SLEEP = 1. / 30.


class VideoPlayer(QThread):
    _update_frame_signal = pyqtSignal(int, object)

    def __init__(self, video_path):
        super().__init__()
        self._video_path = video_path
        self._subscr_func = None
        self._is_playing = False
        self._frame_idx = 0
        self._cap = None
        self._frame_sleep = DEFAULT_FRAME_SLEEP

    def add_subscriber(self, subscr_func):
        self._update_frame_signal.connect(subscr_func)

    def notify_frame_updates(self, frame_idx, img):
        if self._update_frame_signal is not None:
            self._update_frame_signal.emit(frame_idx, img)

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

    def update_frame_sleep(self, speed_up):
        if speed_up == '4x':
            self._frame_sleep = DEFAULT_FRAME_SLEEP / 4.
        elif speed_up == '2x':
            self._frame_sleep = DEFAULT_FRAME_SLEEP / 2.
        elif speed_up == '0.5x':
            self._frame_sleep = DEFAULT_FRAME_SLEEP * 2.
        elif speed_up == '0.25x':
            self._frame_sleep = DEFAULT_FRAME_SLEEP * 4.
        else:
            self._frame_sleep = DEFAULT_FRAME_SLEEP

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
            self.notify_frame_updates(self._frame_idx, img)

            time.sleep(self._frame_sleep)
