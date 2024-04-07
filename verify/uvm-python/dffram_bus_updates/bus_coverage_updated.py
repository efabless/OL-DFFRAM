from EF_UVM.bus_env.bus_coverage.bus_coverage import bus_coverage
from uvm.base.uvm_config_db import UVMConfigDb
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from cocotb_coverage.coverage import CoverPoint
from EF_UVM.bus_env.bus_item import bus_item


class bus_coverage_updated(bus_coverage):
    def __init__(self, name="bus_coverage_updated", parent=None):
        super().__init__(name)

    def build(self):
        super().build()
        self.cov = dffram_cov_groups(
            hierarchy="top.ip", size_in_words=self.get_ram_size()
        )

    def write_bus(self, tr):
        self.cov.sample(tr)

    def get_ram_size(self):
        ram_size = []
        if UVMConfigDb.get(None, "*", "ram_size", ram_size) is True:
            ram_size = ram_size[0]
        else:
            uvm_fatal("NOVIF", "Could not get ram_size from config DB")
        return ram_size


uvm_component_utils(bus_coverage_updated)


class dffram_cov_groups:
    def __init__(self, hierarchy, size_in_words):
        self.hierarchy = hierarchy
        self.size_in_words = size_in_words
        self.old_tr = None
        self.cov_points = self._cov_points()
        self.sample(None, do_sampling=False)

    def sample(self, tr, do_sampling=True):
        @self.apply_decorators(decorators=self.cov_points)
        def cov(tr):
            pass

        if do_sampling:
            cov(tr)
        self.old_tr = tr

    def _cov_points(self):
        cov_points = []
        access_size = ["word", "half", "byte"]
        access_type = {"read": bus_item.READ, "write": bus_item.WRITE}
        for access in access_type.keys():
            for size in access_size:
                cov_points.append(
                    CoverPoint(
                        f"{self.hierarchy}.{access}.{size}.data",
                        xf=lambda tr: (tr.kind, tr.data, tr.write_size),
                        bins=[i for i in range(31)],
                        bins_labels=[f"binary with {i} ones" for i in range(31)],
                        rel=lambda val, b, type=access_type[
                            access
                        ], size_type=size: type
                        == val[0]
                        and size_type == val[2]
                        and b == self._count_one_bits(val[1]),
                    )
                )
                cov_points.append(
                    CoverPoint(
                        f"{self.hierarchy}.{access}.{size}.address",
                        xf=lambda tr: (tr.kind, tr.addr, tr.write_size),
                        bins=[
                            (
                                i * 32,
                                i * 32 + 31,
                            )
                            for i in range(int(self.size_in_words / 8))
                        ],
                        bins_labels=[
                            f"from {hex(i * 32)} to {hex(i * 32 + 31)}"
                            for i in range(int(self.size_in_words / 8))
                        ],
                        rel=lambda val, b, type=access_type[
                            access
                        ], size_type=size: type
                        == val[0]
                        and size_type == val[2]
                        and b[0] <= val[1] <= b[1],
                    )
                )
        cov_points.append(
            CoverPoint(
                f"{self.hierarchy}.consecutives",
                xf=lambda tr: (tr.kind, tr.addr),
                bins=[
                    (i, j) for i in access_type.values() for j in access_type.values()
                ],
                bins_labels=[
                    f"{i}_{j}" for i in access_type.keys() for j in access_type.keys()
                ],
                rel=lambda val, b: self.old_tr is not None
                and b[0] == self.old_tr.kind
                and b[1] == val[0]
                and val[1] == self.old_tr.addr,
            )
        )
        return cov_points

    def get_update_old_tr(self, tr=None):
        temp = self.old_tr
        self.old_tr = tr
        return temp

    def _count_one_bits(self, num):
        count = 0
        while num:
            count += num & 1
            num >>= 1
        return count

    def apply_decorators(self, decorators):
        def decorator_wrapper(func):
            for decorator in decorators:
                func = decorator(func)
            return func

        return decorator_wrapper
