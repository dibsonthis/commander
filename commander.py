import sys
import pyperclip
import pyautogui as pya
from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QGridLayout, QListWidget, QListWidgetItem, QDialog, QWidget, QTextEdit, QFrame, QScrollArea, QMainWindow, QTabWidget, QFileDialog, QLabel)
from PySide2.QtGui import QFont, QTextCursor, QPixmap

from function_classes.text_functions import TextFunctions
from function_classes.extract_functions import ExtractFunctions
from function_classes.image_functions import ImageFunctions

class MainWindow(QWidget):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Commander V 0.1')
        self.resize(1600,1200)

        #Functions
        self.commands = {

                # GUI commands
                'CLEARALL'    :   self.clear_all_results,
                # Basic Text Commands
                'transform'   :   TextFunctions().transform,
                '-tf'         :   TextFunctions().transform,
                # Translation Commands
                'translate'   :   TextFunctions().translate,
                '-tr'         :   TextFunctions().translate,
                # Information Commands
                'extract'     :   ExtractFunctions().extract,
                '-ext'        :   ExtractFunctions().extract,
                'regex'       :   ExtractFunctions().regex,
                '-re'         :   ExtractFunctions().regex,
                # Image Functions
                'grayscale'   :   ImageFunctions().grayscale,
                'bw'          :   ImageFunctions().bw,
                'flip'        :   ImageFunctions().flip,
                'invert'      :   ImageFunctions().invert

        }

        # Fonts
        self.text_font = QFont('monospace', 16)
        self.button_font = QFont('monospace', 18)
        self.console_font = QFont('monospace', 14)

        # Create widgets

        self.input_area = QTabWidget()
        self.input_area.setFont(self.text_font)

        self.text_area = QTextEdit()
        self.text_area.setFont(self.text_font)

        self.file_area = FileArea()
        
        self.image_area = ImageArea()

        self.result_scroll_area = QScrollArea()

        self.result_area = QWidget()
        self.result_area.layout = QVBoxLayout()
        self.result_area.setLayout(self.result_area.layout)

        self.result_scroll_area.setWidget(self.result_area)
        self.result_scroll_area.setWidgetResizable(True)

        self.console = QTextEdit()
        self.console.setMaximumHeight(300)
        self.console.setReadOnly(True)
        self.console.setStyleSheet('background-color: #0F0E0D; color: white; border: 0;')
        self.console.setFont(self.console_font)

        def set_command_line_focus(event):
            self.command_line.setFocus()

        self.console.mousePressEvent = set_command_line_focus

        self.command_line = QLineEdit()
        # self.command_line.setStyleSheet('background-color: #0F0E0D; color: white; border: 0;')
        self.command_line.setFont(self.console_font)
        self.command_line.setPlaceholderText('Enter command')
        self.command_line.setTextMargins(5,0,0,0)

        self.execute_button = QPushButton("Execute")
        self.execute_button.setFont(self.button_font)
        self.execute_button.setStyleSheet('background-color: red; color: white;')
        self.command_line.returnPressed.connect(self.execute_button.click)
        self.execute_button.setVisible(False)

        # Create layout and add widgets
        self.layout = QGridLayout()

        self.top_layout = QGridLayout()

        # Tabbed input area
        self.top_layout.addWidget(self.input_area,0,0)
        self.input_area.insertTab(0, self.text_area, 'Text')
        self.input_area.insertTab(1, self.file_area, 'File')
        self.input_area.insertTab(2, self.image_area, 'Image')

        self.top_layout.addWidget(self.result_scroll_area,0,2)

        self.bottom_layout = QGridLayout()
        self.bottom_layout.setSpacing(0)

        self.bottom_layout.addWidget(self.console,0,0)
        self.bottom_layout.addWidget(self.command_line,1,0)
        self.bottom_layout.addWidget(self.execute_button,2,0)

        # Set layout
        self.setLayout(self.layout)
        self.layout.addLayout(self.top_layout,0,0)
        self.layout.addLayout(self.bottom_layout,1,0)

        # Add button signal to execution function
        self.execute_button.clicked.connect(self.execute_command)

        # Set focus to command line
        self.command_line.setFocus()

    def clear_all_results(self, *args, **kwargs):
        for i in reversed(range(self.result_area.layout.count())): 
            self.result_area.layout.itemAt(i).widget().setParent(None)

    # Executes command
    def execute_command(self):

        command = self.command_line.text().split(' ')
        command_action = command[0]

        if len(command) == 1:
            command_arguments = []
        else:
            command_arguments = ' '.join(command[1:])

        if self.input_area.currentIndex() == 0:
            data_input = self.text_area
        elif self.input_area.currentIndex() == 1:
            data_input = self.file_area.file_preview
        elif self.input_area.currentIndex() == 2:
            data_input = self.image_area.selected_file_name.text()

        # Data Types:
        if self.input_area.currentIndex() == 0 or self.input_area.currentIndex() == 1:
            plain_data = data_input.toPlainText()
            html_data = data_input.toHtml()
            markdown_data = data_input.toMarkdown()

            data = {'plain'     : plain_data, 
                    'html'      : html_data,
                    'markdown'  : markdown_data}

        elif self.input_area.currentIndex() == 2:
            image_data = data_input

            data = {'image' : image_data}

        if command_action in self.commands:

            function = self.commands[command_action]
            result = function(data, command_arguments)

            # Check to see if function returns a result, then sets variables
            if result:
                result_output = result['output']
                result_data_type = result['type']
                result_console_message = result['console_message']

            command_print = QLineEdit(self.command_line.text())
            command_print.setFont(self.console_font)
            command_print.setReadOnly(True)

            # Clears command line
            self.command_line.clear()

            # Inserts the command and the result as widgets
            if result_output:
                self.result_area.layout.addWidget(command_print)
                result_block = ResultBlock(result_output, result_data_type)
                self.result_area.layout.addWidget(result_block)

            # Make sure scrollbar is always at the bottom
            scroll_bar = self.result_scroll_area.verticalScrollBar()
            scroll_bar.rangeChanged.connect( lambda x,y: scroll_bar.setValue(y))

            # Inserts console_message to console
            if result_console_message:
                self.console.append(result['console_message'])

