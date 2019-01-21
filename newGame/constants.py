import random


GAME_WINDOW_TITLE = 'Tales from Ticronem'

# logging
LOG_FOLDER = 'logs/'
LOG_FILENAME = 'gamelog_'
LOG_EXTENSION = '.log'
LOG_TIME = '{time:DD-MM-YYYY at HH:mm:ss.SSS}'
LOGFILE = LOG_FOLDER + LOG_FILENAME + LOG_TIME + LOG_EXTENSION
LOGFORMAT = LOG_TIME + ' | {level} | {message}'

# PCG
PLAYER_SEED = 0
DUNGEON_STREAM = 0

if PLAYER_SEED > 0:
    WORLD_SEED = PLAYER_SEED
else:
    WORLD_SEED = random.getrandbits(30)

# holds the number of RNG streams used in the PCG generator
RNG_STREAMS = 10

# tcod console settings
SCREEN_WIDTH = 100
SCREEN_HEIGHT = 60

# game-map settings
MAP_WIDTH = 240
MAP_HEIGHT = 120

# dungeon viewport
VIEWPORT_WIDTH = 80
VIEWPORT_HEIGHT = 40

# viewport scrolling values
VIEWPORT_SCROLL_X = 30
VIEWPORT_SCROLL_Y = 30

# message box settings
MSG_PANEL_START_Y = VIEWPORT_HEIGHT + 2
MSG_PANEL_WIDTH = 80
MSG_PANEL_DEPTH = 10
MSG_PANEL_LINES = MSG_PANEL_DEPTH - 1

# status effects settings

# simple-dungeon room information
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30
HUD_X_LEFT_COLUMN = 2
HUD_Y_TOP_ROW = 2

# spell constants
AOE_SMALL = 1
AOE_MEDIUM = 2
AOE_LARGE = 3

SPELL_DIST_PERSONAL = 1     # 130 / 150
SPELL_DIST_CLOSE = 3        # 300
SPELL_DIST_NEARBY = 5       # 600
SPELL_DIST_FAR = 7          # 900
SPELL_DIST_VERY_FAR = 10    # 1200


# AI constants

AI_LEVEL_NONE = 0       # the entity cannot perform any actions
AI_LEVEL_PLAYER = 1     # player character
AI_LEVEL_WIZARD = 2     # enemy - most intelligent
AI_LEVEL_DEMON = 3     # enemy - intelligent
AI_LEVEL_MONSTER = 4    # enemy - stupid
AI_LEVEL_NPC = 5       # neutral - task orientated


AIBehaviour = []

# playable classes
character_classes = ['necromancer', 'witch doctor', 'druid', 'mesmer', 'elementalist', 'chronomancer']

playable_classes = ['necromancer']

demon_classes = ['fire', 'ice', 'earth']

demon_weapons = ['focus', 'rod']

# conditions
condi_effects = ['bleeding', 'burning', 'cripple', 'confusion', 'poison', 'torment',
                 'blind', 'chill', 'fear', 'immobilize', 'vulnerability', 'selfbleeding']
boon_effects = ['aegis', 'alacrity', 'fury', 'might', 'protection', 'regeneration',
                'resistance', 'retaliation', 'stability', 'swiftness']

class_resources =['lifeforce', 'damage', 'transferconditions', 'strikes_for','boonsconverted']

FOV_ALGORITHM = 0
FOV_LIGHT_WALLS = True
FOV_RADIUS = 10

# Screenshot
SCRFILEPATH = 'static/screenshots/'
SCRFILENAME = 'screenshot '
SCRFILEEXTENSION = 'jpg'

# external data
JSONFILEPATH = 'static/data/'