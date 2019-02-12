
class Externalfiles:

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

