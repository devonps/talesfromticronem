import configparser


def load_config():
    config = configparser.ConfigParser()
    config.read('static/data/config.ini')

    return config


def get_config_value_as_string(configfile, section, parameter):
    # strip quotes from the string
    raw_parameter = configfile[section][parameter]
    clean_parm = raw_parameter.translate({ord(i): None for i in '\"\''})

    return clean_parm


def get_config_value_as_text(configfile, section, parameter):
    return configfile[section][parameter]


def get_config_value_as_integer(configfile, section, parameter):
    return int(configfile[section][parameter])


def get_config_value_as_float(configfile, section, parameter):
    return float(configfile[section][parameter])


def get_config_file_sections(configfile):
    return configfile.sections()


def write_config_value(configfile, section, parameter, value):
    configfile[section][parameter] = value
