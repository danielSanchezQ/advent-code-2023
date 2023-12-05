def input_stream(file_name):
    with open(file_name) as f:
        yield from (l.strip() for l in f)


def read_file(file_name):
    with open(file_name) as f:
        return f.read()