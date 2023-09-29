import os.path


def exists(file):
    return os.path.exists(file)


def create(file):
    if not exists(file):
        open(os.path.join(os.getcwd(), file), 'w+').close()


def delete(file):
    if not exists(file):
        return

    os.remove(file)


def append(file, text):
    if not exists(file):
        create(file)

    with open(file, 'a') as f:
        f.write(text + "\n")


def read_lines(file):
    file = open(file, 'r')
    lines = file.readlines()
    return lines


def write(file, text):
    if not exists(file):
        create(file)

    with open(file, 'w') as f:
        f.write(text + "\n")
