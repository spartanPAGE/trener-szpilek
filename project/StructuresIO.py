import os
from ast import literal_eval

def save_structures(workspace_path, data_dictionary, data_directory="_trener_dane_"):
    dir_path = os.path.join(workspace_path, data_directory)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    for imagename, data in data_dictionary.items():
        with open(os.path.join(dir_path, imagename + ".txt"), "w") as f:
            f.write('{}'.format(data))

def load_structures(workspace_path, data_directory="_trener_dane_"):
    data_dictionary = {}
    dir_path = os.path.join(workspace_path, data_directory)

    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        for path in os.listdir(dir_path):
            with open(os.path.join(dir_path, path), 'r') as f:
                data = literal_eval(f.read())
                data_dictionary[path.replace(".txt", "")] = data
    return data_dictionary
