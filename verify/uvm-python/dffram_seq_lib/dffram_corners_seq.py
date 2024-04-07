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


class dffram_corners_seq(dffram_bus_base_seq):
    # sequence to verify the corner cases in the ram
    def __init__(self, ram_size, name="dffram_bus_seq"):
        super().__init__(name)
        self.ram_size = ram_size

    async def body(self):
        await super().body()
        # initialize ram
        await uvm_do_with(self, dffram_init_seq(self.ram_size))
        # same address seq
        for _ in range(10):
            await uvm_do_with(self, dffram_same_address_seq(self.ram_size))
        await uvm_do_with(self, dffram_one_zeros_seq(self.ram_size))
        await uvm_do_with(self, dffram_lowest_highest_seq(self.ram_size))


uvm_object_utils(dffram_corners_seq)


class dffram_same_address_seq(dffram_bus_base_seq):
    def __init__(self, ram_size, name="dffram_same_address_seq"):
        super().__init__(name)
        self.ram_size_in_words = ram_size

    async def body(self):
        await super().body()
        pick_address = random.randint(0, self.ram_size_in_words - 1) << 2
        # randomly read and write to the same address 20 times
        for _ in range(25):
            if random.random() >= 0.5:
                await self.write_addr(lambda addr: addr == pick_address)
            else:
                await self.read_addr(lambda addr: addr == pick_address)


class dffram_one_zeros_seq(dffram_bus_base_seq):
    def __init__(self, ram_size, name="dffram_one_zeros_seq"):
        super().__init__(name)
        self.ram_size_in_words = ram_size

    async def body(self):
        await super().body()

        for _ in range(self.ram_size_in_words):
            data = random.choice(
                (0x0, 0xAAAAAAAA, 0x55555555, 0xFFFFFFFF, 0x33333333, 0xCCCCCCCC)
            )
            self.req.data_post = data
            await self.write_addr()

        for _ in range(self.ram_size_in_words):
            await self.read_addr()


class dffram_lowest_highest_seq(dffram_bus_base_seq):
    def __init__(self, ram_size, name="dffram_lowest_highest_seq"):
        super().__init__(name)
        self.ram_size_in_words = ram_size

    async def body(self):
        await super().body()
        # initialize with 0
        for _ in range(self.ram_size_in_words):
            self.req.data_post = 0
            await self.write_addr(lambda write_size: write_size == "word")

        # write then read small data
        for _ in range(self.ram_size_in_words):
            self.req.data_post = random.getrandbits(5)
            await self.write_addr()

        for _ in range(self.ram_size_in_words):
            await self.read_addr()

        # initialize with 0
        for _ in range(self.ram_size_in_words):
            self.req.data_post = 0
            await self.write_addr(lambda write_size: write_size == "word")

        # write then read large data
        for _ in range(self.ram_size_in_words):
            self.req.data_post = random.randint(2**25, 2**32 - 1)
            await self.write_addr()

        for _ in range(self.ram_size_in_words):
            await self.read_addr()
