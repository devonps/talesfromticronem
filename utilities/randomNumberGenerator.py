"""
Implementation of the PCG random number generator, Python OO style.
For the original docs, read
`this <http://www.pcg-random.org/using-pcg-c-basic.html>`_.
"""


def _uint32(n):
    return n & 0xffffffff


def _uint64(n):
    return n & 0xffffffffffffffff


class PCG32Generator:
    __slots__ = ['state', 'inc']

    def __init__(self, state, seq):
        """
        :param state: Any 64-bit value. This is the "current state" of the
                      generator within the output sequence. The RNG iterates
                      through all 2^64 possible internal states.
        :param seq: Any 64-bit value (only 63 bits are significant). This value
                    defines which of the 2^63 possible reandom sequences the
                    current state is iterating through; it holds the same value
                    over the lifetime of the RNG.
        Different values for sequence constant cause the generator to produce a
        different (and unique) sequence of random numbers (sometimes called the
        stream). In other words, it's as if you have 2^63 different RNGs available,
        and this constant lets you choose which one you're using.
        You can create as many separate RNGs as you like. If you give them
        different sequence constants, they will be independent and uncorrelated
        with each other (i.e., their sequences will not overlap at all).
        """
        self.state = 0
        self.inc = _uint64(seq << 1) | 1
        self._advance()
        self.state = _uint64(self.state + state)
        self._advance()

    def _advance(self):
        oldstate = self.state
        self.state = _uint64(oldstate * 6364136223846793005 + self.inc)
        xorshifted = _uint32(((oldstate >> 18) ^ oldstate) >> 27)
        rot = _uint32(oldstate >> 59)
        return _uint32((xorshifted >> rot) | (xorshifted << ((-rot) & 31)))

    def get_next_uint32(self):
        """
        Mutates internal state and returns the next random value in the sequence,
        a 32-bit unsigned integer.
        """
        return self._advance()

    def get_next_uint(self, bound):
        """
        :param int bound: Max value (exclusive)
        Return a value between zero (inclusive) and *bound* (exclusive).
        """
        # To avoid bias, we need to make the range of the RNG a multiple of
        # bound, which we do by dropping output less than a threshold.
        # A naive scheme to calculate the threshold would be to do
        #
        # uint32_t threshold = 0x100000000ull % bound;
        #
        # but 64-bit div/mod is slower than 32-bit div/mod (especially on
        # 32-bit platforms). In essence, we do
        #
        # uint32_t threshold = (0x100000000ull-bound) % bound;
        #
        # because this version will calculate the same modulus, but the LHS
        # value is less than 2^32.
        bound = _uint32(bound)
        threshold = _uint32(-bound) % bound

        # Uniformity guarantees that this loop will terminate. In practice, it
        # should usually terminate quickly; on average (assuming all bounds are
        # equally likely), 82.25% of the time, we can expect it to require just
        # one iteration. In the worst case, someone passes a bound of 2^31 + 1
        # (i.e., 2147483649), which invalidates almost 50% of the range. In
        # practice, bounds are typically small and only a tiny amount of the range
        # is eliminated.
        while True:
            val = self.get_next_uint32()
            if val >= threshold:
                return val % bound

    def get_next_number_in_range(self, lower, upper):
        """

        :param lower: This is the minimum value you want to return
        :param upper: This is the maximum value you want returned
        :return: An integer between lower (inclusive) and upper (exclusive)
        """
        if lower > upper:
            l = upper
            upper = lower
            lower = l

        if lower == upper:
            return lower
        value = PCG32Generator.get_next_uint(self, upper)
        vx = False
        while not vx:
            if value >= lower:
                vx = True
            else:
                value = PCG32Generator.get_next_uint(self, upper)
        return value

    def convert_string_to_integer(value):
        """
        This method converts a string, encoded as utf-8, into a series of integers and then
        sums all integers into a single integer, which is returned.

        :param value: Incoming string to be converted
        :return: Integer that represents the sum of the individual integers
        """
        bytes1 = bytes(value, 'utf-8')
        sm = 0

        for b1 in bytes1:
            sm += b1

        return sm


class BitOperations:

    @staticmethod
    def set_bit(value, bit):
        return value | (1 << bit)

    @staticmethod
    def clear_bit(value, bit):
        return value & ~(1 << bit)

# class TCODGenerator:
#
#     @staticmethod
#     def generate_tcod_random_seed(seed_object):
#         """
#         This method is called from within the map generation routines that require a deterministic tcod
#         RNG, such as the tcod.bsp map generation routines.
#
#         It takes a PCG32Generator object (seed_object) and uses it to create a tcod random number generator
#
#         :param seed_object: 32bit Integer, has already been used in the PCG32Generator class, as in this example
#                     dungeon_seed = PCG32Generator(constants.WORLD_SEED, constants.PRNG_STREAM_DUNGEONS)
#         :return: tcod random number generator object
#         """
#
#         my_rng = seed_object.get_next_uint32()
#
#         tcod_random_object = tcod.random_new_from_seed(my_rng, 0)
#
#         return tcod_random_object
#
#     @staticmethod
#     def destroy_tcod_random_seed(seed_object):
#         tcod.random_delete(seed_object)
