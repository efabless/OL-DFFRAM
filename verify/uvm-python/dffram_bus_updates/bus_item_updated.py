from EF_UVM.bus_env.bus_item import bus_item
from uvm.seq.uvm_sequence_item import UVMSequenceItem
from uvm.macros import (
    uvm_object_utils_begin,
    uvm_object_utils_end,
    uvm_field_int,
    uvm_object_utils,
)
from uvm.base.uvm_object_globals import UVM_ALL_ON, UVM_NOPACK
from uvm.base.sv import sv
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from uvm.base.uvm_object_globals import UVM_HIGH, UVM_LOW
from uvm.base.uvm_config_db import UVMConfigDb
import random


class bus_item_updated(bus_item):
    """write size is new and new constraints
    data can't be constrained
    """

    def __init__(self, name="bus_item_updated"):
        super().__init__(name)
        address_list = range(0, self.get_ram_last_addr())
        self.rand("addr", address_list)
        self.write_size = "word"
        self.rand("write_size", ["byte", "half", "word"])
        self.constraint(
            lambda addr, write_size: (
                (addr % 4 == 0 and write_size == "word")
                or (addr % 2 == 0 and write_size == "half")
                or (write_size == "byte")
            )
        )
        self.data_post = None

    def post_randomize(self):
        if self.data_post is None:
            self.data = random.getrandbits(32)
        else:
            self.data = self.data_post

    def convert2string(self):
        if self.kind == bus_item.RESET:
            return sv.sformatf("RESET command send to DUT")
        if self.kind == bus_item.NOPE:
            return sv.sformatf("NO-OP command send to DUT")
        kind = "READ"
        if self.kind == 1:
            kind = "WRITE"
        try:
            return f"kind={kind}({self.write_size}) addr={hex(self.addr)} data={hex(self.data)}"
        except TypeError:
            return f"kind={kind}({self.write_size}) addr={self.addr} data={self.data}"

    def get_ram_last_addr(self):
        ram_size = []
        if UVMConfigDb.get(None, "*", "ram_size", ram_size) is True:
            ram_size = ram_size[0]
        else:
            uvm_fatal("NOVIF", "Could not get ram_size from config DB")
        return ram_size << 2


uvm_object_utils_begin(bus_item_updated)
uvm_field_int("addr", UVM_ALL_ON | UVM_NOPACK)
uvm_field_int("data", UVM_ALL_ON | UVM_NOPACK)
uvm_object_utils_end(bus_item_updated)
