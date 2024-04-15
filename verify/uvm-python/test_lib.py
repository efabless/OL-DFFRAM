import cocotb
import os
import re
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from uvm.base.uvm_config_db import UVMConfigDb
from uvm.base.uvm_object_globals import UVM_LOW
from uvm.base.uvm_globals import run_test
from dffram_interface.dffram_if import dffram_if
from EF_UVM.bus_env.bus_interface.bus_if import (
    bus_apb_if,
    bus_irq_if,
    bus_ahb_if,
    bus_wb_if,
)
from cocotb_coverage.coverage import coverage_db
from cocotb.triggers import Event, First
from EF_UVM.bus_env.bus_regs import bus_regs
from uvm.base import UVMRoot
from EF_UVM.base_test import base_test

# seqences import
from dffram_seq_lib.dffram_write_read_seq import dffram_write_read_seq
from dffram_seq_lib.dffram_corners_seq import dffram_corners_seq
from dffram_seq_lib.dffram_ip_seq import dffram_ip_seq

# override classes
from EF_UVM.ip_env.ip_agent.ip_driver import ip_driver
from dffram_agent.dffram_driver import dffram_driver
from EF_UVM.ip_env.ip_agent.ip_monitor import ip_monitor
from dffram_agent.dffram_monitor import dffram_monitor
from EF_UVM.ref_model.ref_model import ref_model
from dffram_ref_model.dffram_ref_model import dffram_ref_model
from EF_UVM.ip_env.ip_coverage.ip_coverage import ip_coverage
from dffram_coverage.dffram_coverage import dffram_coverage
from EF_UVM.ip_env.ip_logger.ip_logger import ip_logger
from dffram_logger.dffram_logger import dffram_logger

#
from EF_UVM.bus_env.bus_item import bus_item
from dffram_bus_updates.bus_item_updated import bus_item_updated
from dffram_bus_updates.bus_ahb_if_updated import bus_ahb_if_updated
from EF_UVM.bus_env.bus_agent.bus_ahb_monitor import bus_ahb_monitor
from dffram_bus_updates.bus_ahb_monitor_updated import bus_ahb_monitor_updated
from EF_UVM.bus_env.bus_agent.bus_ahb_driver import bus_ahb_driver
from dffram_bus_updates.bus_ahb_driver_updated import bus_ahb_driver_updated
from EF_UVM.bus_env.bus_agent.bus_apb_driver import bus_apb_driver
from dffram_bus_updates.bus_coverage_updated import bus_coverage_updated
from EF_UVM.bus_env.bus_coverage.bus_coverage import bus_coverage


@cocotb.test()
async def module_top(dut):
    # profiler = cProfile.Profile()
    # profiler.enable()
    BUS_TYPE = cocotb.plusargs["BUS_TYPE"]
    pif = dffram_if(dut)
    if BUS_TYPE == "APB":
        w_if = bus_apb_if(dut)
    elif BUS_TYPE == "AHB":
        w_if = bus_ahb_if_updated(dut)
    elif BUS_TYPE == "WISHBONE":
        w_if = bus_wb_if(dut)
    else:
        uvm_fatal("module_top", f"unknown bus type {BUS_TYPE}")
    UVMConfigDb.set(None, "*", "ip_if", pif)
    UVMConfigDb.set(None, "*", "bus_if", w_if)
    yaml_file = []
    UVMRoot().clp.get_arg_values("+YAML_FILE=", yaml_file)
    yaml_file = yaml_file[0]
    regs = bus_regs(yaml_file)
    UVMConfigDb.set(None, "*", "bus_regs", regs)
    UVMConfigDb.set(None, "*", "irq_exist", False)
    UVMConfigDb.set(None, "*", "collect_coverage", True)
    UVMConfigDb.set(None, "*", "disable_logger", False)
    test_path = []
    UVMRoot().clp.get_arg_values("+TEST_PATH=", test_path)
    test_path = test_path[0]
    # get RAM size
    ram_size = get_ram_size(yaml_file)
    if ram_size is None:
        uvm_fatal("module_top", "Could not get ram_size from yaml file")
    else:
        UVMConfigDb.set(None, "*", "ram_size", ram_size)
        uvm_info("module_top", f"detect ram with size {ram_size} words", UVM_LOW)
    # get bus type
    await run_test()
    coverage_db.export_to_yaml(filename=f"{test_path}/coverage.yalm")
    # profiler.disable()
    # profiler.dump_stats("profile_result.prof")


