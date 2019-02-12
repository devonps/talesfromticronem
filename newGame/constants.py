import tcod


GAME_WINDOW_TITLE = 'Tales from Ticronem'

# logging
LOG_FOLDER = 'logs/'
LOG_FILENAME = 'gamelog_'
LOG_EXTENSION = '.log'
LOG_TIME = '{time:DD-MM-YYYY at HH:mm:ss.SSS}'
LOGFILE = LOG_FOLDER + LOG_FILENAME + LOG_TIME + LOG_EXTENSION
LOGFORMAT = LOG_TIME + ' | {level} | {message}'

# PCG
PLAYER_SEED = ''
WORLD_SEED = 0

# individual streams used throughout the game
PRNG_STREAM_MOBILES = 0
PRNG_STREAM_ITEMS = 1
PRNG_STREAM_SPELLS = 2
PRNG_STREAM_DUNGEONS = 3

# external game activities settings
GAME_ACTIONS_FILE = 'Actions.txt'

# tcod root console settings
SCREEN_WIDTH = 100
SCREEN_HEIGHT = 60

# game-map settings

# the next 2 settings are the dimensions of the total map area size
# MAP_WIDTH = 240
# MAP_HEIGHT = 120
# for now I've restricted the total area to the size of the viewport
MAP_WIDTH = 80
MAP_HEIGHT = 40

# dungeon viewport
VIEWPORT_WIDTH = 82
VIEWPORT_HEIGHT = 42
VIEWPORT_START_X = 0
VIEWPORT_START_Y = 0

# game map drawing offsets for use with viewport
MAP_VIEW_DRAW_X = VIEWPORT_START_X + 1
MAP_VIEW_DRAW_Y = VIEWPORT_START_Y + 1

# viewport scrolling values
VIEWPORT_SCROLL_X = 30
VIEWPORT_SCROLL_Y = 30

# FOV settings
FOV_ALGORITHM = tcod.FOV_BASIC
FOV_LIGHT_WALLS = True
FOV_RADIUS = 10

# HUD_X_LEFT_COLUMN = 2
# HUD_Y_TOP_ROW = 2

# message box settings
MSG_PANEL_START_Y = VIEWPORT_HEIGHT
MSG_PANEL_START_X = 0
MSG_PANEL_WIDTH = 40
MSG_PANEL_LINES = 10
MSG_PANEL_DEPTH = MSG_PANEL_LINES + 2


# horizontal bar starting points
H_BAR_X = MSG_PANEL_WIDTH
H_BAR_Y = MSG_PANEL_START_Y

BO_CO_CO_WIDTH = 19
BCC_BAR_RIGHT_SIDE = BO_CO_CO_WIDTH + 2

# Vertical bars
V_BAR_DEPTH = 30
V_BAR_X = VIEWPORT_WIDTH
V_BAR_Y = (VIEWPORT_HEIGHT - V_BAR_DEPTH) - 3
# V_BAR_D = V_BAR_Y + V_BAR_DEPTH + 1
V_BAR_D = V_BAR_DEPTH + 2

# Spell bar settings
SPELL_BAR_X = 20
SPELL_BAR_Y = MSG_PANEL_START_Y + MSG_PANEL_DEPTH
SPELL_SLOTS = 10
SPELL_BOX_WIDTH = 5
SPELL_BAR_WIDTH = SPELL_SLOTS * SPELL_BOX_WIDTH
SPELL_BOX_DEPTH = 5
SPELL_SLOTS_Y = 55
SPELL_SLOTS_X = 21

SPELL_SLOT_N_X = []
for a in range(1, SPELL_SLOTS):
    px = 21 + (a * SPELL_BOX_WIDTH)
    SPELL_SLOT_N_X.append(px)


# status effects settings

# simple-dungeon room information
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

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

# playable races
playable_races = ['human', 'elf', 'orc', 'troll']

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

# colors
colors = {
    'unexplored': tcod.black,
    'dark_wall': tcod.dark_gray,
    'dark_ground': tcod.darker_gray,
    'light_wall': tcod.grey,
    'light_ground': tcod.yellow
}

# Screenshot
SCRFILEPATH = 'static/screenshots/'
SCRFILENAME = 'screenshot '
SCRFILEEXTENSION = 'jpg'

# external data
JSONFILEPATH = 'static/data/'
HUMANNAMESFILE = 'static/names/human.txt'
ELFNAMESFILE = 'static/names/elf.txt'
ORCNAMESFILE = 'static/names/orc.txt'
TROLLNAMESFILE = 'static/names/troll.txt'
REGIONNAMESFILE = 'static/names/region.txt'
TOWNNAMESFILE = 'static/names/town.txt'
WIZARDNAMESFILE = 'static/names/wizard.txt'
NPCNAMESFILE = 'static/names/npc.txt'
DEMONNAMESFILE = 'static/names/demon.txt'

# text input panel settings
TXT_PANEL_WRITE_X = 1
TXT_PANEL_WRITE_Y = 2
TXT_PANEL_WIDTH = 35
TXT_PANEL_HEIGHT = 25
TXT_PANEL_FPS = 30