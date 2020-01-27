from components import mobiles
from utilities import configUtilities, colourUtilities
from utilities.mobileHelp import MobileUtilities
from loguru import logger
from utilities.externalfileutilities import Externalfiles
from utilities.jsonUtilities import read_json_file

# actions
# create new entity with no trappings --> done
# create and equip armour
# create and equip  weapons
# create and equip  jewellery
# position entity in the game map


class Entity:
    def __init__(self, gameworld):
        self.gameworld = gameworld
        self.game_config = configUtilities.load_config()

    def create_new_entity(self):
        entity_id = MobileUtilities.get_next_entity_id(self.gameworld)
        return entity_id

    def create_new_enemy(self, entity_id):
        enemy_file = configUtilities.get_config_value_as_string(configfile=self.game_config, section='default',
                                                                      parameter='ENEMIESFILE')

        MobileUtilities.create_base_mobile(gameworld=self.gameworld, game_config=self.game_config, entity_id=entity_id)

        # temp code to read the enemies Json file
        # and use it to define the enemy
        # will need a different way to create multiple enemies

        enemies_file = read_json_file(enemy_file)

        for option in enemies_file['enemies']:
            enemy_race = option['race']
            enemy_class = option['class']
            enemy_desc = option['description']
            enemy_glyph = option['glyph']
            enemy_fg = option['fg']
            enemy_bg = option['bg']
            enemy_image = int(option['image'])
            enemy_ai = option['ai']

            entity_ai = configUtilities.get_config_value_as_string(configfile=self.game_config, section='game',
                                                                      parameter='AI_LEVEL_' + enemy_ai)

            if option['clothing-present'] == 'no':
                if option['clothing-generate'] == 'yes':
                    pass
                    # generate them procedurally
            else:
                clothing_head = option['clothing-head']
                clothing_back = option['clothing-back']
                clothing_front = option['clothing-front']
                clothing_feet = option['clothing-feet']
                clothing_legs = option['clothing-legs']
                clothing_chest = option['clothing-chest']
                clothing_shoulders = option['clothing-shoulders']

            if option['weapons-present'] == 'no':
                if option['weapons-generate'] == 'yes':
                    pass
                    # generate them procedurally
            else:
                main_hand = option['weapons-main']
                off_hand = option['weapons-off']
                both_hands = option['weapons-both']

            if option['jewellery-present'] == 'no':
                if option['jewellery-generate'] == 'yes':
                    pass
                    # generate them procedurally
            else:
                jewell_neck = option['jewellery-neck']
                jewell_ring1 = option['jewellery-ring1']
                jewell_ring2 = option['jewellery-ring2']
                jewell_earring1 = option['jewellery-earring1']
                jewell_earring2 = option['jewellery-earring2']

        # now apply the values to the base mobile object

            MobileUtilities.set_entity_ai(gameworld=self.gameworld, entity=entity_id, value=entity_ai)
            MobileUtilities.setup_racial_attributes(gameworld=self.gameworld, player=entity_id, selected_race=enemy_race, race_size='normal', bg=colourUtilities.get('BLACK'))
            MobileUtilities.setup_class_attributes(gameworld=self.gameworld, player=entity_id, selected_class=enemy_class, health=100, spellfile='')
            MobileUtilities.set_mobile_description(gameworld=self.gameworld, entity=entity_id, value=enemy_desc)
            MobileUtilities.set_mobile_glyph(gameworld=self.gameworld, entity=entity_id, value=enemy_glyph)
            MobileUtilities.set_mobile_fg_render_colour(gameworld=self.gameworld, entity=entity_id, value=enemy_fg.upper())
            MobileUtilities.set_mobile_bg_render_colour(gameworld=self.gameworld, entity=entity_id, value=enemy_bg.upper())
            MobileUtilities.set_mobile_render_image(gameworld=self.gameworld, entity=entity_id, value=enemy_image)
            MobileUtilities.set_mobile_visible(gameworld=self.gameworld, entity=entity_id)
