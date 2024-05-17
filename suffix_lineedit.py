from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

class SuffixLineEdit(QtWidgets.QLineEdit):
    def __init__(self, suffix, parent=None):
        super().__init__(parent)
        self.suffix = suffix
        
        self.textChanged.connect(self.ensure_suffix)

        # Initially set the text to just the suffix
        self.setText(self.suffix)
        
        # Temporarily block signals to avoid triggering textChanged event
        self.blockSignals(True)
        self.setCursorPosition(0)
        self.blockSignals(False)

    def ensure_suffix(self):
        current_text = super().text()
        
        # Ensure the text always ends with the suffix
        if not current_text.endswith(self.suffix):
            if self.suffix in current_text:
                current_text = current_text.replace(self.suffix, '')
            self.blockSignals(True)  # Temporarily block signals to avoid recursive calls
            self.setText(current_text + self.suffix)
            self.setCursorPosition(len(current_text))  # Set cursor position before suffix
            self.blockSignals(False)
            
    def text(self):
        current_text = super().text()
        if current_text.endswith(self.suffix):
            return current_text[:-len(self.suffix)]
        return current_text
    
    def keyPressEvent(self, event):
        if event.key() in [QtCore.Qt.Key_Right, QtCore.Qt.Key_Backspace]:
            current_text = super().text()
            cursor_pos = self.cursorPosition()
            suffix_start = len(current_text) - len(self.suffix)
            if cursor_pos <= suffix_start:
                super().keyPressEvent(event)
            return
        super().keyPressEvent(event)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.correct_cursor_position()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.correct_cursor_position()

    def correct_cursor_position(self):
        current_text = super().text()
        cursor_pos = self.cursorPosition()
        suffix_start = len(current_text) - len(self.suffix)
        if cursor_pos > suffix_start:
            self.setCursorPosition(suffix_start)

    def setSuffix(self, suffix):
        self.suffix = suffix
        super().setText("")
        self.ensure_suffix()