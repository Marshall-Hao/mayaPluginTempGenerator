from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

class CustomImageWidget(QtWidgets.QWidget):
    
    def __init__(self,width, height,image_path, parent=None):
        super(CustomImageWidget,self).__init__(parent)
        
        self.set_size(width,height)
        self.set_image(image_path)
        self.set_background_color(QtCore.Qt.black)
        
    def set_size(self,width,height):
        self.setFixedSize(width,height)
    
    def set_image(self,image_path):
        image = QtGui.QImage(image_path)
        image = image.scaled(self.width(), self.height(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        
        self.pixmap = QtGui.QPixmap()
        self.pixmap.convertFromImage(image)
        
        self.update()
        
    def set_background_color(self,color):
        self.background_color = color
        self.update()
        
    def paintEvent(self,event):
        # specify which widget, the self
        painter = QtGui.QPainter(self)
        
        # top left coner coord, then width and height
        painter.fillRect(0,0,self.width(),self.height(),self.background_color)
        
        painter.drawPixmap(self.rect(), self.pixmap)
        
