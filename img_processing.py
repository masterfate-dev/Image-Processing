from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from numpy.distutils.fcompiler import none

from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.searcher import Searcher
import cv2
import numpy as np
import os
from matplotlib import pyplot as plt


class Img_Proc_Gui(QWidget):
    def __init__(self, parent=None):
        super(Img_Proc_Gui, self).__init__(parent)
        self.img_processed = False
        btn_process_img = QPushButton("Process Image")
        #calling for INPUT
        btn_process_img.clicked.connect(self.getInput)

        btn_quit = QPushButton("Quit")
        btn_quit.clicked.connect(self.quit_clicked)
        hbox_btn = QHBoxLayout()
        hbox_btn.addWidget(btn_process_img)
        hbox_btn.addWidget(btn_quit)

        hbox_address = QHBoxLayout()
        self.address = QLineEdit()
        hbox_address.addWidget(self.address)
        btn_img_explorer = QPushButton('Open Image')
        hbox_address.addWidget(btn_img_explorer)

        btn_img_explorer.clicked.connect(self.open)

        hbox_size = QHBoxLayout()
        label_width = QLabel('Width :')
        label_height = QLabel('Height :')
        self.et_width = QLineEdit()
        self.et_height = QLineEdit()
        hbox_size.addWidget(label_width)
        hbox_size.addWidget(self.et_width)
        hbox_size.addWidget(label_height)
        hbox_size.addWidget(self.et_height)

        hbox_colorscale = QHBoxLayout()
        color_scale = QLabel('Color Scale :')
        self.Cbas = QRadioButton('COLOR BASED ', self)
        self.Hias = QRadioButton('Histogram BASED ', self)
        self.Eias = QRadioButton('Edge Detection ', self)
        self.Grey_scale = QRadioButton('Grey',self)
        self.Hsv = QRadioButton('HSV ',self)
        hbox_colorscale.addWidget(color_scale)
        hbox_colorscale.addWidget(self.Cbas)
        hbox_colorscale.addWidget(self.Hias)
        hbox_colorscale.addWidget(self.Eias)
        hbox_colorscale.addWidget(self.Grey_scale)
        hbox_colorscale.addWidget(self.Hsv)

        hbox_save = QHBoxLayout()
        self.address_save = QLineEdit()
        hbox_save.addWidget(self.address_save)
        self.btn_save = QPushButton('Save Image')
        self.btn_save.clicked.connect(self.save)
        hbox_save.addWidget(self.btn_save)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_address)
        vbox.addLayout(hbox_size)
        vbox.addLayout(hbox_colorscale)
        vbox.addLayout(hbox_btn)
        vbox.addLayout(hbox_save)

        self.setGeometry(400,300,400,200)
        self.setWindowTitle('Image Processing')
        self.setLayout(vbox)

    #@pyqtSlot()
    def quit_clicked(self):
        print("Sayonaara!!")
        cv2.destroyAllWindows()
        self.close()

   # @pyqtSlot()
    def open(self):
        fileName = QFileDialog.getOpenFileName(self,'openFile')
        self.address.setText(fileName[0])

        self.showImage(fileName[0])
        #print(fileName)

    def save(self):
        if self.img_processed:
            saveFile = QFileDialog.getSaveFileName(self,'saveFile')
            self.address_save.setText(saveFile[0])
            if saveFile[0] != '':
                cv2.imwrite(str(self.address_save.text()),self.req_img)
        else:
            QMessageBox.about(self,'Suggestion','Do Something')


    def showImage(self,address):
        img = cv2.imread(address)
        cv2.imshow('INPUT',img)

    def getInput(self):
        self.req_height = self.et_height.text()
        self.req_width = self.et_width.text()
        if self.req_width != '' and self.req_height != '':
            self.ready = True
            self.img_processed = True
        else:
            self.ready =  False

        if self.ready == False :
            QMessageBox.about(self,'Error','Fill parameters to process')
        elif self.address.text() == '':
            QMessageBox.about(self,'Error','Select Image to process')
        else:
            self.req_img = self.process_img(cv2.imread(self.address.text()))
            cv2.imshow("OutPut",self.req_img)

        #print(self.req_height,self.req_width)

    def process_img(self, imgtoproc):
        if self.Cbas.isChecked():
            cd = ColorDescriptor((8, 12, 3))
            cv2.imwrite('100000.png', imgtoproc)
            query = cv2.imread("100000.png", cv2.IMREAD_COLOR)
            cv2.line(query, (0, 0), (150, 150), (255, 255, 255), 15)
            features = cd.describe(query)
            # print(features);
            # perform the search
            searcher = Searcher("index.csv")
            # print(indexPath)
            results = searcher.search(features)
            for (score, resultID) in results:
                result = cv2.imread(resultID)
                # create blank image - y, x
                # result = np.zeros((600, 1000, 3), np.uint8)
                # setup text
                hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
                height, width, no_channels = result.shape
                font = cv2.FONT_HERSHEY_SIMPLEX
                # img = Image.open('image.png')
                text = "Width=" + str(width) + "Height=" + str(height)
                # get boundary of this text
                textsize = cv2.getTextSize(text, font, 1, 2)[0]
                # get coords based on boundary
                textX = (result.shape[1] - textsize[0]) / 2
                textY = (result.shape[0] + textsize[1]) / 2
                # add text centered on image
                cv2.putText(result, text, (10, 30), font, 1, (255, 255, 255), 2)
                # imgtoproc= result
                cv2.imshow("Result", result)
                cv2.waitKey(0)

            # imgtoproc = cv2.cvtColor(imgtoproc,cv2.COLOR_BGR2GRAY)
        elif self.Hias.isChecked():
            color = ('b', 'g', 'r')
            for i, col in enumerate(color):
                histr = cv2.calcHist([imgtoproc], [i], None, [256], [0, 256])
                plt.plot(histr, color=col)
                plt.xlim([0, 256])
            plt.show()
        elif self.Eias.isChecked():
            edges = cv2.Canny(imgtoproc, 100, 200)
            plt.subplot(121), plt.imshow(imgtoproc, cmap='gray')
            plt.title('Original Image'), plt.xticks([]), plt.yticks([])
            plt.subplot(122), plt.imshow(edges, cmap='gray')
            plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
            # plt.show()
            imgtoproc = edges
        elif self.Grey_scale.isChecked():
            imgtoproc = cv2.cvtColor(imgtoproc,cv2.COLOR_BGR2GRAY)
        elif self.Hsv.isChecked():
            imgtoproc[:, :, 0] = 0
            cv2.imwrite('_no_red.jpg', imgtoproc)
            #imgtoproc[np.where((imgtoproc == [0, 0, 0]).all(axis=2))] = [0, 33, 166]
        return cv2.resize(imgtoproc, (int(self.req_width),int(self.req_height)))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    screen = Img_Proc_Gui()
    screen.show()
    sys.exit(app.exec_())
