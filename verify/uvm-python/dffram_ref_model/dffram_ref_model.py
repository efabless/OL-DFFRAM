from uvm.base.uvm_component import UVMComponent
from uvm.macros import uvm_component_utils
from uvm.tlm1.uvm_analysis_port import UVMAnalysisImp
from uvm.base.uvm_object_globals import UVM_HIGH, UVM_LOW, UVM_MEDIUM
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info, uvm_error
from uvm.base.uvm_config_db import UVMConfigDb
from uvm.tlm1.uvm_analysis_port import UVMAnalysisExport
import cocotb
from EF_UVM.ref_model.ref_model import ref_model
from EF_UVM.bus_env.bus_item import bus_item


class dffram_ref_model(ref_model):
    """
    The reference model is a crucial element within the top-level verification environment, designed to validate the functionality and performance of both the IP (Intellectual Property) and the bus system. Its primary role is to act as a representative or mimic of the actual hardware components, including the IP and the bus. Key features and functions of the reference model include:
    1) Input Simulation: The reference model is capable of receiving the same inputs that would be provided to the actual IP and bus via connection with the monitors of the bus and IP.
    2) Functional Emulation: It emulates the behavior and responses of the IP and bus under test. By replicating the operational characteristics of these components, the reference model serves as a benchmark for expected performance and behavior.
    3) Output Generation: Upon receiving inputs, the reference model processes them in a manner akin to the real hardware, subsequently generating expected outputs. These outputs are essential for comparison in the verification process.
    4) Interface with Scoreboard: The outputs from the reference model, representing the expected results, are forwarded to the scoreboard. The scoreboard then compares these expected results with the actual outputs from the IP and bus for verification.
    5)Register Abstraction Layer (RAL) Integration: The reference model includes a RAL model that mirrors the register values of the RTL, ensuring synchronization between expected and actual register states. This model facilitates register-level tests and error detection, offering accessible and up-to-date register values for other verification components. It enhances the automation and coverage of register testing, playing a vital role in ensuring the accuracy and comprehensiveness of the verification process.
    """

    def __init__(self, name="dffram_ref_model", parent=None):
        super().__init__(name, parent)
        self.tag = name
        self.ris_reg = 0
        self.mis_reg = 0
        self.irq = 0

    def build_phase(self, phase):
        super().build_phase(phase)
        # get ram size
        ram_size = []
        if UVMConfigDb.get(None, "*", "ram_size", ram_size) is True:
            self.ram_size = ram_size[0]
        else:
            uvm_fatal("NOVIF", "Could not get ram_size from config DB")
        self.ram = DFF_Ram(self.ram_size)

    async def run_phase(self, phase):
        await super().run_phase(phase)
        pass

    def write_bus(self, tr):
        # Called when new transaction is received from the bus monitor
        # TODO: update the following logic to determine what to do with the received transaction
        uvm_info(
            self.tag,
            " Ref model recieved from bus monitor: " + tr.convert2string(),
            UVM_HIGH,
        )
        if tr.kind == bus_item.RESET:
            self.bus_bus_export.write(tr)
            uvm_info("Ref model", "reset from ref model", UVM_LOW)
            # TODO: write logic needed when reset is received
            self.ram.reset()
            self.bus_bus_export.write(tr)
            return
        if tr.kind == bus_item.WRITE:
            # TODO: write logic needed when write transaction is received
            # For example, to write the same value to the same resgiter uncomment the following lines
            # self.regs.write_reg_value(tr.addr, tr.data)
            # self.bus_bus_export.write(tr) # this is output to the scoreboard
            if tr.write_size == "byte":
                byte_number = tr.addr & 0b11
                data = (tr.data >> (byte_number * 8)) & 0xFF
                self.ram.write_byte(tr.addr, data)
            elif tr.write_size == "half":
                half_number = int((tr.addr & 0b10) == 0b10)
                data = (tr.data >> (half_number * 16)) & 0xFFFF
                if tr.addr & 0b1 != 0b0:
                    uvm_error(
                        self.tag,
                        f"Half word address not aligned transaction: {tr.convert2string()}",
                    )
                self.ram.write_half_word(tr.addr, data)
            elif tr.write_size == "word":
                if tr.addr & 0b11 != 0b00:
                    uvm_error(
                        self.tag,
                        f"Word address not aligned transaction: {tr.convert2string()}",
                    )
                self.ram.write_word(tr.addr, tr.data)
            pass
        elif tr.kind == bus_item.READ:
            # TODO: write logic needed when read transaction is received
            # For example, to read the same resgiter uncomment the following lines
            td = tr.do_clone()
            if tr.write_size == "byte":
                td.data = self.ram.read_word(tr.addr >> 2)
            elif tr.write_size == "half":
                if tr.addr & 0b1 != 0b0:
                    uvm_error(
                        self.tag,
                        f"Half word address not aligned transaction: {tr.convert2string()}",
                    )
                td.data = self.ram.read_word(tr.addr >> 2)
            elif tr.write_size == "word":
                if tr.addr & 0b11 != 0b00:
                    uvm_error(
                        self.tag,
                        f"Word address not aligned transaction: {tr.convert2string()}",
                    )
                td.data = self.ram.read_word(tr.addr >> 2)
            self.bus_bus_export.write(td)  # this is output to the scoreboard
            pass


uvm_component_utils(dffram_ref_model)


class DFF_Ram:
    WORD_SIZE = 4  # Each word is 4 bytes

    def __init__(self, size_in_words):
        self.size_in_bytes = size_in_words * DFF_Ram.WORD_SIZE
        self.memory = bytearray(self.size_in_bytes)
        uvm_info(
            "DFF_Ram",
            f"Initialized with size {self.size_in_bytes} bytes with {size_in_words}({type(size_in_words)}) words memory = {self.memory}",
            UVM_LOW,
        )

    def read(self, address, length=1):
        if address < 0 or address + length > self.size_in_bytes:
            raise ValueError("Address out of range")

        return int.from_bytes(self.memory[address : address + length], "little")

    def write(self, address, data, length=1):
        if address < 0 or address + length > self.size_in_bytes:
            raise ValueError(
                f"Address out of range byte_address={address} length={length} full size={self.size_in_bytes}bytes"
            )
        if len(data) != length:
            raise ValueError("Data length does not match the specified length")

        self.memory[address : address + length] = data

    def read_byte(self, address):
        return self.read(address, 1)

    def read_half_word(self, address):
        return self.read(address, 2)

    def read_word(self, address):
        address = address << 2
        data = self.read(address, DFF_Ram.WORD_SIZE)
        uvm_info(
            "DFF_Ram", f"read_word: {hex(data)} at address {hex(address)}", UVM_LOW
        )
        return data

    def write_byte(self, address, data):
        self.write(address, data.to_bytes(1, byteorder="little"), 1)

    def write_half_word(self, address, data):
        self.write(address, data.to_bytes(2, byteorder="little"), 2)

    def write_word(self, address, data):
        self.write(
            address,
            data.to_bytes(DFF_Ram.WORD_SIZE, byteorder="little"),
            DFF_Ram.WORD_SIZE,
        )

    def reset(self):
        self.memory = bytearray(self.size_in_bytes)
