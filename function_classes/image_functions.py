class ImageFunctions:

    def __init__(self):
        pass

    def convert_to_qimage(self, image):

        from PIL import Image
    
        from PySide2.QtGui import QPixmap
        from PySide2.QtWidgets import QLabel
        from PIL.ImageQt import ImageQt

        qim = ImageQt(image)
        pix = QPixmap.fromImage(qim).copy()
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

    def bw(self, data, command_arguments):

        image = data['image']

        from PIL import Image

        image = Image.open(image)
        image = image.convert('1')
        image = self.convert_to_qimage(image)

        console_message = 'Converted image to black and white'
        
        return {'output': image, 'type': 'image', 'console_message': console_message}

    def flip(self, data, command_arguments):

        image = data['image']

        from PIL import Image, ImageOps

        image = Image.open(image)
        image = ImageOps.flip(image)
        image = self.convert_to_qimage(image)

        console_message = 'Flipped Image'
        
        return {'output': image, 'type': 'image', 'console_message': console_message}

    def invert(self, data, command_arguments):

        image = data['image']

        from PIL import Image, ImageOps

        image = Image.open(image)
        image = ImageOps.invert(image)
        image = self.convert_to_qimage(image)

        console_message = 'Inverted Image'
        
        return {'output': image, 'type': 'image', 'console_message': console_message}