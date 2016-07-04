""" core of the run length encoder module """
from myhdl import always_comb, always_seq, block
from myhdl import intbv, Signal, modbv
from jpegenc.subblocks.RLE.RLECore.entropycoder import entropycoder


class Component(object):
    """Select the color component"""
    def __init__(self):
        self.y1 = 0
        self.y2 = 1
        self.cb = 2
        self.cr = 3


class DataStream(object):
    """
    Input data streams into Rle Core

    data_in: input to the rle module
    read_addr: data address to be written into core

    """
    def __init__(self, width_data, width_addr):
        self.data_in = Signal(intbv(0)[width_data:].signed())
        self.read_addr = Signal(intbv(0)[width_addr:])


class RLESymbols(object):
    """
    Output Signals generatred by RLE Core
    Amplitude: amplitude of the number

    size: size required to store amplitude

    runlength: number of zeros

    dovalid: asserts if ouput is valid

    """
    def __init__(self, width_data, width_size, width_runlength):
        self.runlength = Signal(intbv(0)[width_runlength:])
        self.size = Signal(intbv(0)[width_size:])
        self.amplitude = Signal(intbv(0)[width_data:].signed())
        self.dovalid = Signal(bool(0))


class RLEConfig(object):
    """
    RLE configuration Signals are the generic signals used in the block
    color_component: select the color component to be processed(Y or cb or cr)
    start: start signal triggers the module to start
            processing data

    sof: start of frame asserts when frame is ready to be processes

    """
    def __init__(self):
        self.color_component = Signal(intbv(0)[3:])
        self.start = Signal(bool(0))
        self.sof = Signal(bool(0))
        self.ready = Signal(bool(0))


def sub(num1, num2):
    """subtractor for Difference Encoder"""
    return num1 - num2

component = Component()

@block
def rle(clock, reset, datastream, rlesymbols, rleconfig):
    """This is the heart of the Run Length Encoder"""
    assert isinstance(datastream, DataStream)
    assert isinstance(rlesymbols, RLESymbols)
    assert isinstance(rleconfig, RLEConfig)

    width_data = len(datastream.data_in)
    width_addr = len(datastream.read_addr)
    width_size = len(rlesymbols.size)
    max_addr_cnt = int((2**(width_addr)) - 1)
    width_runlength = len(rlesymbols.runlength)

    # maximum number of zero's that can be count
    limit = int((2**len(rlesymbols.runlength)) - 1)

    # these signals processes data temporarily
    rlesymbols_temp = RLESymbols(width_data, width_size, width_runlength)
    assert isinstance(rlesymbols_temp, RLESymbols)


    # signals used to store previous data for difference encoding
    # signals used to do zrl processing when zero's exceed limit
    prev_dc_0, prev_dc_1, prev_dc_2, zrl_data_in = [Signal(intbv(0)[
        (width_data):].signed()) for _ in range(4)]

    # used to calculate amplitude
    accumulator = Signal(intbv(0)[(width_data):].signed())

    # signals used to enable read and to store counts
    read_en, divalid, divalid_en, zrl_processing = [
        Signal(bool(0)) for _ in range(4)]

    zero_cnt, read_cnt = [Signal(modbv(0)[(
        width_addr):]) for _ in range(2)]

    write_cnt = Signal(modbv(0)[(width_addr):])

    @always_comb
    def assign():
        """capture the output signals form the rle core"""
        rlesymbols.size.next = rlesymbols_temp.size
        rlesymbols.amplitude.next = rlesymbols_temp.amplitude
        datastream.read_addr.next = read_cnt

    @always_seq(clock.posedge, reset=reset)
    def mainprocessing():
        """sequential block to calculate the runlength"""
        rlesymbols_temp.dovalid.next = False
        rlesymbols_temp.runlength.next = 0
        rlesymbols.runlength.next = rlesymbols_temp.runlength
        rlesymbols.dovalid.next = rlesymbols_temp.dovalid
        divalid.next = read_en

        # when start asserts divalid asserts and processing starts
        if rleconfig.start:
            read_cnt.next = 0
            read_en.next = True
            divalid_en.next = True

        # after processing the last component processing stops
        if divalid and (write_cnt == max_addr_cnt):
            divalid_en.next = False

        if read_en:
            # after processing the last component processing stops
            if read_cnt == max_addr_cnt:
                read_cnt.next = 0
                read_en.next = False
            else:
                read_cnt.next = read_cnt + 1

        if divalid:
            write_cnt.next = write_cnt + 1

            if write_cnt == 0:
                # differece encoding for the dc component
                if (rleconfig.color_component == component.y1) or (
                        rleconfig.color_component == component.y2):

                    # stores previous value
                    accumulator.next = sub(
                        datastream.data_in.signed(), prev_dc_0)

                    prev_dc_0.next = datastream.data_in.signed()

                elif rleconfig.color_component == component.cb:
                    accumulator.next = sub(
                        datastream.data_in.signed(), prev_dc_1)

                    # stores previous value
                    prev_dc_1.next = datastream.data_in.signed()

                elif rleconfig.color_component == component.cr:
                    accumulator.next = sub(
                        datastream.data_in.signed(), prev_dc_2)

                    # stores previous value
                    prev_dc_2.next = datastream.data_in.signed()

                else:
                    pass

                rlesymbols_temp.runlength.next = 0
                rlesymbols_temp.dovalid.next = True

            else:
                # we calculate the runlength here
                if datastream.data_in.signed() == 0:
                    if write_cnt == max_addr_cnt:
                        accumulator.next = 0
                        rlesymbols_temp.runlength.next = 0
                        rlesymbols_temp.dovalid.next = True

                    else:
                        # calulate total number of continous zeroes
                        zero_cnt.next = zero_cnt + 1

                else:
                    if write_cnt == max_addr_cnt:
                        write_cnt.next = 0

                    # if zero's less than limit
                    if zero_cnt <= limit:
                        accumulator.next = datastream.data_in
                        rlesymbols_temp.runlength.next = zero_cnt
                        zero_cnt.next = 0
                        rlesymbols_temp.dovalid.next = True

                    # if zero's greater than limit zrl processing occurs
                    else:
                        accumulator.next = 0
                        rlesymbols_temp.runlength.next = limit

                        # break zero's into parts of limit by subtracting limit
                        zero_cnt.next = zero_cnt - limit
                        rlesymbols_temp.dovalid.next = True
                        zrl_processing.next = True
                        zrl_data_in.next = datastream.data_in
                        divalid.next = False
                        read_cnt.next = read_cnt

        if zrl_processing:
            # if number of zeroes exceeds 15 we stall the input
            if zero_cnt <= limit:
                accumulator.next = zrl_data_in
                rlesymbols_temp.runlength.next = zero_cnt
                zero_cnt.next = 0
                rlesymbols_temp.dovalid.next = True
                divalid.next = divalid_en
                zrl_processing.next = False

            else:
                accumulator.next = 0
                rlesymbols_temp.runlength.next = limit
                zero_cnt.next = zero_cnt - limit
                rlesymbols_temp.dovalid.next = True
                divalid.next = False
                read_cnt.next = read_cnt

        # reset counters when start asserts
        if rleconfig.start:
            zero_cnt.next = 0
            write_cnt.next = 0

        # when end of image occurs
        if rleconfig.sof:
            prev_dc_0.next = 0
            prev_dc_1.next = 0
            prev_dc_2.next = 0

    encoder_inst = entropycoder(
        width_data, clock, reset, accumulator,
        rlesymbols_temp.size, rlesymbols_temp.amplitude)

    return assign, mainprocessing, encoder_inst
