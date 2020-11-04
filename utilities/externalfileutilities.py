import os
import csv
from pathlib import Path
import pickle


class Externalfiles:

    @staticmethod
    def write_meta_events_to_pickle(filename, meta_events):
        output = open(filename, 'wb')
        pickle.dump(meta_events, output)
        output.close()

    @staticmethod
    def read_meta_events_from_pickle(filename):
        pickle_file = open(filename, 'rb')
        mydict = pickle.load(pickle_file)

        return mydict

    @staticmethod
    def read_prefab_from_csv(filename):
        file_content = Externalfiles.load_existing_file(filename=filename)
        csv_reader = csv.reader(file_content)

        return csv_reader

    @staticmethod
    def new_file(filename):
        Path(filename).touch()

    @staticmethod
    def write_to_existing_file(filename, value):
        with open(filename, 'a') as file:
            file.write(value + '\n')

    @staticmethod
    def close_existing_file(fileobject):
        fileobject.close()

    @staticmethod
    def load_existing_file(filename):
        fileobject = open(filename, 'r')
        fc = fileobject.readlines()
        fileobject.close()
        filecontent = [line.rstrip('\n') for line in fc]

        return filecontent

    @staticmethod
    def start_new_game_replay_file(filename):
        if Externalfiles.does_file_exist(filename):
            Externalfiles.delete_existing_file(filename)
            Externalfiles.new_file(filename=filename)

    @staticmethod
    def does_file_exist(filename):
        if os.path.exists(filename):
            return True
        else:
            return False

    @staticmethod
    def delete_existing_file(filename):
        os.remove(filename)

    @staticmethod
    def create_new_directory(directory_name):
        default_path = './'
        if not Externalfiles.does_file_exist(directory_name):
            path = os.path.join(default_path, directory_name)
            os.mkdir(path=path)