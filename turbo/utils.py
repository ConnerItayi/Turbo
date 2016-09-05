import logging
import sys
import os
import colorlog
import configparser

class Logging:
    """
    Configures and sets up logging modules
    """
    def __init__(self, filename):
        self.lg = logging.getLogger(__name__)
        self.lg.setLevel(logging.DEBUG)
        self.fh = logging.FileHandler(filename=filename, encoding='utf-8', mode='w')
        self.fh.setFormatter(logging.Formatter(
                "[{asctime}] {levelname} ({filename} L{lineno}, {funcName}): {message}", style='{'
            ))
        self.lg.addHandler(self.fh)

        self.sh = logging.StreamHandler(stream=sys.stdout)
        self.sh.setFormatter(colorlog.LevelFormatter(
                fmt = {
                    "DEBUG": "{log_color}{levelname} ({module} L{lineno}, {funcName}): {message}",
                    "INFO": "{log_color}{message}",
                    "WARNING": "{log_color}{levelname}: {message}",
                    "ERROR": "{log_color}{levelname} ({module} L{lineno}, {funcName}): {message}",
                    "CRITICAL": "{log_color}{levelname} ({module} L{lineno}, {funcName}): {message}"
                },
                log_colors = {
                    "DEBUG": "purple",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red"
                },
                style = '{'
            ))
        self.sh.setLevel(logging.INFO)
        self.lg.addHandler(self.sh)
        self.lg.debug('Logging has started')

class Config:
    """
    Class for working with the configuration file
    """
    def __init__(self, filename):
        self.log = logging.getLogger(__name__)

        self.filename = filename
        if not os.path.isfile(filename):
            self.log.critical("'{}'' does not exist".format(filename))
            os._exit(1)
        
        try:
            config = configparser.ConfigParser(interpolation=None)
            config.read(filename, encoding='utf-8')
        except Exception as e:
            self.log.critical(str(e))
            os._exit(1)

        self.token = config.get('Auth', 'Token', fallback=None)

        self.log.debug("Loaded '{}'".format(filename))
        self.validate()

    def validate(self):
        """
        Checks configuration options for valid values
        """
        critical = False
        if not self.token:
            self.log.critical('You must provide a token in the config')
            critical = True
        if critical:
            os._exit(1)
