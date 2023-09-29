class Parameter:
    def __init__(self, key: str, value: object):
        self.key = key
        self.value = value

    def to_string(self):
        return  f"{self.key}={self.value}"