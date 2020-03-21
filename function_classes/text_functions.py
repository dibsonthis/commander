class TextFunctions:
    def __init__(self):
        pass

    def html_to_text(self, data):

        import html2text

        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.ignore_emphasis = True

        default_tag_replacement = { '<b>'    :  '<strong>',
                                    '</b>'   :  '</strong>'}

        for tag, replacement_tag in default_tag_replacement.items():
            data.replace(tag, replacement_tag)

        text_only = h.handle(data).split('\n')

        text_only = [x.strip() for x in text_only if x]

        return text_only

    def translate(self, data, command_arguments):

        data = data['html']

        command_arguments = command_arguments.split(' ')

        if len(command_arguments) == 1:
            from_lang = 'autodetect'
            to_lang = command_arguments[0]
        elif len(command_arguments) == 2:
            from_lang = command_arguments[0]
            to_lang = command_arguments[1]

        from googletrans import Translator
        translator = Translator()

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

        result = {'output': data, 'type': 'html'}

        print(f'Translated text from {from_lang} to {to_lang}')

        return result

    def make_upper(self, data, command_arguments):

        data = data['html']

        text_only = self.html_to_text(data)

        for text in text_only:
            modified_text = text.upper()
            print(modified_text)
            data = data.replace(text, modified_text)

        result = {'output': data, 'type': 'html'}

        print('Made text uppercase')

        return result

    def make_lower(self, data, command_arguments):

        data = data['html']

        text_only = self.html_to_text(data)

        for text in text_only:
            modified_text = text.lower()
            data = data.replace(text, modified_text)
            
        result = {'output': data, 'type': 'html'}

        print('Made text lowercase')

        return result

    def extract(self, data, command_arguments):

            import re

            data = data['plain']

            command_arguments = command_arguments.split(' ')

            data_to_extract = command_arguments[0]

            print(data_to_extract)

            if data_to_extract == 'emails':

                extract_list = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', data)

            extract_list = '\n'.join(extract_list)

            result = {'output': extract_list, 'type': 'plain'}

            if not extract_list:
                extract_list = f'No {data_to_extract} found'
            else:
                print(f'Extracted {data_to_extract}')

            return result

    