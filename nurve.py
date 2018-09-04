import os
import sys

import cv2
from PyQt4.QtCore import QStringList, QString
from PyQt4.QtGui import QMainWindow, QApplication, QMessageBox, QTabWidget, QGridLayout, QAction, QFileDialog, \
    QDesktopWidget
from modules.QImageWidget import QImageWidget


class Nurve(QMainWindow):
    def __init__(self, parent= None):
        super(Nurve, self).__init__(parent)
        self.current_images = []
        self.setWindowTitle("Nurve - Alpha 0.0.1")
        self.image_tabs_widget = QTabWidget()
        self.setCentralWidget(self.image_tabs_widget)
        openAction = QAction("&Open Image", self)
        openAction.setShortcut("Ctrl+O")
        openAction.setStatusTip('Open a new image')
        openAction.triggered.connect(self.open_image)

        self.statusBar()

        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu('&File')
        self.fileMenu.addAction(openAction)
        self.menuBar()
        self.screen_size = QDesktopWidget().screenGeometry()

    def open_image(self, checked=False, path=None):
        if path is None:
            dlg = QFileDialog()
            dlg.setFileMode(QFileDialog.ExistingFile)
            dlg.setFilter("Image Files (*.NEF *.TIFF *.TIF)")
            filenames = []
            if dlg.exec_():
                filenames = dlg.selectedFiles()
            if len(filenames) >= 1:
                path = unicode(filenames[0])
            else:
                #TODO: add messagebox
                return

        if os.path.isfile(path):
            filename = os.path.basename(path)
            if path not in self.current_images:
                im = cv2.imread(path, -1)
                widget = QImageWidget()
                visualization = im.copy()
                if visualization .shape[0] > self.screen_size.height():
                    visualization = self.image_resize(visualization , height=self.screen_size.height()-200)
                if visualization .shape[1] > self.screen_size.width():
                    visualization  = self.image_resize(visualization , width=self.screen_size.width()-200)
                widget.set_opencv_image(visualization )
                new_image = {"filename": filename, "path": path, "data":im, "widget": widget}
                self.create_image_tab(new_image)
            else:
                #TODO: Go to tab
                pass
            self.current_images.append(new_image)
            self.statusBar().showMessage("Opened file %s"%filename)
        else:
            mb = QMessageBox("ERROR in path", "Path to file \n%s\ncould not be found."%path,  QMessageBox.Warning, QMessageBox.Ok, 0, 0)
            mb.exec_()

    def image_resize(self, image, width=None, height=None, inter=cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation=inter)
        return resized

    def create_image_tab(self, image_struct):
        self.image_tabs_widget.addTab(image_struct["widget"], QString(image_struct["filename"]))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Nurve()
    window.show()
    sys.exit(app.exec_())