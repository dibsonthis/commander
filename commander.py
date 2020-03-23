import sys
import pyperclip
import pyautogui as pya
from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QGridLayout, QListWidget, QListWidgetItem, QDialog, QWidget, QTextEdit, QFrame, QScrollArea)
from PySide2.QtGui import QFont, QTextCursor
from function_classes.text_functions import TextFunctions

class MainWindow(QWidget):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Commander V 0.1')
        self.resize(1600,1200)

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
        text_font = QFont('monospace', 16)
        button_font = QFont('monospace', 18)

        # Create widgets
        self.text_area = QTextEdit()
        self.text_area.setFont(text_font)

        self.result_scroll_area = QScrollArea()

        self.result_area = QWidget()
        self.result_area.layout = QVBoxLayout()
        self.result_area.setLayout(self.result_area.layout)

        self.result_scroll_area.setWidget(self.result_area)
        self.result_scroll_area.setWidgetResizable(True)

        self.text_line = QLineEdit()
        self.text_line.setFont(text_font)

        self.execute_button = QPushButton("Execute")
        self.execute_button.setFont(button_font)
        self.execute_button.setStyleSheet('background-color: red; color: white;')
        self.text_line.returnPressed.connect(self.execute_button.click)

        # Create layout and add widgets
        self.layout = QGridLayout()
        self.layout.addWidget(self.text_area,0,0)
        self.layout.addWidget(self.result_scroll_area,0,1)
        self.layout.addWidget(self.text_line,1,0)
        self.layout.addWidget(self.execute_button,1,1)

        # Set layout
        self.setLayout(self.layout)

        # Add button signal to execution function
        self.execute_button.clicked.connect(self.execute_command)

    # Executes command
    def execute_command(self):

        command = self.text_line.text().split(' ')
        command_action = command[0]
        if len(command) == 1:
            command_arguments = []
        else:
            command_arguments = ' '.join(command[1:])

        # Data Types
        plain_data = self.text_area.toPlainText()
        html_data = self.text_area.toHtml()
        markdown_data = self.text_area.toMarkdown()

        data = {'plain'     : plain_data, 
                'html'      : html_data,
                'markdown'  : markdown_data}

        if command_action in self.commands:

            function = self.commands[command_action]
            result = function(data, command_arguments)

            command_print = QLineEdit(self.text_line.text())
            command_print.setReadOnly(True)

            # Inserts the command and the result as widgets
            self.result_area.layout.addWidget(command_print)
            result_block = ResultBlock(result['output'], result['type'])
            self.result_area.layout.addWidget(result_block)

            # Make sure scrollbar is always at the bottom
            scroll_bar = self.result_scroll_area.verticalScrollBar()
            scroll_bar.rangeChanged.connect( lambda x,y: scroll_bar.setValue(y))

            # Clears command line
            self.text_line.clear()

class ResultBlock(QWidget):

    def __init__(self, result, type, parent=None):
        super(ResultBlock, self).__init__(parent)
        self.result = result

        text_font = QFont('monospace', 16)

        if type == 'plain':
            self.result_block = QTextEdit()
            self.result_block.setFont(text_font)
            self.result_block.insertPlainText(result)
            self.result_block.setMinimumHeight(600)
        elif type == 'html':
            self.result_block = QTextEdit()
            self.result_block.setFont(text_font)
            self.result_block.insertHtml(result)
            self.result_block.setMinimumHeight(600)

        # Make sure scrollbar is always at the bottom
        self.result_block.moveCursor(QTextCursor().Start)
        self.result_block.ensureCursorVisible()

        self.result_block.setReadOnly(True)

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.result_block)

        # Set layout
        self.setLayout(layout)


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    window = MainWindow()
    window.show()
    # Run the main Qt loop
    sys.exit(app.exec_())