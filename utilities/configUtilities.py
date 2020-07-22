import configparser


def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

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


def set_config_value(configfile, section, parameter, value):
    configfile[section][parameter] = value


def get_config_value_as_list(configfile, section, parameter):
    my_str = get_config_value_as_text(configfile, section, parameter)
    # now break this out into a list
    mylist = my_str.split(",")
    return mylist


def update_game_state(configfile, section, parameter, value):
    configfile[section][parameter] = value
