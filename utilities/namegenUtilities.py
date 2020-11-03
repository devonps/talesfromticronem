import random

from utilities import jsonUtilities, randomNumberGenerator


def read_name_file(file_to_read):
    return jsonUtilities.read_json_file(filename=file_to_read)


def process_name_file(name_file):
    syllables_start_string = ''
    syllables_middle_string = ''
    syllables_end_string = ''
    rules_string = ''

    for namegen in name_file['male']:
        syllables_start_string = namegen['syllablesStart']
        syllables_middle_string = namegen['syllablesMiddle']
        syllables_end_string = namegen['syllablesEnd']
        rules_string = namegen['rules']

    syllables_start = syllables_start_string.split(',')
    syllables_middle = syllables_middle_string.split(',')
    syllables_end = syllables_end_string.split(',')
    rules = rules_string.split('$')

    mega_list = [syllables_start, syllables_middle, syllables_end, rules]

    return mega_list


def generate_name(name_components):
    formatted_name = ''
    syllables_start = name_components[0]
    syllables_middle = name_components[1]
    syllables_end = name_components[2]
    rules = name_components[3]

    compiled_name = ''

    # TEMP SOLUTION TO USE SAFE PRNG
    prng_seed = random.randrange(1, 100)
    stream = 1
    random_range = randomNumberGenerator.PCG32Generator(prng_seed, stream)

    for rule in rules:
        if rule == 's':
            # use a starting syllable
            ss_len = len(syllables_start)
            random_syllable_index = random_range.get_next_uint(bound=ss_len)
            compiled_name += syllables_start[random_syllable_index]
        if rule == 'm':
            # use a middle syllable
            sm_len = len(syllables_middle)
            random_syllable_index = random_range.get_next_uint(bound=sm_len)
            compiled_name += syllables_middle[random_syllable_index]
        if rule == 'e':
            # use an end syllable
            se_len = len(syllables_end)
            random_syllable_index = random_range.get_next_uint(bound=se_len)
            compiled_name += syllables_end[random_syllable_index]
            formatted_name = compiled_name.replace(" ", "")

    return formatted_name
