import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image, ImageEnhance
from PyQt5.QtCore import Qt
from PIL.ImageFilter import *


def pil2pixmap(im):
    if im.mode == "RGB":
        r, g, b = im.split()
        im = Image.merge("RGB", (b, g, r))
    elif  im.mode == "RGBA":
        r, g, b, a = im.split()
        im = Image.merge("RGBA", (b, g, r, a))
    elif im.mode == "L":
        im = im.convert("RGBA")
    im2 = im.convert("RGBA")
    data = im2.tobytes("raw", "RGBA")
    qim = QImage(data, im.size[0], im.size[1], QImage.Format_ARGB32)
    pixmap = QPixmap.fromImage(qim)
    return pixmap


folderName = ""

app = QApplication([])
app.setStyleSheet("""
    QWidget {
        background: #DFD3C3;
    }
    QPushButton {
        background: #D0B8A8;
        font-family: comic sans ms;
        font: bold 24px;
        color: black;
    }
    QListWidget {
        background: #D0B8A8;
        font-family: comic sans ms;
        font: bold 20px;
        color: black;
    }
""")
win = QWidget()
win.setWindowTitle("Фото едітор 2к22")
win.resize(1200, 1000)

btnFolder = QPushButton("Папка")
btnLeft = QPushButton("Ліворуч")
btnRight = QPushButton("Праворуч")
btnMirror = QPushButton("Дзеркало")
btnSharpness = QPushButton("Різкість")
btnBlackWhite = QPushButton("Ч/Б")
btnBlur = QPushButton('Блюр')
btnCountour = QPushButton('Контур')
btnSmoothMore = QPushButton('Деталізація')
btnbright = QPushButton('Яскравість')
btnFormat = QPushButton('Формат зображення')
btnSize = QPushButton('Розмір Зображення')
btnMode = QPushButton('Колір Зображення')
btnContrast = QPushButton('Контрасність')
btnColor = QPushButton('Насиченість')
btnEdgeEnhance = QPushButton('Покращення ребер')

photoLabel = QLabel(" ")
photoList = QListWidget()


mainLine = QHBoxLayout()
leftColumn = QVBoxLayout()
rightColumn = QVBoxLayout()


leftColumn.addWidget(btnFolder)
leftColumn.addWidget(photoList)
mainLine.addLayout(leftColumn)

rightColumn.addWidget(photoLabel)
horizontalLine = QHBoxLayout()
horizontalLine1 = QHBoxLayout()
horizontalLine2 = QHBoxLayout()
horizontalLine3 = QHBoxLayout()
horizontalLine1.addWidget(btnBlur)
horizontalLine1.addWidget(btnRight)
horizontalLine1.addWidget(btnSmoothMore)
horizontalLine1.addWidget(btnCountour)
horizontalLine.addWidget(btnLeft)
horizontalLine.addWidget(btnMirror)
horizontalLine.addWidget(btnSharpness)
horizontalLine.addWidget(btnBlackWhite)

horizontalLine2.addWidget(btnEdgeEnhance)
horizontalLine2.addWidget(btnContrast)
horizontalLine2.addWidget(btnColor)
horizontalLine2.addWidget(btnbright)
horizontalLine3.addWidget(btnFormat)
horizontalLine3.addWidget(btnSize)
horizontalLine3.addWidget(btnMode)

rightColumn.addLayout(horizontalLine)
rightColumn.addLayout(horizontalLine1)
rightColumn.addLayout(horizontalLine2)
rightColumn.addLayout(horizontalLine3)
mainLine.addLayout(rightColumn)

win.setLayout(mainLine)

def chooseWorkFolder():
    global folderName
    folderName = QFileDialog.getExistingDirectory()

def showFileNames():
    fileExtension = ["jpg", "png", "jpeg"]

    chooseWorkFolder()
    files = os.listdir(folderName)
    newFile = []
    for file in files:
        ext = file.split(".")
        if len(ext) >= 2:
            ext = ext[1]
            if ext in fileExtension:
                newFile.append(file)

    photoList.clear()
    photoList.addItems(newFile)#новий список)

class ImageEditor:
    def __init__(self):
        self.image = None
        self.folder = None
        self.filename = None

    def loadImage(self):
        imagePath = os.path.join(self.folder, self.filename)
        self.image = Image.open(imagePath)

    def showImage(self):
        pixel = pil2pixmap(self.image)
        pixel = pixel.scaled(400, 400, Qt.KeepAspectRatio)
        photoLabel.setPixmap(pixel)

    def doBlackWhite(self):
        self.image = self.image.convert("L")
        self.showImage()

    def Blur(self):
        self.image = self.image.filter(BLUR)
        self.showImage()

    def Mirir(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.showImage()

    def Detail(self):
        self.image = self.image.filter(DETAIL)
        self.showImage()

    def Flip_Left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.showImage()

    def Flip_Right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.showImage()

    def Countour(self):
        self.image = self.image.filter(CONTOUR)
        self.showImage()
    
    def Sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.showImage()

    def Brightmess (self):
        self.image = ImageEnhance.Brightness(self.image).enhance(1.5)
        self.showImage()

    def showFormat(self):
        msg =  QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Формат зображення " + self.image.format)
        msg.setWindowTitle("Information MessageBox")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()

    def showSize(self):
        msg =  QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Розмір зображення " + self.image.size)
        msg.setWindowTitle("Information MessageBox")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()
        
    def showMode(self):
        msg =  QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Колір зоюраження " + self.image.mode)
        msg.setWindowTitle("Information MessageBox")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()

    def Contrast(self):
        self.image = ImageEnhance.Contrast(self.image).enhance(1.5)
        self.showImage()

    def Color(self):
        self.image = ImageEnhance.Color(self.image).enhance(1.5)
        self.showImage()

    def EdgeEnhance(self):
        self.image = self.image.filter(EDGE_ENHANCE)
        self.showImage()
imageEditor = ImageEditor()

def showChosenImage():
    imageEditor.folder = folderName
    imageEditor.filename = photoList.currentItem().text()
    imageEditor.loadImage()
    imageEditor.showImage()


btnBlackWhite.clicked.connect(imageEditor.doBlackWhite)
btnMirror.clicked.connect(imageEditor.Mirir)
btnBlur.clicked.connect(imageEditor.Blur)
btnRight.clicked.connect(imageEditor.Flip_Right)
btnLeft.clicked.connect(imageEditor.Flip_Left)
btnSmoothMore.clicked.connect(imageEditor.Detail)
btnSharpness.clicked.connect(imageEditor.Sharpen)
btnCountour.clicked.connect(imageEditor.Countour)
btnContrast.clicked.connect(imageEditor.Contrast)
btnColor.clicked.connect(imageEditor.Color)
btnEdgeEnhance.clicked.connect(imageEditor.EdgeEnhance)

btnbright.clicked.connect(imageEditor.Brightmess)
btnFormat.clicked.connect(imageEditor.showFormat)
btnSize.clicked.connect(imageEditor.showSize)
btnMode.clicked.connect(imageEditor.showMode)


btnFolder.clicked.connect(showFileNames)
photoList.currentRowChanged.connect(showChosenImage)
win.show()
app.exec_()
