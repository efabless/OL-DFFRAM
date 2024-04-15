from uvm.base.sv import sv_if


class bus_ahb_if_updated(sv_if):
    """HSIZE is new from other if"""

    def __init__(self, dut):
        bus_map = {
            "CLK": "CLK",
            "RESETn": "RESETn",
            "HADDR": "HADDR",
            "HWRITE": "HWRITE",
            "HSEL": "HSEL",
            "HREADYOUT": "HREADYOUT",
            "HTRANS": "HTRANS",
            "HWDATA": "HWDATA",
            "HRDATA": "HRDATA",
            "HREADY": "HREADY",
            "HSIZE": "HSIZE",
        }
        sv_if.__init__(self, dut, "", bus_map)
