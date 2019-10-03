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
    def save_build_to_library(gameworld):

        build_entity = BuildLibrary.get_build_entity(gameworld=gameworld)

        buildCode = BuildLibrary.get_build_race(gameworld=gameworld, entity=build_entity)
        buildCode += BuildLibrary.get_build_class(gameworld=gameworld, entity=build_entity)
        buildCode += BuildLibrary.get_build_jewellery(gameworld=gameworld, entity=build_entity)
        buildCode += BuildLibrary.get_build_main_hand(gameworld=gameworld, entity=build_entity)
        buildCode += BuildLibrary.get_build_off_hand(gameworld=gameworld, entity=build_entity)
        buildCode += BuildLibrary.get_build_armour(gameworld=gameworld, entity=build_entity)
        buildCode += BuildLibrary.get_build_gender(gameworld=gameworld, entity=build_entity)
        build_name = BuildLibrary.get_build_name(gameworld=gameworld, entity=build_entity)
        build_date = BuildLibrary.get_build_date(gameworld=gameworld, entity=build_entity)
        build_time = BuildLibrary.get_build_time(gameworld=gameworld, entity=build_entity)
        build_info = buildCode + ':' + build_name + ':' + build_date + ':' + build_time

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