class ResultBlock(QWidget):

    def __init__(self, result, type, parent=None):
        super(ResultBlock, self).__init__(parent)
        self.result = result

        self.text_font = QFont('monospace', 16)

        if type == 'plain':
            self.result_block = QTextEdit()
            self.result_block.setFont(self.text_font)
            self.result_block.insertPlainText(result)
            self.result_block.setMinimumHeight(600)

            # Make sure scrollbar is always at the top
            self.result_block.moveCursor(QTextCursor().Start)
            self.result_block.ensureCursorVisible()

            self.result_block.setReadOnly(True)

        elif type == 'html':
            self.result_block = QTextEdit()
            self.result_block.setFont(self.text_font)
            self.result_block.insertHtml(result)
            self.result_block.setMinimumHeight(600)

            # Make sure scrollbar is always at the top
            self.result_block.moveCursor(QTextCursor().Start)
            self.result_block.ensureCursorVisible()

            self.result_block.setReadOnly(True)

        elif type == 'image':
            self.result_block = QScrollArea()

            self.image_preview = QWidget()
            image_preview_layout = QVBoxLayout()
            image_preview_layout.addWidget(result)
            print(result)
            self.image_preview.setLayout(image_preview_layout)

            self.result_block.setWidget(self.image_preview)
            self.result_block.setWidgetResizable(True)
            self.result_block.setMinimumHeight(600)

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.result_block)

        # Set layout
        self.setLayout(layout)

class FileArea(QWidget):
    def __init__(self, parent=None):
        super(FileArea, self).__init__(parent)

        # Fonts
        self.text_font = QFont('monospace', 16)
        self.button_font = QFont('monospace', 18)
        self.selected_file_name_font = QFont('monospace', 10)

        self.file_selection_button = QPushButton('Select File')
        self.file_selection_button.setFont(self.button_font)
        self.file_selection_button.clicked.connect(self.open_file)

        self.selected_file_name = QLineEdit()
        self.selected_file_name.setReadOnly(True)
        self.selected_file_name.setFont(self.selected_file_name_font)

        self.file_preview = QTextEdit()
        self.file_preview.setReadOnly(True)
        self.file_preview.setFont(self.text_font)

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.file_selection_button)
        layout.addWidget(self.selected_file_name)
        layout.addWidget(self.file_preview)

        # Set layout
        self.setLayout(layout)

    def get_file_path(self):
        file_path = QFileDialog.getOpenFileNames(filter="Text files (*.txt);;XML files (*.xml);;CSV files (*.csv);;Word files (*.doc *.docx)")
        file_path = file_path[0][0]
        self.selected_file_name.setText(file_path)
        return file_path

    def get_file_contents(self, file_path):
        with open(file_path, 'r', encoding="utf8") as file:
            file_contents = file.read()

        self.file_preview.insertPlainText(file_contents)
        return file_contents

    def open_file(self):
        self.file_preview.clear()
        self.selected_file_name.clear()
        file_path = self.get_file_path()
        file_contents = self.get_file_contents(file_path)
        return file_contents

class ImageArea(QWidget):
    def __init__(self, parent=None):
        super(ImageArea, self).__init__(parent)

        self.image = None

        # Fonts
        self.text_font = QFont('monospace', 16)
        self.button_font = QFont('monospace', 18)
        self.selected_file_name_font = QFont('monospace', 10)

        self.file_selection_button = QPushButton('Select Image')
        self.file_selection_button.setFont(self.button_font)
        self.file_selection_button.clicked.connect(self.open_file)

        self.selected_file_name = QLineEdit()
        self.selected_file_name.setReadOnly(True)
        self.selected_file_name.setFont(self.selected_file_name_font)

        self.image_preview_container = QScrollArea()


        self.image_preview = QWidget()
        image_preview_layout = QVBoxLayout()
        self.image_preview.setLayout(image_preview_layout)

        self.image_preview_container.setWidget(self.image_preview)
        self.image_preview_container.setWidgetResizable(True)

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.file_selection_button)
        layout.addWidget(self.selected_file_name)
        layout.addWidget(self.image_preview_container)

        # Set layout
        self.setLayout(layout)

    def get_file_path(self):
        file_path = QFileDialog.getOpenFileNames(filter="Images (*.png *.xpm *.jpg *.jpeg)")
        file_path = file_path[0][0]
        self.selected_file_name.setText(file_path)
        return file_path

    def get_file_contents(self, file_path):

        pixmap = QPixmap(file_path)
        label = QLabel('', self)
        label.setPixmap(pixmap)
        
        return label

    def open_file(self):
        # self.file_preview.clear()
        self.clear_image()
        self.selected_file_name.clear()
        file_path = self.get_file_path()
        file_contents = self.get_file_contents(file_path)
        self.image_preview.layout().addWidget(file_contents)

        self.image = file_path
        
        return file_contents

    def clear_image(self):
        for i in reversed(range(self.image_preview.layout().count())): 
            self.image_preview.layout().itemAt(i).widget().setParent(None)


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show window
    window = MainWindow()
    window.show()
    # Run the main Qt loop
    sys.exit(app.exec_())