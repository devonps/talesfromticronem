import esper

from utilities.jsonUtilities import read_json_file
from loguru import logger
from newGame import constants
from components import shared, condis, spellBoons
from components.addStatusEffects import process_status_effect


def main():

#    logger.add(constants.LOGFILE, format=constants.LOGFORMAT)

    logger.info('********************')
    logger.info('* New game started *')
    logger.info('********************')

    weapons = read_json_file(constants.JSONFILEPATH + 'weapons.json')
    for weapon in weapons['weapons']:
        print(weapon['wielded_both_hands'])

    mobiles = read_json_file(constants.JSONFILEPATH + 'mobiles.json')

    for mobile in mobiles['mobiles']:
        print('The ' + mobile['name'] + ' is a type of ' + mobile['type'], )
        if 'variations' in mobile:
            print('The ' + mobile['name'] + ' has variations')
            variations = mobile['variations']
            for k in variations:
                print('The ' + mobile['name'] + ' is now a ' + mobile['name'] + ' ' + k['suffix'] +
                      ' and is now equipped with a ' + k['equipment'])

    conditions = read_json_file(constants.JSONFILEPATH + 'conditions.json')
    for condi in conditions['conditions']:
        print(condi['name'])

    boons = read_json_file(constants.JSONFILEPATH + 'boons.json')
    for boon in boons['boons']:
        print(boon['name'])


# create esper world
    Gameworld = esper.World()

    spells = read_json_file(constants.JSONFILEPATH + 'spells.json')
    for spell in spells['spells']:
        myspell = Gameworld.create_entity()
        Gameworld.add_component(myspell, shared.Name(spell['name']))
        Gameworld.add_component(myspell, shared.Description(spell['description']))
        effects = spell['effects']
        process_status_effect(Gameworld, myspell, effects)

    for ent, (name, desc, cond, boon) in Gameworld.get_components(shared.Name, shared.Description,
                                                                  condis.Bleeding, spellBoons.Regeneration):
        print(name.text + ' lasts for: ' + str(cond.lasts_for) + ' turns.')
        print(name.text + ' regen max stacks: ' + str(boon.max_stacks))


if __name__ == '__main__':
    main()