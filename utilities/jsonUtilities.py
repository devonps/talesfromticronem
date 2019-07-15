import json


def read_json_file(filename):

    with open(filename) as f:
        data = json.loads(f.read())
        f.close()
        return data


# data is a json object
def write_to_json_file(data, filename):
    with open('filename', 'w') as f:
        json.dump(data, f)
        f.close()


def get_count_of_items(filename, element):
    return len(filename[element])
