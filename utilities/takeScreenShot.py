from subprocess import call
from time import gmtime, strftime
from loguru import logger
from newGame import constants


class Screenshot:

    @staticmethod
    def grab_screen_shot(filename):
        # save screen shots where
        scrfilename = 'screenshot ' + strftime("%d-%m-%Y %H:%M:%S", gmtime())

        fullfile = constants.SCRFILEPATH + scrfilename + '.' + constants.SCRFILEEXTENSION

        logger.info('Screenshot saved to {file}', file=filename)
        call(["screencapture", fullfile])

        # "static/screenshots/screenshot" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ".jpg"]
