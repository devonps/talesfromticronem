from subprocess import call
from time import gmtime, strftime
from loguru import logger


class Screenshot:

    @staticmethod
    def grab_screen_shot(filename):
        # save screen shots where
        scrfilepath = 'static/screenshots/'
        scrfilename = 'screenshot ' + strftime("%d-%m-%Y %H:%M:%S", gmtime())
        scrfileextension = 'jpg'
        fullfile = scrfilepath + scrfilename + '.' + scrfileextension

        logger.info('Screenshot saved to {file}', file=filename)
        call(["screencapture", fullfile])

        # "static/screenshots/screenshot" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ".jpg"]
