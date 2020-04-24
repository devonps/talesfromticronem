from subprocess import call
from time import gmtime, strftime
from loguru import logger


class Screenshot:

    @staticmethod
    def grab_screen_shot(filename):
        # save screen shots where
        scrfilename = 'screenshot ' + strftime("%d-%m-%Y %H:%M:%S", gmtime())

        fullfile = '' + scrfilename

        logger.info('Screenshot saved to {file}', file=filename)
        call(["screencapture", fullfile])
