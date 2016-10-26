import logging
import os
import configparser
import ruamel.yaml as yaml
import json

from .exceptions import Shutdown

log = logging.getLogger(__name__)


def load_json(file):
    """Loads a JSON file and returns it as a dict"""
    with open(file) as f:
        return json.load(f)


def dump_json(file, array):
    """Dumps a dict to a JSON file"""
    with open(file, 'w') as f:
        return json.dump(array, f)


class Config:

    """
    Class for working with the configuration file
    """

    def __init__(self, filename):
        self.filename = filename
        if not os.path.isfile(filename):
            log.critical("'{}'' does not exist".format(filename))
            raise Shutdown()

        try:
            config = configparser.ConfigParser(interpolation=None)
            config.read(filename, encoding='utf-8')
        except Exception as e:
            log.critical(str(e))
            raise Shutdown()

        # ---------------------------------------------------- #
        # DO NOT EDIT THIS FILE DIRECTLY. EDIT THE CONFIG FILE #
        # ---------------------------------------------------- #

        # [Auth]
        self.token = config.get('Auth', 'Token', fallback=None)
        self.password = config.get('Auth', 'Password', fallback=None)

        # [General]
        self.selfbot = config.getboolean('General', 'Selfbot', fallback=False)
        self.pm = config.getboolean('General', 'AllowPms', fallback=True)
        self.prefix = config.get('General', 'Prefix', fallback='!')
        self.delete = config.getboolean('General', 'Delete', fallback=True)

        # [Database]
        self.rhost = config.get('Database', 'Host', fallback='localhost')
        self.rport = config.getint('Database', 'Port', fallback=28015)
        self.ruser = config.get('Database', 'User', fallback='admin')
        self.rpass = config.get('Database', 'Password', fallback='')
        self.rname = config.get('Database', 'Name', fallback='turbo')

        # [Advanced]
        self.nodatabase = config.getboolean('Advanced', 'NoDatabase', fallback=False)
        self.readaliases = config.getboolean('Advanced', 'ReadAliases', fallback=True)
        self.selfbotmessageedit = config.getboolean('Advanced', 'SelfbotMessageEdit', fallback=True)

        self.dbtable_tags = config.get('Advanced', 'DbTable_Tags', fallback='tags')

        self.discrimrevert = config.getboolean('Advanced', 'DiscrimRevert', fallback=True)
        self.backuptags = config.getboolean('Advanced', 'BackupTags', fallback=True)

        log.debug("Loaded '{}'".format(filename))
        self.validate()

    def validate(self):
        """
        Checks configuration options for valid values
        """
        critical = False
        if not self.token:
            log.critical('You must provide a token in the config')
            critical = True
        if critical:
            raise Shutdown()


class Yaml:

    """
    Class for handling YAML
    """

    def parse(filename):
        """
        Parse a YAML file
        """
        try:
            with open(filename) as f:
                try:
                    return yaml.load(f)
                except yaml.YAMLError as e:
                    log.critical("Problem parsing {} as YAML: {}".format(
                        filename, e))
                    return None
        except FileNotFoundError:
            log.critical("Problem opening {}: File was not found".format(filename))
            return None
