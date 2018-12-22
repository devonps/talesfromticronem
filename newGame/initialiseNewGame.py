import random
import tcod
from time import gmtime, strftime


def get_constants():

    game_window_title = 'Tales from Ticronem'
    screen_width = 100
    screen_height = 60

    map_width = 80
    map_height = 40

    # logging
    log_folder = 'logs/'
    log_filename = 'gamelog_'
    log_extension = '.log'
    log_time = '{time:DD-MM-YYYY at HH:mm:ss.SSS}'
    logfile = log_folder + log_filename + log_time + log_extension
    logformat = log_time + ' | {level} | {message}'

    # PCG
    player_seed = 0
    dungeon_stream = 0

    if player_seed > 0:
        world_seed = player_seed
    else:
        world_seed = random.getrandbits(30)

    # holds the number of RNG streams used in the PCG generator
    rng_streams = 10

    # simple-dungeon room information
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    hud_x_left_column = 2
    hud_y_top_row = 2

    # colours used to draw the dungeon
    colors = {
        'dark_wall': tcod.dark_yellow,
        'dark_ground': tcod.Color(50, 50, 150),
        'light_wall': tcod.Color(130, 110, 50),
        'light_ground': tcod.Color(200, 180, 50)
    }

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    # Screenshot
    scrfilepath = 'static/screenshots/'
    scrfilename = 'screenshot '
    scrfileextension = 'jpg'
    scrrandomname = strftime("%d-%m-%Y %H:%M:%S", gmtime())

    # external data
    JsonFilepath = 'static/data/'


    constants = {
        'game_window_title': game_window_title,
        'screen_height': screen_height,
        'screen_width': screen_width,
        'logformat': logformat,
        'logfile': logfile,
        'map_width': map_width,
        'map_height': map_height,
        'world_seed': world_seed,
        'dungeon_stream': dungeon_stream,
        'rng_streams': rng_streams,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'colours': colors,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'hud_x_left_column': hud_x_left_column,
        'hud_y_top_row': hud_y_top_row,
        'ss_folder': scrfilepath,
        'ss_filename': scrfilename,
        'ss_extension': scrfileextension,
        'ss_random_name': scrrandomname,
        'Json_file_path': JsonFilepath

    }

    return constants

