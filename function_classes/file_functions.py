class FileFunctions:

    def __init__(self):
        pass

    def convert_to_qimage(self, image):
    
        from PySide2.QtGui import QPixmap
        from PySide2.QtWidgets import QLabel
        from PIL.ImageQt import ImageQt

        qim = ImageQt(image)
        pix = QPixmap.fromImage(qim)
        result_label = QLabel('')
        result_label.setPixmap(pix)

        return result_label

    def grayscale(self, data, command_arguments):

        image = data['image']

        from PIL import Image

        image = Image.open(image)
        image = image.convert('L')
        image = self.convert_to_qimage(image)

        console_message = 'Converted image to grayscale'
        
        return {'output': image, 'type': 'image', 'console_message': console_message}