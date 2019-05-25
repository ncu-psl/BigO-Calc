import javalang


class JavaASTGenerator(object):
    def __init__(self):
        pass

    def generate(self, filename: str):
        with open(filename, 'r') as file:
            source_code = file.read()

        return javalang.parse.parse(source_code)
