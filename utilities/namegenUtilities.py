from loguru import logger
from utilities.jsonUtilities import read_json_file
from utilities.randomNumberGenerator import PCG32Generator


def read_name_file(file_to_read):
    return read_json_file(filename=file_to_read)


def process_name_file(name_file):
    syllablesStart_string = ''
    syllablesMiddle_string = ''
    syllablesEnd_string = ''
    rules_string = ''

    for namegen in name_file['male']:
        syllablesStart_string = namegen['syllablesStart']
        syllablesMiddle_string = namegen['syllablesMiddle']
        syllablesEnd_string = namegen['syllablesEnd']
        rules_string = namegen['rules']

    syllables_start = syllablesStart_string.split(',')
    syllables_middle = syllablesMiddle_string.split(',')
    syllables_end = syllablesEnd_string.split(',')
    rules = rules_string.split('$')

    mega_list = [syllables_start, syllables_middle, syllables_end, rules]

    return mega_list


def generate_name(name_components):
    syllables_start = name_components[0]
    syllables_middle = name_components[1]
    syllables_end = name_components[2]
    rules = name_components[3]

    compiled_name = ''

    # TEMP SOLUTION TO USE SAFE PRNG
    prng_seed = 99
    stream = 1
    random_range = PCG32Generator(prng_seed, stream)

    for rule in rules:
        if rule == 's':
            # use a starting syllable
            ss_len = len(syllables_start)
            random_syllable_index = random_range.get_next_uint(bound=ss_len)
            logger.warning('Random start syllable is {}', syllables_start[random_syllable_index])
            compiled_name += syllables_start[random_syllable_index]
        if rule == 'm':
            # use a middle syllable
            sm_len = len(syllables_middle)
            random_syllable_index = random_range.get_next_uint(bound=sm_len)
            logger.warning('Random start syllable is {}', syllables_middle[random_syllable_index])
            compiled_name += syllables_middle[random_syllable_index]
        if rule == 'e':
            # use an end syllable
            se_len = len(syllables_end)
            random_syllable_index = random_range.get_next_uint(bound=se_len)
            logger.warning('Random start syllable is {}', syllables_end[random_syllable_index])
            compiled_name += syllables_end[random_syllable_index]

    logger.warning('Compiled name is {}', compiled_name)

    return compiled_name
