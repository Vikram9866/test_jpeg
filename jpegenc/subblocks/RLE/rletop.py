from myhdl import always_seq, always_comb, block, modbv     
from myhdl import intbv, Signal, concat
from jpegenc.subblocks.RLE.RLECore.rlecore import DataStream, rle
from jpegenc.subblocks.RLE.RLECore.rlecore import RLESymbols, RLEConfig
from jpegenc.subblocks.RLE.RleDoubleFifo.rledoublebuffer import rledoublefifo
from jpegenc.subblocks.RLE.RleDoubleFifo.rledoublebuffer import DoubleFifoBus


class BufferDataBus(RLESymbols):
    """
    Output Interface Class
    Amplitude: amplitude of the number

    size: size required to store amplitude

    runlength: number of zeros

    dovalid: asserts if ouput is valid
    buffer_sel: It selects the buffer in double buffer
    read_enable: enables
    fifo_empty: asserts if any of the two fifos are empty

    """
    def __init__(self, width_data, width_size, width_runlength):
        super(BufferDataBus, self).__init__(width_data, width_size, width_runlength)
        self.buffer_sel = Signal(bool(0))
        self.read_enable = Signal(bool(0))
        self.fifo_empty = Signal(bool(0))


@block
def rletop(clock, reset, datastream, bufferdatabus, rleconfig):
    """The top module connects rle core and rle double buffer"""

    assert isinstance(datastream, DataStream)
    assert isinstance(bufferdatabus,BufferDataBus)
    assert isinstance(rleconfig, RLEConfig)

    width_data = len(datastream.data_in)
    width_addr = len(datastream.read_addr)
    width_size = len(bufferdatabus.size)
    width_runlength = len(bufferdatabus.runlength)
    max_addr_cnt = int((2**(width_addr)) - 1)
    width_depth = max_addr_cnt + 1

    # Signals used to temporarily process data
    rlesymbols_temp = RLESymbols(
        width_data, width_size, width_runlength)
    assert isinstance(rlesymbols_temp, RLESymbols)

    # maximum number of zeroes that can be count
    limit = int((2**width_runlength) - 1)

    # width of data to be stored in rle double fifo
    width_dbuf_data = width_data + width_size + width_runlength

    # instantiation of double buffer bus
    dfifo = DoubleFifoBus(width_dbuf_data)
    assert isinstance(dfifo, DoubleFifoBus)

    # maximum number of pixels that can be processes for one time
    wr_cnt = Signal(modbv(0)[width_addr:])

    @always_comb
    def assign0():      
        dfifo.buffer_sel.next = bufferdatabus.buffer_sel
        dfifo.read_req.next = bufferdatabus.read_enable
        bufferdatabus.fifo_empty.next = dfifo.fifo_empty

    @always_comb
    def assign1():
        """runlength, size and amplitude read from double buffer"""
        bufferdatabus.runlength.next = dfifo.data_out[(
            width_data+width_size+width_runlength):(
            width_data+width_size)]

        bufferdatabus.size.next = dfifo.data_out[(
            width_data+width_size):width_data]

        bufferdatabus.amplitude.next = dfifo.data_out[width_data:0].signed()

    # send the inputdata into rle core
    rle_core = rle(clock, reset, datastream, rlesymbols_temp, rleconfig)

    # write the processed data to rle double fifo
    rle_doublefifo = rledoublefifo(clock, reset, dfifo, width_depth)

    @always_comb
    def assign3():
        dfifo.data_in.next = concat(
            rlesymbols_temp.runlength, rlesymbols_temp.size,
            rlesymbols_temp.amplitude)

        dfifo.write_enable.next = rlesymbols_temp.dovalid

    @always_seq(clock.posedge, reset=reset)
    def seq1():
        rleconfig.ready.next = False
        if rleconfig.start:
            wr_cnt.next = 0

        # select the data to be written
        if rlesymbols_temp.dovalid:
            if (rlesymbols_temp.runlength == limit) and (
                    rlesymbols_temp.size == 0):

                wr_cnt.next = wr_cnt + limit + 1

            else:
                wr_cnt.next = wr_cnt + 1 + rlesymbols_temp.runlength

        if dfifo.data_in == 0 and wr_cnt != 0:
            rleconfig.ready.next = 1
        else:
            if (wr_cnt + rlesymbols_temp.runlength) == max_addr_cnt:
                rleconfig.ready.next = True

    @always_comb
    def assign4():
        # output data valid signal
        bufferdatabus.dovalid.next = bufferdatabus.read_enable

    return (assign0, assign1, rle_core, rle_doublefifo,
            assign3, seq1, assign4)
