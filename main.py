import sys
import os


from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

from version_spin_box import LadderSpinBox
from image_widget import CustomImageWidget
from collapse_widget import CollapsibleWidget
from suffix_lineedit import SuffixLineEdit


from shiboken2 import wrapInstance

def is_running_in_maya():
    try:
        import maya.cmds as cmds
        return True
    except ImportError:
        return False


# helper get the maya main window pointer and let the dialog parent be it
def maya_main_window():
  import maya.OpenMayaUI as omui
  main_window_ptr = omui.MQtUtil.mainWindow()
  return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

      
class CodeGeneratorWindow(QtWidgets.QWidget):
  
  TYPE_LIST = ["Command", "Node"]
  NODE_LIST = ["PxNode", "PxLocatorNode"]
  COMMAND_LIST = ["PxCommand"]
  
  FILE_FILTERS = "Python (*.py);;Cpp (*.cpp *.h);;All Files (*.*)"
    
  selected_filter = "Python (*.py);;Cpp (*.cpp *.h)"
  
  def __init__(self,parent):
    super(CodeGeneratorWindow, self).__init__(parent)
    if is_running_in_maya():
      self.fold_image_path = ":/fileOpen.png"
    else: 
      self.fold_image_path = "./util/fileOpen.png"
    
    self.script_dir = os.path.dirname(os.path.abspath(__file__))
    self.LOGO_PATH = os.path.join(self.script_dir, "util", "logo.png")
    
    self.setWindowTitle("Maya Plugin Code Generator")
    self.setWindowFlags(QtCore.Qt.WindowType.Window)
    self.setMinimumWidth(400)
    self.create_widgets()
    self.create_logo()
    self.create_collapsible_widget()
    self.create_layouts()
    
    self.create_connections()
    
    self.adjustSize()
    
  def create_widgets(self):
    self.type_cb = QtWidgets.QComboBox()
    self.type_cb.addItem("Select Type")  # Add the placeholder item
    self.type_cb.setCurrentIndex(0)  # Set the placeholder as the default
    self.type_cb.setItemData(0, 0, QtCore.Qt.UserRole - 1)  # Disable the placeholder item
    self.type_cb.addItems(self.TYPE_LIST)
    self.plugin_name_le = SuffixLineEdit("")
    self.plugin_name_le.setPlaceholderText("Enter Plugin Name")
    self.plugin_name_le.setEnabled(False)

    
    self.author_le = QtWidgets.QLineEdit()
    self.author_le.setPlaceholderText("Enter Author Name")
    self.version_sb = LadderSpinBox()
  
    self.python_label = QtWidgets.QLabel("<b>Python:</b>")
    self.python_cb = QtWidgets.QCheckBox()
    self.c_label = QtWidgets.QLabel("<b>C++:</b>")
    self.c_cb = QtWidgets.QCheckBox()
    
    # file path selection
    self.python_file_path_le = QtWidgets.QLineEdit()
    self.python_file_path_le.setVisible(False)
    self.python_select_file_path_btn = QtWidgets.QPushButton()
    self.python_select_file_path_btn.setVisible(False)
    self.python_select_file_path_btn.setIcon(QtGui.QIcon(self.fold_image_path))
    self.python_select_file_path_btn.setToolTip("Select File path for Python file")
    
    
    self.cpp_file_path_le = QtWidgets.QLineEdit()
    self.cpp_file_path_le.setVisible(False)
    self.cpp_select_file_path_btn = QtWidgets.QPushButton()
    self.cpp_select_file_path_btn.setVisible(False)
    self.cpp_select_file_path_btn.setIcon(QtGui.QIcon(self.fold_image_path))
    self.cpp_select_file_path_btn.setToolTip("Select File path for C++ file")
    
    #generation
    self.generate_btn = QtWidgets.QPushButton("Generate")
    self.generate_btn.setEnabled(False)
    
    
  
  def create_logo(self):
    self.logo_widget = CustomImageWidget(66, 66, self.LOGO_PATH)
    self.logo_widget.set_background_color(QtCore.Qt.gray)
    
  def create_collapsible_widget(self):
    self.node_collapsible_widget = CollapsibleWidget("Node")
    self.node_collapsible_widget.set_header_background_color(QtCore.Qt.blue)
    self.node_collapsible_widget.set_expanded(True)
    layout = QtWidgets.QHBoxLayout()
    self.PxNode_rb = QtWidgets.QRadioButton("PxNode")
    self.LocatorNode_rb = QtWidgets.QRadioButton("PxLocatorNode")
    layout.addWidget(self.PxNode_rb)
    layout.addWidget(self.LocatorNode_rb)
    self.node_collapsible_widget.add_layout(layout)
    self.node_collapsible_widget.setVisible(False)
    
    self.command_collapsible_widget = CollapsibleWidget("Command")
    self.command_collapsible_widget.set_header_background_color(QtCore.Qt.gray)
    self.command_collapsible_widget.set_expanded(True)
    layout = QtWidgets.QHBoxLayout()
    self.PxCommand_rb = QtWidgets.QRadioButton("PxCommand")
    layout.addWidget(self.PxCommand_rb)
    self.command_collapsible_widget.add_layout(layout)
    self.command_collapsible_widget.setVisible(False)
    
  def create_layouts(self):
    # logo layout
    self.logo_layout = QtWidgets.QHBoxLayout()
    self.logo_layout.addStretch()
    self.logo_layout.addWidget(self.logo_widget)
    self.logo_layout.addStretch()
    self.logo_layout.setAlignment(QtCore.Qt.AlignCenter)
    
    # basic info layout
    self.basic_info_layout = QtWidgets.QFormLayout()
    self.basic_info_layout.addRow("<b>Type</b>:</b>", self.type_cb)
    self.basic_info_layout.addRow("<b>Plugin Name:</b>", self.plugin_name_le)
    self.basic_info_layout.addRow("<b>Author:</b>", self.author_le)
    self.basic_info_layout.addRow("<b>Version:</b>", self.version_sb)
    
    #python language layout
    self.python_language_layout = QtWidgets.QVBoxLayout()
    self.python_language_layout.setAlignment(QtCore.Qt.AlignLeft)

    self.python_layout = QtWidgets.QHBoxLayout()
    self.python_layout.setAlignment(QtCore.Qt.AlignLeft)
    self.python_layout.addWidget(self.python_label)
    self.python_layout.addWidget(self.python_cb)
    
    #$ file path layout
    self.python_file_path_layout = QtWidgets.QHBoxLayout()
    self.python_file_path_layout.addWidget(self.python_file_path_le)
    self.python_file_path_layout.addWidget(self.python_select_file_path_btn)
    
    self.python_language_layout.addLayout(self.python_layout)
    self.python_language_layout.addLayout(self.python_file_path_layout)
    #cpp language layout
    self.cpp_language_layout = QtWidgets.QVBoxLayout()
    self.cpp_language_layout.setAlignment(QtCore.Qt.AlignLeft)
    self.cpp_layout = QtWidgets.QHBoxLayout()
    self.cpp_layout.setAlignment(QtCore.Qt.AlignLeft)
    self.cpp_layout.addWidget(self.c_label)
    self.cpp_layout.addWidget(self.c_cb)
    self.cpp_file_path_layout = QtWidgets.QHBoxLayout()
    self.cpp_file_path_layout.addWidget(self.cpp_file_path_le)
    self.cpp_file_path_layout.addWidget(self.cpp_select_file_path_btn)
    self.cpp_language_layout.addLayout(self.cpp_layout)
    self.cpp_language_layout.addLayout(self.cpp_file_path_layout)
    
    
    
    # confirm layout
    self.confirm_layout = QtWidgets.QHBoxLayout()
    self.confirm_layout.addStretch()
    self.confirm_layout.addWidget(self.generate_btn)
    
    # main layout
    main_layout = QtWidgets.QVBoxLayout(self)
    main_layout.setContentsMargins(4,10,4,2)
    main_layout.setAlignment(QtCore.Qt.AlignTop)
    main_layout.addLayout(self.logo_layout)
    main_layout.addLayout(self.basic_info_layout)
    main_layout.addWidget(self.node_collapsible_widget)
    main_layout.addWidget(self.command_collapsible_widget)
    main_layout.setSpacing(10)
    main_layout.addLayout(self.python_language_layout)
    main_layout.addLayout(self.cpp_language_layout)
    main_layout.setSpacing(16)
    main_layout.addLayout(self.confirm_layout)
     
  
  def create_connections(self):
    # check the generate state
    self.type_cb.currentIndexChanged.connect(self.enable_generate)
    self.plugin_name_le.textChanged.connect(self.enable_generate)
    self.author_le.textChanged.connect(self.enable_generate)
    self.version_sb.valueChanged.connect(self.enable_generate)
    self.python_cb.stateChanged.connect(self.enable_generate)
    self.c_cb.stateChanged.connect(self.enable_generate)
    self.PxNode_rb.toggled.connect(self.enable_generate)
    self.LocatorNode_rb.toggled.connect(self.enable_generate)
    self.PxCommand_rb.toggled.connect(self.enable_generate)
    self.python_file_path_le.textChanged.connect(self.enable_generate)
    self.cpp_file_path_le.textChanged.connect(self.enable_generate)  
    
    self.type_cb.currentIndexChanged.connect(self.show_details_type)
    self.generate_btn.clicked.connect(self.generate_plugin)
    
    self.python_cb.stateChanged.connect(self.show_python_file_select_dialog)
    self.c_cb.stateChanged.connect(self.show_cpp_file_select_dialog)  
    
    self.python_select_file_path_btn.clicked.connect(self.python_show_file_select_dialog)
    self.cpp_select_file_path_btn.clicked.connect(self.cpp_show_file_select_dialog) 
    
  def enable_generate(self):
    if self.type_cb.currentIndex() > 0 and self.plugin_name_le.text() and self.author_le.text() and self.version_sb.value() > 0 and (self.python_cb.isChecked() or self.c_cb.isChecked()) and (self.PxNode_rb.isChecked() or self.LocatorNode_rb.isChecked() or self.PxCommand_rb.isChecked()) and (self.python_file_path_le.text() or self.cpp_file_path_le.text()):
      self.generate_btn.setEnabled(True)
    else:
      self.generate_btn.setEnabled(False)
  
  def show_details_type(self,value):
    self.plugin_name_le.clear()
    self.plugin_name_le.setSuffix("")
    self.plugin_name_le.setEnabled(True)
    if value == 1:
      self.node_collapsible_widget.setVisible(False)
      self.command_collapsible_widget.setVisible(True)
      self.plugin_name_le.setSuffix("Command")
    elif value == 2:
      self.node_collapsible_widget.setVisible(True)
      self.command_collapsible_widget.setVisible(False)
      self.plugin_name_le.setSuffix("Node")
  
  def show_python_file_select_dialog(self,checked):
    if checked:
      self.python_file_path_le.setVisible(True)
      self.python_select_file_path_btn.setVisible(True)
    else:
      self.python_file_path_le.setVisible(False)
      self.python_select_file_path_btn.setVisible(False)
      
  def show_cpp_file_select_dialog(self,checked):
    if checked:
      self.cpp_file_path_le.setVisible(True)
      self.cpp_select_file_path_btn.setVisible(True)
    else:
      self.cpp_file_path_le.setVisible(False)
      self.cpp_select_file_path_btn.setVisible(False)
  
  def python_show_file_select_dialog(self):
    
        file_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select File", " ")
        if file_path:
            self.python_file_path_le.setText(file_path)
  
  def cpp_show_file_select_dialog(self):
        file_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select File", " ")
        if file_path:
            self.cpp_file_path_le.setText(file_path)
  
  def generate_plugin(self):
    type_index = self.type_cb.currentIndex()
    type_name = self.type_cb.currentText()  
    plugin_name = self.plugin_name_le.text()
    author = self.author_le.text()
    version = self.version_sb.text()
    
    if type_index == 1:
      detail_name = self.PxCommand_rb.text()
    elif type_index == 2:
      if self.PxNode_rb.isChecked():
        detail_name = self.PxNode_rb.text() 
      elif self.LocatorNode_rb.isChecked():
        detail_name = self.LocatorNode_rb.text()
    try:
      if self.python_cb.isChecked():
        python_template_path = os.path.join(self.script_dir, "template", detail_name, "python", "template.py")
        python_template_content = self.load_template(python_template_path)
        python_new_content = self.config_template(python_template_content, plugin_name, author, version, detail_name)
        create_file_path = self.python_file_path_le.text()
        self.create_plugin(create_file_path, f"{plugin_name}{type_name}.py", python_new_content)
      
      if self.c_cb.isChecked():
        c_source_template_path = os.path.join(self.script_dir, "template", detail_name, "cpp", "template.cpp")
        c_header_template_path = os.path.join(self.script_dir, "template", detail_name, "cpp", "template.h")
        c_main_template_path = os.path.join(self.script_dir, "template", detail_name, "cpp", "main.cpp")
        
        c_source_template_content = self.load_template(c_source_template_path)
        c_header_template_content = self.load_template(c_header_template_path)
        c_main_template_content = self.load_template(c_main_template_path)
        
        c_source_new_content = self.config_template(c_source_template_content, plugin_name, author, version, detail_name)
        c_header_new_content = self.config_template(c_header_template_content, plugin_name, author, version, detail_name)
        c_main_new_content = self.config_template(c_main_template_content, plugin_name, author, version, detail_name)
        
        c_create_file_path = f"{self.cpp_file_path_le.text()}/{plugin_name}Node"
        self.create_plugin(c_create_file_path, f"{plugin_name}{type_name}.cpp", c_source_new_content)
        self.create_plugin(c_create_file_path, f"{plugin_name}{type_name}.h", c_header_new_content)
        self.create_plugin(c_create_file_path, "main.cpp", c_main_new_content)  
      
      QtWidgets.QMessageBox.information(self, "Success", "Plugin generated successfully")
     
    except Exception as e:
        QtWidgets.QMessageBox.critical(self, "Error", "An error occurred while generating the plugin" + str(e))

  def load_template(self,file_path):
        with open(file_path, "r") as file:
            return file.read()
    
  def config_template(self,template, plugin_name, author, version, detail_name):
        template = template.replace("{{plugin_name}}", plugin_name)
        template = template.replace("{{author}}", author)
        template = template.replace("{{version}}", version)
        template = template.replace("{{detail_name}}", detail_name)
        return template
      
  def create_plugin(self,file_path, file_name, content):
        os.makedirs(file_path, exist_ok=True)
        
        # Write the content to the file
        with open(os.path.join(file_path, file_name), "w") as file:
            file.write(content)
    
      
if __name__ == "__main__":
  if is_running_in_maya():
      try:
          code_generator.close() # pylint: disable=E0601
          code_generator.deleteLater() # pylint: disable=E0601
      except:
          pass
      code_generator = CodeGeneratorWindow(maya_main_window())
      code_generator.show()
  else:
    app = QtWidgets.QApplication(sys.argv)
    code_generator = CodeGeneratorWindow(None)
    code_generator.show()
    sys.exit(app.exec_())      
    
    