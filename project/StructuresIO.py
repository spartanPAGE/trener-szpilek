import os

from PyQt5.QtWidgets import QMessageBox

from ast import literal_eval

def save_structures(workspace_path, data_dictionary, data_directory="_trener_dane_"):
    dir_path = os.path.join(workspace_path, data_directory)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    for imagename, data in data_dictionary.items():
        with open(os.path.join(dir_path, imagename + ".txt"), "w", encoding="utf-8") as f:
            f.write('{}'.format(data))

def load_structures(workspace_path="", data_directory="_trener_dane_"):
    def show_error_messagebox():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText('Dane trenera zakodowane są w nieznany sposób. Spróbuj zamienić je na UTF-8 i spróbuj ponownie')
        msg.setWindowTitle("Błąd odczytu")
        msg.exec_()

    data_dictionary = {}

    if workspace_path:
        dir_path = os.path.join(workspace_path, data_directory)
    else:
        dir_path = data_directory

    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        for path in os.listdir(dir_path):
            try:
                with open(os.path.join(dir_path, path), 'r', encoding='utf-8') as f:
                    data_dictionary[path.replace(".txt", "")] = literal_eval(f.read())
            except UnicodeDecodeError:
                try:
                    with open(os.path.join(dir_path, path), 'r', encoding='windows-1250') as f:
                        data_dictionary[path.replace(".txt", "")] = literal_eval(f.read())
                except UnicodeDecodeError:
                    show_error_messagebox()
                    break
    return data_dictionary
