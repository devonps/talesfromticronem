
import os.path
import csv

from utilities.common import CommonUtils


class Externalfiles:

    @staticmethod
    def read_prefab_from_csv(filename):
        file_content = Externalfiles.load_existing_file(filename=filename)
        csv_reader = csv.reader(file_content)

        return csv_reader

    @staticmethod
    def create_new_file(filename):
        fileobject = open(filename, 'w')
        return fileobject

    @staticmethod
    def write_to_existing_file(filename, value):
        with open(filename, 'a') as file:
            file.write(value + '\n')

    @staticmethod
    def write_full_game_log(gameworld, log_id):

        filename = "game_log.txt"
        fileobject = Externalfiles.create_new_file(filename)
        stored_msgs = CommonUtils.get_all_log_messages_for_export(gameworld=gameworld, log_entity=log_id)
        for message in stored_msgs:
            Externalfiles.write_to_existing_file(filename, value=message)

        Externalfiles.close_existing_file(fileobject=fileobject)

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
