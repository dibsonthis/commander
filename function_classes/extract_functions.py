class ExtractFunctions:
    def __init__(self):
        pass

    def regex(self, data, command_arguments):

        import re

        data_type = 'plain'

        data = data[data_type]

        command_arguments = command_arguments.split(' ')
            
        data_to_extract = command_arguments[0]
        
        extract_list = re.findall(f'{data_to_extract}', data)

        extract_list = '\n'.join(extract_list)

        if not extract_list:
            extract_list = ''
            console_message = f'No matches found for "{data_to_extract}"'
        else:
            console_message = f'Found matches for "{data_to_extract}"'

        result = {'output': extract_list, 'type': data_type, 'console_message': console_message}

        return result

    def extract(self, data, command_arguments):

        import re

        data_type = 'plain'

        data = data[data_type]

        command_arguments = command_arguments.split(' ')

        data_to_extract = command_arguments[0]

        if data_to_extract == 'emails':

            extract_list = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', data)

        elif data_to_extract == 'names':

            extract_list = re.findall(r'([A-Z][a-z]+)', data)

        elif data_to_extract == 'digits':

            extract_list = re.findall(r'[0-9]+', data)

        extract_list = '\n'.join(extract_list)

        if not extract_list:
            extract_list = ''
            console_message = f'No matches found for "{data_to_extract}"'
        else:
            console_message = f'Found matches for "{data_to_extract}"'

        result = {'output': extract_list, 'type': data_type, 'console_message': console_message}

        return result