import os

import javalang


class ASTGenerator(object):
    def __init__(self):
        pass

    def generate(self, filename: str):
        if not os.path.isfile(filename):
            raise FileNotFoundError

        with open(filename, 'r') as file:
            source_code = file.read()
        return javalang.parse.parse(source_code)
