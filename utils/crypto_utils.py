import os.path


def get_cryptos(file_path):
    cryptos = []
    if not os.path.exists(file_path):
        return cryptos

    file = open(file_path, 'r')
    lines = file.readlines()

    for line in lines:
        if len(line.strip()) > 0:
            cryptos.append(line.replace("\r", "").replace("\n", ""))

    return cryptos

