from components import builds
from utilities import world
from loguru import logger


class BuildLibrary:

    @staticmethod
    def get_build_entity(gameworld):

        build = 0
        for ent, build_date in gameworld.get_component(builds.DateTimeStamp):
            if build_date:
                build = ent
        return build

    @staticmethod
    def create_build_entity(gameworld):

        build_entity = world.get_next_entity_id(gameworld=gameworld)

        gameworld.add_component(build_entity, builds.BuildRace())
        gameworld.add_component(build_entity, builds.BuildClass())
        gameworld.add_component(build_entity, builds.BuildJewellery())
        gameworld.add_component(build_entity, builds.BuildMainHand())
        gameworld.add_component(build_entity, builds.BuildOffHand())
        gameworld.add_component(build_entity, builds.BuildArmour())
        gameworld.add_component(build_entity, builds.BuildGender())
        gameworld.add_component(build_entity, builds.BuildName())
        gameworld.add_component(build_entity, builds.DateTimeStamp())

        return build_entity

    @staticmethod
    def decode_saved_build(buildcode):
        decoded = []
        if len(buildcode) < 7:
            logger.warning('Incorrect buildcode length of {}', len(buildcode))
            return 0

        r = buildcode[0]
        if r == 'A':
            decoded.append('Dilga')
        if r == 'B':
            decoded.append('Eskeri')
        if r == 'C':
            decoded.append('Jogah')
        if r == 'D':
            decoded.append('Oshun')

        c = buildcode[1]
        if c == 'A':
            decoded.append('necromancer')
        if c == 'B':
            decoded.append('witch doctor')
        if c == 'C':
            decoded.append('druid')
        if c == 'D':
            decoded.append('illusionist')
        if c == 'E':
            decoded.append('elementalist')
        if c == 'F':
            decoded.append('chronomancer')

        j = buildcode[2]
        if j == 'A':
            decoded.append('defensive')
        if j == 'B':
            decoded.append('balanced')
        if j == 'C':
            decoded.append('offensive')

        m = buildcode[3]
        if m == 'A':
            decoded.append('sword')
        if m == 'B':
            decoded.append('wand')
        if m == 'C':
            decoded.append('staff')
        if m == 'F':
            decoded.append('dagger')
        if m == 'G':
            decoded.append('scepter')

        o = buildcode[4]
        if o == 'A':
            decoded.append('sword')
        if o == 'C':
            decoded.append('staff')
        if o == 'D':
            decoded.append('rod')
        if o == 'E':
            decoded.append('focus')
        if o == 'F':
            decoded.append('dagger')

        a = buildcode[5]
        if a == 'A':
            decoded.append('giver')
        if a == 'B':
            decoded.append('healer')
        if a == 'C':
            decoded.append('malign')
        if a == 'D':
            decoded.append('mighty')
        if a == 'E':
            decoded.append('precise')
        if a == 'F':
            decoded.append('resilient')
        if a == 'G':
            decoded.append('vital')

        g = buildcode[6]
        if g == 'A':
            decoded.append('male')
        if g == 'B':
            decoded.append('female')

        return decoded


    @staticmethod
    def save_build_to_library(gameworld):

        build_entity = BuildLibrary.get_build_entity(gameworld=gameworld)

        build_code = BuildLibrary.get_build_race(gameworld=gameworld, entity=build_entity)
        build_code += BuildLibrary.get_build_class(gameworld=gameworld, entity=build_entity)
        build_code += BuildLibrary.get_build_jewellery(gameworld=gameworld, entity=build_entity)
        build_code += BuildLibrary.get_build_main_hand(gameworld=gameworld, entity=build_entity)
        build_code += BuildLibrary.get_build_off_hand(gameworld=gameworld, entity=build_entity)
        build_code += BuildLibrary.get_build_armour(gameworld=gameworld, entity=build_entity)
        build_code += BuildLibrary.get_build_gender(gameworld=gameworld, entity=build_entity)
        build_name = BuildLibrary.get_build_name(gameworld=gameworld, entity=build_entity)
        build_date = BuildLibrary.get_build_date(gameworld=gameworld, entity=build_entity)
        build_time = BuildLibrary.get_build_time(gameworld=gameworld, entity=build_entity)
        build_info = build_code + ':' + build_name + ':' + build_date + ':' + build_time

        return build_info

    @staticmethod
    def get_build_date(gameworld, entity):
        return gameworld.component_for_entity(entity, builds.DateTimeStamp).dt


    @staticmethod
    def get_build_time(gameworld, entity):
        return gameworld.component_for_entity(entity, builds.DateTimeStamp).tm


    @staticmethod
    def set_build_race(gameworld, entity, label):
        gameworld.component_for_entity(entity, builds.BuildRace).label = label

    @staticmethod
    def get_build_race(gameworld, entity):
        return gameworld.component_for_entity(entity, builds.BuildRace).label

    @staticmethod
    def set_build_armour(gameworld, entity, label):
        gameworld.component_for_entity(entity, builds.BuildArmour).label = label

    @staticmethod
    def get_build_armour(gameworld, entity):
        return gameworld.component_for_entity(entity, builds.BuildArmour).label

    @staticmethod
    def set_build_main_hand(gameworld, entity, label):
        gameworld.component_for_entity(entity, builds.BuildMainHand).label = label

    @staticmethod
    def get_build_main_hand(gameworld, entity):
        return gameworld.component_for_entity(entity, builds.BuildMainHand).label

    @staticmethod
    def set_build_off_hand(gameworld, entity, label):
        gameworld.component_for_entity(entity, builds.BuildOffHand).label = label

    @staticmethod
    def get_build_off_hand(gameworld, entity):
        return gameworld.component_for_entity(entity, builds.BuildOffHand).label

    @staticmethod
    def set_build_name(gameworld, entity, label):
        gameworld.component_for_entity(entity, builds.BuildName).label = label

    @staticmethod
    def get_build_name(gameworld, entity):
        return gameworld.component_for_entity(entity, builds.BuildName).label

    @staticmethod
    def set_build_gender(gameworld, entity, label):
        gameworld.component_for_entity(entity, builds.BuildGender).label = label

    @staticmethod
    def get_build_gender(gameworld, entity):
        return gameworld.component_for_entity(entity, builds.BuildGender).label

    @staticmethod
    def set_build_class(gameworld, entity, label):
        gameworld.component_for_entity(entity, builds.BuildClass).label = label

    @staticmethod
    def get_build_class(gameworld, entity):
        return gameworld.component_for_entity(entity, builds.BuildClass).label

    @staticmethod
    def set_build_jewellery(gameworld, entity, label):
        gameworld.component_for_entity(entity, builds.BuildJewellery).label = label

    @staticmethod
    def get_build_jewellery(gameworld, entity):
        return gameworld.component_for_entity(entity, builds.BuildJewellery).label