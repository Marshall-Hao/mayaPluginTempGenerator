import sys
import os
import unittest
from PySide2 import QtWidgets, QtCore
from PySide2.QtTest import QTest
# Adjust the path to include the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import CodeGeneratorWindow, is_running_in_maya

class TestCodeGeneratorWindow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not is_running_in_maya():
            cls.app = QtWidgets.QApplication(sys.argv)
        else:
            cls.app = None

    @classmethod
    def tearDownClass(cls):
        if cls.app:
            cls.app.quit()

    def setUp(self):
        self.widget = CodeGeneratorWindow(None)
        self.widget.show()

    def tearDown(self):
        self.widget.close()
        self.widget.deleteLater()

    def test_initial_state(self):
        self.assertEqual(self.widget.type_cb.currentIndex(), 0)
        self.assertFalse(self.widget.plugin_name_le.isEnabled())
        self.assertFalse(self.widget.generate_btn.isEnabled())

    def test_enable_generate(self):
        self.widget.type_cb.setCurrentIndex(1)  # Select "Command"
        self.widget.plugin_name_le.setText("TestPlugin")
        self.widget.author_le.setText("Author")
        self.widget.version_sb.setValue(1.0)
        self.widget.python_cb.setChecked(True)
        self.widget.PxCommand_rb.setChecked(True)
        self.widget.python_file_path_le.setText(os.path.dirname(os.path.abspath(__file__)))

        self.assertTrue(self.widget.generate_btn.isEnabled())

    def test_show_details_type(self):
        self.widget.type_cb.setCurrentIndex(1)  # Select "Command"
        self.assertTrue(self.widget.command_collapsible_widget.isVisible())
        self.assertFalse(self.widget.node_collapsible_widget.isVisible())
        self.assertEqual(self.widget.plugin_name_le.text(), "")

        self.widget.type_cb.setCurrentIndex(2)  # Select "Node"
        self.assertFalse(self.widget.command_collapsible_widget.isVisible())
        self.assertTrue(self.widget.node_collapsible_widget.isVisible())
        self.assertEqual(self.widget.plugin_name_le.text(), "")

    def test_generate_plugin(self):
        self.widget.type_cb.setCurrentIndex(1)  # Select "Command"
        self.widget.plugin_name_le.setText("TestPlugin")
        self.widget.author_le.setText("Author")
        self.widget.version_sb.setValue(1.0)
        self.widget.python_cb.setChecked(True)
        self.widget.PxCommand_rb.setChecked(True)
        self.widget.python_file_path_le.setText(os.path.dirname(os.path.abspath(__file__)))

        QTest.mouseClick(self.widget.generate_btn, QtCore.Qt.LeftButton)

        # Check if the file was created (example for a test environment)
        expected_path = os.path.join("/tmp", "TestPluginCommand.py")
        self.assertTrue(os.path.exists(expected_path))
        with open(expected_path, 'r') as file:
            content = file.read()
            self.assertIn("TestPlugin", content)
            self.assertIn("Author", content)

if __name__ == "__main__":
    unittest.main()