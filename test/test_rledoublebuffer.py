"""Test file for RLE Double Buffer to check its conversion and funtioning"""

from myhdl import block, StopSimulation
from myhdl import ResetSignal, Signal, instance
from myhdl.conversion import verify

from jpegenc.subblocks.RLE.RleDoubleFifo.rledoublebuffer import DoubleFifoBus
from jpegenc.subblocks.RLE.RleDoubleFifo.rledoublebuffer import rledoublefifo

from common import tbclock, reset_on_start, resetonstart


def test_doublebuffer():
    """The functionality of Double Buffer is done here"""

    @block
    def bench_doublebuffer():
        """We check the module with test inputs here"""

        # buffer constant for depth of fifo's and data width
        width_depth = 64
        clock = Signal(bool(0))
        reset = ResetSignal(0, active=1, async=True)

        # instantiation of fifo-bus, clock and rledoublefifo
        dfifo_bus = DoubleFifoBus(width=20)
        inst = rledoublefifo(clock, reset, dfifo_bus, width_depth)
        inst_clock = tbclock(clock)

        assert isinstance(dfifo_bus, DoubleFifoBus)

        @instance
        def tbstim():
            """write data inputs to double buffer"""

            print("start simulation")

            # disable read and write
            dfifo_bus.write_enable.next = False
            dfifo_bus.read_req.next = False

            # reset before sending data
            yield reset_on_start(clock, reset)
            assert dfifo_bus.fifo_empty

            # select first buffer
            dfifo_bus.buffer_sel.next = False
            yield clock.posedge

            # write first data into rle double buffer
            dfifo_bus.write_enable.next = True
            dfifo_bus.data_in.next = -1 and 0xFF
            yield clock.posedge
            dfifo_bus.write_enable.next = False
            yield clock.posedge
            assert dfifo_bus.fifo_empty

            # write data into rle double buffer
            dfifo_bus.write_enable.next = True
            dfifo_bus.data_in.next = 0xA1
            yield clock.posedge
            dfifo_bus.write_enable.next = False
            yield clock.posedge
            assert dfifo_bus.fifo_empty

            # write data into rle double buffer
            dfifo_bus.write_enable.next = True
            dfifo_bus.data_in.next = 0x11
            yield clock.posedge
            dfifo_bus.write_enable.next = False
            yield clock.posedge

            # write data into rle double buffer
            dfifo_bus.write_enable.next = True
            dfifo_bus.data_in.next = 0x101
            yield clock.posedge
            dfifo_bus.write_enable.next = False
            yield clock.posedge

            # write data into rle double buffer
            for test_cases in range(64):
                if test_cases < 28:
                    dfifo_bus.buffer_sel.next = False
                    yield clock.posedge
                else:
                    dfifo_bus.buffer_sel.next = True
                    yield clock.posedge

                dfifo_bus.write_enable.next = True
                dfifo_bus.data_in.next = test_cases
                yield clock.posedge
                dfifo_bus.write_enable.next = False
                yield clock.posedge

            # read data from rle double buffer
            dfifo_bus.read_req.next = True
            yield clock.posedge
            assert dfifo_bus.data_out and -1 == -1
            dfifo_bus.read_req.next = False

            dfifo_bus.buffer_sel.next = True
            yield clock.posedge

            # read data from rle double buffer
            dfifo_bus.read_req.next = True
            yield clock.posedge
            assert dfifo_bus.data_out == 0xA1
            dfifo_bus.read_req.next = False

            dfifo_bus.buffer_sel.next = True
            yield clock.posedge

            # read data from rle double buffer
            dfifo_bus.read_req.next = True
            yield clock.posedge
            assert dfifo_bus.data_out == 0x11
            dfifo_bus.read_req.next = False

            dfifo_bus.buffer_sel.next = True
            yield clock.posedge

            # read data from rle double buffer
            dfifo_bus.read_req.next = True
            yield clock.posedge
            assert dfifo_bus.data_out == 0x101
            dfifo_bus.read_req.next = False

            # read data from rle double buffer
            for test_cases in range(64):
                if test_cases < 28:
                    dfifo_bus.buffer_sel.next = True
                    yield clock.posedge
                else:
                    dfifo_bus.buffer_sel.next = False
                    yield clock.posedge

                dfifo_bus.read_req.next = True
                yield clock.posedge
                assert dfifo_bus.data_out == test_cases
                dfifo_bus.read_req.next = False

            yield clock.posedge

            assert dfifo_bus.fifo_empty

            raise StopSimulation

        return inst, inst_clock, tbstim

    inst_dbuf = bench_doublebuffer()
    inst_dbuf.config_sim(trace=False)
    inst_dbuf.run_sim()


def test_doublebuffer_conversion():
    """This block checks the conversion of Rle Double Fifo"""

    @block
    def bench_doublebuffer_conversion():
        """ test bench for conversion purpose"""

        clock = Signal(bool(0))
        reset = ResetSignal(0, active=1, async=True)
        width_depth = 64
        dfifo_bus = DoubleFifoBus(width=20)

        assert isinstance(dfifo_bus, DoubleFifoBus)

        inst = rledoublefifo(clock, reset, dfifo_bus, width_depth)
        inst_clock = tbclock(clock)
        inst_reset = resetonstart(clock, reset)

        @instance
        def tbstim():
            """dummy inputs given here"""

            yield clock.posedge
            print ("Conversion done!!")
            raise StopSimulation

        return tbstim, inst, inst_clock, inst_reset

    verify.simulator = 'iverilog'
    assert bench_doublebuffer_conversion().verify_convert() == 0
