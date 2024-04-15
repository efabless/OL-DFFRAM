from EF_UVM.bus_env.bus_agent.bus_ahb_driver import bus_ahb_driver
from uvm.macros import uvm_component_utils


class bus_ahb_driver_updated(bus_ahb_driver):
    """the HSIZE isn't handled for other AHB lite wrappers so this driver is for handing that for this wrapper"""

    def __init__(self, name="bus_ahb_driver_updated", parent=None):
        super().__init__(name, parent)

    def drv_optional_signals_address(self, tr):
        if tr.write_size == "byte":
            self.vif.HSIZE.value = 0b00
        elif tr.write_size == "half":
            self.vif.HSIZE.value = 0b01
        elif tr.write_size == "word":
            self.vif.HSIZE.value = 0b10


uvm_component_utils(bus_ahb_driver_updated)
