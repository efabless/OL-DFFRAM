from EF_UVM.bus_env.bus_agent.bus_ahb_monitor import bus_ahb_monitor
from uvm.macros import uvm_component_utils


class bus_ahb_monitor_updated(bus_ahb_monitor):
    """the HSIZE isn't handled for other AHB lite wrappers so this driver is for handing that for this wrapper"""

    def monitor_optional_signals_address(self, tr):
        if self.vif.HSIZE == 0b00:
            tr.write_size = "byte"
        elif self.vif.HSIZE == 0b01:
            tr.write_size = "half"
        elif self.vif.HSIZE == 0b10:
            tr.write_size = "word"
        return tr


uvm_component_utils(bus_ahb_monitor_updated)
