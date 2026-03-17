import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, QtGui, QtCore
from design import Ui_MainWindow
from PyQt5.QtGui import QPixmap

class DesignWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(DesignWindow, self).__init__()
        self.setupUi(self)
        self.image = None
        self.pushButton.clicked.connect(self.get_image)
        self.pushButton_3.clicked.connect(self.showRedChannel)
        self.pushButton_4.clicked.connect(self.showGreenChannel)
        self.pushButton_5.clicked.connect(self.showBlueChannel)
        self.pushButton_2.clicked.connect(self.show_HistColor)
        self.pushButton_6.clicked.connect(self.show_UpdatedImgGray)
        self.pushButton_7.clicked.connect(self.show_HistGray)

    def get_image(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.jpg *.jpeg *.png)")
        if file:
            self.image = cv2.imread(file)
            self.showDimensions()
            pix = self.convert_cv_qt(self.image, self.label_7)
            self.label_7.setPixmap(pix)

    def convert_cv_qt(self, cv_image, target_label):
        h, w, ch = cv_image.shape
        bytes_per_line = ch * w
        qimg = QtGui.QImage(cv_image.data, w, h, bytes_per_line, QtGui.QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(qimg)
        return pixmap.scaled(target_label.width(), target_label.height(), QtCore.Qt.IgnoreAspectRatio)

    def showDimensions(self):
        h, w, ch = self.image.shape
        self.label_19.setText(f"Hauteur: {h}\nLargeur: {w}\nCanaux: {ch}")

    def showRedChannel(self):
        r = self.image[:, :, 2]
        pix = self.convert_cv_qt(cv2.merge([np.zeros_like(r), np.zeros_like(r), r]), self.label)
        self.label.setPixmap(pix)

    def showGreenChannel(self):
        g = self.image[:, :, 1]
        pix = self.convert_cv_qt(cv2.merge([np.zeros_like(g), g, np.zeros_like(g)]), self.label_2)
        self.label_2.setPixmap(pix)

    def showBlueChannel(self):
        b = self.image[:, :, 0]
        pix = self.convert_cv_qt(cv2.merge([b, np.zeros_like(b), np.zeros_like(b)]), self.label_3)
        self.label_3.setPixmap(pix)

    def show_HistColor(self):
        plt.figure(figsize=(8, 6))
        colors = ('b', 'g', 'r')
        for i, col in enumerate(colors):
            hist = cv2.calcHist([self.image], [i], None, [256], [0, 256])
            plt.plot(hist, color=col, linewidth=2)
        plt.xlim([0, 256])
        plt.xlabel("Intensité")
        plt.ylabel("Fréquence des pixels")
        plt.title("Histogramme couleur")
        plt.savefig("Color_Histogram.png", bbox_inches='tight')
        pix = QPixmap("Color_Histogram.png")
        pix = pix.scaled(self.label_4.width(), self.label_4.height(), QtCore.Qt.IgnoreAspectRatio)
        self.label_4.setPixmap(pix)
        plt.close()

    def getContrast(self):
        return float(self.textEdit.toPlainText())

    def getBrightness(self):
        return float(self.textEdit_2.toPlainText())

    def show_UpdatedImgGray(self):
        alpha = self.getContrast()
        beta = self.getBrightness()
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        updated = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
        pix = self.convert_cv_qt(cv2.cvtColor(updated, cv2.COLOR_GRAY2BGR), self.label_6)
        self.label_6.setPixmap(pix)
        cv2.imwrite("UpdatedGray.png", updated)

    def show_HistGray(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        plt.figure(figsize=(8, 6))
        plt.plot(hist, color='black', linewidth=2)
        plt.xlim([0, 256])
        plt.xlabel("Niveaux de gris")
        plt.ylabel("Fréquence des pixels")
        plt.title("Histogramme en niveaux de gris")
        plt.savefig("Gray_Histogram.png", bbox_inches='tight')
        pix = QPixmap("Gray_Histogram.png")
        pix = pix.scaled(self.label_5.width(), self.label_5.height(), QtCore.Qt.IgnoreAspectRatio)
        self.label_5.setPixmap(pix)
        plt.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DesignWindow()
    window.show()
    sys.exit(app.exec_())