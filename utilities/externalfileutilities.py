
import os.path
import csv


class Externalfiles:

    @staticmethod
    def read_prefab_from_csv(filename):
        fileContent = Externalfiles.load_existing_file(filename=filename)
        csvReader = csv.reader(fileContent)

        return csvReader

    @staticmethod
    def create_new_file(filename):
        fileobject = open(filename, 'w')
        return fileobject

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
        filecontent = fileobject.readlines()
        fileobject.close()

        return filecontent

    @staticmethod
    def start_new_game_replay_file(filename):
        if Externalfiles.does_file_exist(filename):
            Externalfiles.delete_existing_file(filename)
        fileobject = Externalfiles.create_new_file(filename)
        return fileobject

    @staticmethod
    def does_file_exist(filename):
        if os.path.exists(filename):
            return True
        else:
            return False

    @staticmethod
    def delete_existing_file(filename):
        os.remove(filename)
