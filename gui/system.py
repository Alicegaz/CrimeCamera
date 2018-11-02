from video_player import VideoPlayer

VIDEO_PATH = '../data/faces/detected_faces3.mp4'


class System:
    def __init__(self):
        self._video_player = VideoPlayer(VIDEO_PATH)

    def subscribe_on_video(self, subscr_func):
        if self._video_player is not None:
            self._video_player.add_subscriber(subscr_func)

    def play_video(self):
        self._video_player.play()

    def pause_video(self):
        self._video_player.pause()

    def stop_video(self):
        self._video_player.stop()
