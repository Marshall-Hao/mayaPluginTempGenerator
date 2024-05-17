import sys
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets


class ValueLadderSection(QtWidgets.QWidget):

    def __init__(self, increment_size, parent=None):
        super(ValueLadderSection, self).__init__(parent)

        self.increment_size = increment_size

        self.setAutoFillBackground(True)
        self.setMinimumHeight(40)

        self.increment_label = QtWidgets.QLabel("{0}".format(self.increment_size))
        self.increment_label.setAlignment(QtCore.Qt.AlignCenter)

        self.value_label = QtWidgets.QLabel("0.0")
        self.value_label.setAlignment(QtCore.Qt.AlignCenter)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.increment_label)
        main_layout.addWidget(self.value_label)

        self.set_active(False)

    def set_active(self, active):
        self.active = active

        pal = self.palette()
        if self.active:
            pal.setColor(QtGui.QPalette.Background, QtCore.Qt.yellow)
        else:
            pal.setColor(QtGui.QPalette.Background, QtCore.Qt.white)

        self.setPalette(pal)

        self.value_label.setVisible(self.active)

    def set_value(self, value):
        self.value_label.setText("{0}".format(value))


class ValueLadder(QtWidgets.QWidget):

    PIXELS_PER_INCREMENT = 20

    value_changed = QtCore.Signal(float)

    def __init__(self, parent=None):
        super(ValueLadder, self).__init__(parent)

        self.active_section = None

        self.initial_value = 0
        self.current_value = 0

        self.x_start = sys.maxsize
        self.multiplier = 0

        self.setMinimumSize(60, 140)
        self.setWindowFlags(QtCore.Qt.Popup)

        pal = self.palette()
        pal.setColor(QtGui.QPalette.Background, QtCore.Qt.black)
        self.setPalette(pal)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.setSpacing(1)

        for increment in [ 1, 0.1, 0.01]:
            main_layout.addWidget(ValueLadderSection(increment))

    def set_position(self, pos):
        self.move(pos.x() - (0.5 * self.width()), pos.y() - (0.5 * self.height()))

    def set_initial_value(self, value):
        self.initial_value = value

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MiddleButton:
            self.close()

    def mouseMoveEvent(self, event):
        pos = event.pos()

        widget_under_mouse = self.childAt(pos)
        if widget_under_mouse:
            self.activate_section(widget_under_mouse)
        else:
            if self.x_start == sys.maxsize:
                self.x_start = pos.x()

            temp_multiplier = int((pos.x() - self.x_start) / ValueLadder.PIXELS_PER_INCREMENT)
            if self.multiplier != temp_multiplier:
                self.multiplier = temp_multiplier

                self.current_value = round(self.initial_value + (self.multiplier * self.active_section.increment_size), 4)
                self.active_section.set_value(self.current_value)

                self.value_changed.emit(self.current_value)

    def activate_section(self, widget_under_mouse):
        if not self.is_value_ladder_section(widget_under_mouse):
            while widget_under_mouse:
                widget_under_mouse = widget_under_mouse.parentWidget()
                if self.is_value_ladder_section(widget_under_mouse):
                    break

        if self.active_section != widget_under_mouse:
            self.current_value = self.initial_value
            self.x_start = sys.maxsize

            if self.active_section:
                self.active_section.set_active(False)

            self.active_section = widget_under_mouse

            if self.active_section:
                self.active_section.set_active(True)
                self.active_section.set_value(self.current_value)

    def is_value_ladder_section(self, widget):
        if type(widget) == ValueLadderSection:
            return True

        return False


class LadderSpinBox(QtWidgets.QDoubleSpinBox):

    def __init__(self, parent=None):
        super(LadderSpinBox, self).__init__(parent)

        self.value_ladder = None

        self.setButtonSymbols(QtWidgets.QDoubleSpinBox.NoButtons)
        self.setMinimum(1.00)
        self.setMaximum(10.99)
        self.setDecimals(2)

        self.lineEdit().installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.lineEdit():
            if event.type() == QtCore.QEvent.MouseButtonPress and event.button() == QtCore.Qt.MiddleButton:
                self.show_ladder(self.mapToGlobal(event.pos()))
                return True

        return super(LadderSpinBox, self).eventFilter(obj, event)

    def show_ladder(self, pos):
        if not self.value_ladder:
            self.value_ladder = ValueLadder()
            self.value_ladder.value_changed.connect(self.setValue)

        self.value_ladder.set_initial_value(self.value())
        self.value_ladder.show()

        self.value_ladder.set_position(pos)

    def textFromValue(self, value):
        text = f"{value:.2f}"
        parts = text.split(".")
        if len(parts) == 2 and len(parts[1]) == 2:
            return f"{parts[0]}.{parts[1][0]}.{parts[1][1]}"
        return text
