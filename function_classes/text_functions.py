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

        data_type = 'html'

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

        result = {'output': data, 'type': data_type}

        print(f'Translated text from {from_lang} to {to_lang}')

        return result

    def make_upper(self, data, command_arguments):

        data_type = 'html'

        data = data[data_type]

        if data_type == 'html':

            text_only = self.html_to_text(data)

            replacements = {}

            for text in text_only:
                modified_text = text.upper()
                replacements[text] = modified_text

            for text, modified_text in replacements.items():  
                data = data.replace(text, modified_text)
        
        elif data_type == 'plain':

            data = data.upper()

        result = {'output': data, 'type': data_type}

        print('Made text uppercase')

        return result

    def make_lower(self, data, command_arguments):

        data_type = 'html'

        data = data[data_type]

        if data_type == 'html':

            text_only = self.html_to_text(data)

            replacements = {}

            for text in text_only:
                modified_text = text.lower()
                replacements[text] = modified_text

            for text, modified_text in replacements.items():  
                data = data.replace(text, modified_text)
        
        elif data_type == 'plain':

            data = data.lower()
            
        result = {'output': data, 'type': data_type}

        print('Made text lowercase')

        return result

    def extract(self, data, command_arguments):

            import re

            data_type = 'plain'

            data = data[data_type]

            command_arguments = command_arguments.split(' ')

            data_to_extract = command_arguments[0]

            print(data_to_extract)

            if data_to_extract == 'emails':

                extract_list = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', data)

            extract_list = '\n'.join(extract_list)

            if not extract_list:
                extract_list = f'No {data_to_extract} found'

            result = {'output': extract_list, 'type': data_type}

            return result

    