""" This module takes a input and returns amplitude of the input and number of bits required to store the input """

from myhdl import always_seq, block, intbv

def two2bin(num):
    """converts negative number to positive"""
    inum = ~ num
    return inum + 1


def nbits(num, width_data):
    """returns the number of bits required to store num"""
    i = width_data - 1
    while i >= 0:
        if num[i] == 1:
            return i + 1
        i = i - 1
    return num[width_data]


@block
def entropycoder(width_data, clock, reset, data_in, size, amplitude):
    """returns the amplitude of input and number of bits required to store the input """

    @always_seq(clock.posedge, reset=reset)
    def logic():
        """sequential block that finds amplitude and num of bits"""
        if data_in[width_data] == 0:
            amplitude.next = data_in
            size.next = nbits(data_in, width_data)

        else:
            amplitude.next = data_in - 1
            absval = intbv(0)[(width_data):0]
            absval[:] = two2bin(data_in)
            size.next = nbits(absval, width_data)

    return logic