def get_ram_size(yaml_file):
    normalized_path = os.path.abspath(yaml_file)

    # Use a regular expression to find numbers in the file name
    match = re.search(r"(\d+)x\d+\.yaml$", normalized_path)
    if match:
        return int(match.group(1))
    else:
        return None


class dffram_base_test(base_test):
    def __init__(self, name="dffram_first_test", parent=None):
        BUS_TYPE = cocotb.plusargs["BUS_TYPE"]
        super().__init__(name, bus_type=BUS_TYPE, parent=parent)
        self.set_type_override_by_type(bus_item.get_type(), bus_item_updated.get_type())

        self.tag = name

    def build_phase(self, phase):
        super().build_phase(phase)
        # override
        self.set_type_override_by_type(ip_driver.get_type(), dffram_driver.get_type())
        self.set_type_override_by_type(ip_monitor.get_type(), dffram_monitor.get_type())
        self.set_type_override_by_type(
            ref_model.get_type(), dffram_ref_model.get_type()
        )
        self.set_type_override_by_type(
            ip_coverage.get_type(), dffram_coverage.get_type()
        )
        self.set_type_override_by_type(ip_logger.get_type(), dffram_logger.get_type())
        self.set_type_override_by_type(
            bus_ahb_monitor.get_type(), bus_ahb_monitor_updated.get_type()
        )
        self.set_type_override_by_type(
            bus_ahb_driver.get_type(), bus_ahb_driver_updated.get_type()
        )
        self.set_type_override_by_type(
            bus_coverage.get_type(), bus_coverage_updated.get_type()
        )
        ram_size = []
        if UVMConfigDb.get(None, "*", "ram_size", ram_size) is True:
            self.ram_size = ram_size[0]
        else:
            uvm_fatal("NOVIF", "Could not get ram_size from config DB")


uvm_component_utils(dffram_base_test)


class dffram_wr_rd_test(dffram_base_test):
    def __init__(self, name="dffram__first_test", parent=None):
        super().__init__(name, parent=parent)
        self.tag = name

    async def main_phase(self, phase):
        # await super().run_phase(phase)
        phase.raise_objection(self, f"{self.__class__.__name__} OBJECTED")
        uvm_info(self.tag, f"Starting test {self.__class__.__name__}", UVM_LOW)
        # TODO: conntect sequence with sequencer here
        # for example if you need to run the 2 sequence sequentially
        bus_seq = dffram_write_read_seq(self.ram_size, "dffram_write_read_seq")
        # ip_seq = dffram_ip_seq("dffram_ip_seq")
        await bus_seq.start(self.bus_sqr)
        # await ip_seq.start(self.ip_sqr)
        phase.drop_objection(self, f"{self.__class__.__name__} drop objection")


uvm_component_utils(dffram_wr_rd_test)


class dffram_corners_test(dffram_base_test):
    def __init__(self, name="dffram__first_test", parent=None):
        super().__init__(name, parent=parent)
        self.tag = name

    async def main_phase(self, phase):
        # await super().run_phase(phase)
        phase.raise_objection(self, f"{self.__class__.__name__} OBJECTED")
        uvm_info(self.tag, f"Starting test {self.__class__.__name__}", UVM_LOW)
        # TODO: conntect sequence with sequencer here
        # for example if you need to run the 2 sequence sequentially
        bus_seq = dffram_corners_seq(self.ram_size, "dffram_corners_seq")
        # ip_seq = dffram_ip_seq("dffram_ip_seq")
        await bus_seq.start(self.bus_sqr)
        # await ip_seq.start(self.ip_sqr)
        phase.drop_objection(self, f"{self.__class__.__name__} drop objection")


uvm_component_utils(dffram_corners_test)
