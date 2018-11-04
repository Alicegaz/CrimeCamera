from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsScene


def cvt_numpy_to_qscene(img):
    height, width, channels = img.shape
    bytesPerLine = channels * width
    q_img = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
    scene = QGraphicsScene()
    scene.addPixmap(QPixmap(q_img))

    return scene
