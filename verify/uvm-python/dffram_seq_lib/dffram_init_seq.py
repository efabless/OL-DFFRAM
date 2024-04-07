from uvm.seq import UVMSequence
from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_message_defines import uvm_fatal, uvm_info, uvm_warning
from uvm.base.uvm_config_db import UVMConfigDb
from EF_UVM.bus_env.bus_seq_lib.bus_seq_base import bus_seq_base
from cocotb.triggers import Timer
from uvm.macros.uvm_sequence_defines import uvm_do_with, uvm_do
from dffram_seq_lib.dffram_bus_base_seq import dffram_bus_base_seq


class dffram_init_seq(dffram_bus_base_seq):
    """seuqence for dffram initialization with random values"""

    def __init__(self, ram_size, name="dffram_bus_seq"):
        super().__init__(name)
        self.ram_size = ram_size

    async def body(self):
        for address in range(0, self.ram_size * 4, 4):
            await self.write_addr(
                lambda addr: addr == address, lambda write_size: write_size == "word"
            )


uvm_object_utils(dffram_init_seq)
