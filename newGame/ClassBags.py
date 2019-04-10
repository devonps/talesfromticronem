from utilities.jsonUtilities import read_json_file
from newGame import constants
from loguru import logger
from utilities import world
from components import bags, mobiles


def create_bag(gameworld, entity):
    bags_file = read_json_file(constants.JSONFILEPATH + 'bags.json')
    bag_count = 0
    for this_bag in bags_file['bags']:
        new_bag = world.get_next_entity_id(gameworld=gameworld)
        bag_count += 1

        gameworld.add_component(new_bag, bags.Description(this_bag['description']))
        gameworld.add_component(new_bag, bags.Material(this_bag['material']))
        gameworld.add_component(new_bag, bags.SlotSize(maxsize=this_bag['slots'], populated=0))
        gameworld.add_component(new_bag, bags.Owner(entity))
        gameworld.add_component(new_bag, bags.BagBeingUsed)
        logger.info('New bag created as entity {} and a description of {}', new_bag, this_bag['description'])

        mobile_inventory_component = gameworld.component_for_entity(entity, mobiles.Inventory)

        mobile_inventory_component.bags.append(new_bag)
