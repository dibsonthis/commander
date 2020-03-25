class TextFunctions:
    def __init__(self):
        pass

    def html_to_text(self, data):

        import html2text

        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.ignore_emphasis = True
        h.escape_snob = True

        text_only = h.handle(data).split('\n')

        text_only = [x.strip() for x in text_only if x]

        text_only = [x.replace('\\', '') for x in text_only]

        # Reverse the list so that larger blocks of text get replaced before smaller ones
        text_only = sorted(text_only, key=len, reverse=True)

        return text_only

    def translate(self, data, command_arguments):

        data_type = 'plain'

        data = data[data_type]

        command_arguments = command_arguments.split(' ')

        if len(command_arguments) == 1:
            from_lang = 'autodetect'
            to_lang = command_arguments[0]
        elif len(command_arguments) == 2:
            from_lang = command_arguments[0]
            to_lang = command_arguments[1]

        from googletrans import Translator
        translator = Translator()

        if data_type == 'html':

            text_only = self.html_to_text(data)

            replacements = {}

            for text in text_only:
                try:
                    translation = translator.translate(text, src=from_lang, dest=to_lang).text
                    replacements[text] = translation
                except TypeError:
                    pass

            for text, translation in replacements.items():
                data = data.replace(text, translation)

        elif data_type == 'plain':

            data = translator.translate(data, src=from_lang, dest=to_lang).text

        console_message = f'Translated text from {from_lang} to {to_lang}'

        result = {'output': data, 'type': data_type, 'console_message': console_message}

        return result

    def transform(self, data, command_arguments):

        data_type = 'plain'

        data = data[data_type]

        command_arguments = command_arguments.split(' ')

        transformation_command = command_arguments[0]

        if data_type == 'html':

            text_only = self.html_to_text(data)

            replacements = {}

            for text in text_only:

                if transformation_command == 'upper':
                    modified_text = text.upper()
                elif transformation_command == 'lower':
                    modified_text = text.lower()

                replacements[text] = modified_text

            for text, modified_text in replacements.items():  
                data = data.replace(text, modified_text)
        
        elif data_type == 'plain':

            if transformation_command == 'upper':
                data = data.upper()
            elif transformation_command == 'lower':
                data = data.lower()

        console_message = f'Transformed text to {transformation_command}'

        result = {'output': data, 'type': data_type, 'console_message': console_message}

        return result