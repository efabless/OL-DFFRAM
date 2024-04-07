from uvm.seq import UVMSequence
from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_message_defines import uvm_fatal, uvm_warning
from uvm.base.uvm_config_db import UVMConfigDb
from EF_UVM.bus_env.bus_seq_lib.bus_seq_base import bus_seq_base
from cocotb.triggers import Timer
from uvm.macros.uvm_sequence_defines import uvm_do_with, uvm_do
from dffram_seq_lib.dffram_bus_base_seq import dffram_bus_base_seq
from dffram_seq_lib.dffram_init_seq import dffram_init_seq
import random


class dffram_write_read_seq(dffram_bus_base_seq):
    # use this sequence write or read from register by the bus interface
    # this sequence should be connected to the bus sequencer in the testbench
    # you should create as many sequences as you need not only this one
    def __init__(self, ram_size, name="dffram_bus_seq"):
        super().__init__(name)
        self.ram_size = ram_size

    async def body(self):
        await super().body()
        # initialize ram
        await uvm_do_with(self, dffram_init_seq(self.ram_size))
        # random read and write with 70% write and 30% read
        await self._write_read_seq(write_probability=0.7)
        # random read and write with 50% write and 50% read
        await self._write_read_seq(write_probability=0.5)
        # random read and write with 30% write and 70% read
        await self._write_read_seq(write_probability=0.3)

    async def _write_read_seq(self, iteration_num=0x1000, write_probability=0.5):
        for _ in range(iteration_num):
            if random.random() > write_probability:
                await self.write_addr()
            else:
                await self.read_addr()


uvm_object_utils(dffram_write_read_seq)
