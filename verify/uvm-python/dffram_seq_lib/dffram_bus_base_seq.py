from uvm.seq import UVMSequence
from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_message_defines import uvm_fatal
from uvm.base.uvm_config_db import UVMConfigDb
from EF_UVM.bus_env.bus_seq_lib.bus_seq_base import bus_seq_base
from cocotb.triggers import Timer
from uvm.macros.uvm_sequence_defines import uvm_do_with, uvm_do
from EF_UVM.bus_env.bus_item import bus_item
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from uvm.base.uvm_object_globals import UVM_LOW
from dffram_bus_updates.bus_item_updated import bus_item_updated


class dffram_bus_base_seq(bus_seq_base):
    # use this sequence write or read from register by the bus interface
    # this sequence should be connected to the bus sequencer in the testbench
    # you should create as many sequences as you need not only this one
    def __init__(self, name="dffram_bus_base_seq"):
        super().__init__(name)
        self.req = bus_item_updated()
        self.rsp = bus_item_updated()

    async def write_addr(self, *constraints):
        await self._write_read(True, *constraints)

    async def read_addr(self, *constraints):
        await self._write_read(False, *constraints)

    async def _write_read(self, is_write, *constraints):
        access_type = bus_item.WRITE if is_write else bus_item.READ
        if constraints is not None:
            await uvm_do_with(
                self, self.req, lambda kind: kind == access_type, *constraints
            )
        else:
            await uvm_do_with(self, self.req, lambda kind: kind == access_type)


uvm_object_utils(dffram_bus_base_seq)
