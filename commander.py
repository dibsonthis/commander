import sys
import pyperclip
import pyautogui as pya
from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog, QWidget, QTextEdit)
from PySide2.QtGui import QFont
from function_classes.text_functions import TextFunctions

class MainWindow(QWidget):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('New Window')
        self.resize(1200,1600)

        #Functions
        self.commands = {

                # Basic Text Commands
                'upper'     :   TextFunctions().make_upper,
                '-u'        :   TextFunctions().make_upper,
                'lower'     :   TextFunctions().make_lower,
                '-l'        :   TextFunctions().make_lower,
                # Translation Commands
                'translate' :   TextFunctions().translate,
                '-t'        :   TextFunctions().translate,
                # Information Commands
                'extract'   :   TextFunctions().extract,
                '-e'        :   TextFunctions().extract

        }

        # Fonts
        text_font = QFont('Arial', 16)
        button_font = QFont('Arial', 18)

        # Create widgets
        self.text_area = QTextEdit()
        self.text_area.setFont(text_font)

        self.result_area = QTextEdit()
        self.result_area.setFont(text_font)
        self.result_area.setReadOnly(True)

        self.text_line = QLineEdit()
        self.text_line.setFont(text_font)

        self.button = QPushButton("Execute")
        self.button.setFont(button_font)
        self.button.setStyleSheet('background-color: red; color: white;')
        self.text_line.returnPressed.connect(self.button.click)

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.text_area)
        layout.addWidget(self.result_area)
        layout.addWidget(self.text_line)
        layout.addWidget(self.button)

        # Set dialog layout
        self.setLayout(layout)

        # Add button signal to greetings slot
        self.button.clicked.connect(self.execute_command)

    # Executes command
    def execute_command(self):
        command = self.text_line.text().split(' ')
        command_action = command[0]
        if len(command) == 1:
            command_arguments = []
        else:
            command_arguments = ' '.join(command[1:])

        plain_data = self.text_area.toPlainText()
        html_data = self.text_area.toHtml()
        markdown_data = self.text_area.toMarkdown()

        data = {'plain'     : plain_data, 
                'html'      : html_data,
                'markdown'  : markdown_data}

        if command_action in self.commands:
            function = self.commands[command_action]
            result = function(data, command_arguments)

            self.result_area.clear()

            if result['type'] == 'html':
                self.result_area.insertHtml(result['output'])
            elif result['type'] == 'plain':
                self.result_area.insertPlainText(result['output'])

            # Clears command line
            self.text_line.clear()



if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    window = MainWindow()
    window.show()
    # Run the main Qt loop
    sys.exit(app.exec_())