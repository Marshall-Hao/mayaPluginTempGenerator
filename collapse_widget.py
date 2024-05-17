from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

def is_running_in_maya():
    try:
        import maya.cmds as cmds
        return True
    except ImportError:
        return False
            
class CollapsibleHeader(QtWidgets.QWidget):
    
  
    
    # set a clicked signal for custom widget
    clicked = QtCore.Signal()
    
    def __init__(self,text,parent=None):
      
        super(CollapsibleHeader,self).__init__(parent)
        
        # for background color fullfill
        self.setAutoFillBackground(True)
        
        self.set_background_color(None)
        self.icon_label = QtWidgets.QLabel()
        
        if is_running_in_maya():
            self.COLLAPSED_PIXMAP = QtGui.QPixmap(":teRightArrow.png")
            self.EXPANDED_PIXMAP = QtGui.QPixmap(":teDownArrow.png")
        else:
            self.COLLAPSED_PIXMAP = QtGui.QPixmap("./util/teRight.png")
            self.EXPANDED_PIXMAP = QtGui.QPixmap("./util/teDown.png")
        
        self.icon_label.setFixedWidth(self.COLLAPSED_PIXMAP.width())
        
        self.text_label = QtWidgets.QLabel()
        # text label does not pass the event to the parent widget, so doest trigger the parent mouseevent
        self.text_label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(4,4,4,4)
        self.main_layout.addWidget(self.icon_label)
        self.main_layout.addWidget(self.text_label)
        
        self.set_text(text)
        self.set_expanded(False)
        
    def set_text(self,text):
        self.text_label.setText(f"<b>{text}</b>")
        
    def set_background_color(self,color):
        if not color:
            color = QtWidgets.QPushButton().palette().color(QtGui.QPalette.Button)
        
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, color)
        self.setPalette(palette)
    
    def is_expanded(self):
        return self._expanded
    
    def set_expanded(self, expanded):
        self._expanded = expanded
        
        if (self._expanded):
            self.icon_label.setPixmap(self.EXPANDED_PIXMAP)
        else:
            self.icon_label.setPixmap(self.COLLAPSED_PIXMAP)
            
    def mouseReleaseEvent(self,event):
        self.clicked.emit() #pylint: disable=E1101
  
  
class CollapsibleWidget(QtWidgets.QWidget):
    
    def __init__(self, text, parent=None):
        super(CollapsibleWidget, self).__init__(parent)
        
        self.header_wdg =  CollapsibleHeader(text)
        self.header_wdg.clicked.connect(self.on_header_clicked)
        
        self.body_wdg = QtWidgets.QWidget()
        
        self.body_layout = QtWidgets.QVBoxLayout(self.body_wdg)
        self.body_layout.setContentsMargins(4,2,4,2)
        self.body_layout.setSpacing(3)
        
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.addWidget(self.header_wdg)
        self.main_layout.addWidget(self.body_wdg)
        
        self.set_expanded(False)
    
    def add_widget(self,widget):
        self.body_layout.addWidget(widget)
        
    def add_layout(self,layout):
        self.body_layout.addLayout(layout)
        
    def set_expanded(self,expanded):
        self.header_wdg.set_expanded(expanded)
        self.body_wdg.setVisible(expanded)
        
    def set_header_background_color(self,color):
        self.header_wdg.set_background_color(color)
        
    def on_header_clicked(self):
        self.set_expanded(not self.header_wdg.is_expanded())
