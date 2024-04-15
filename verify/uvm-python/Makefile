PLUSARGS += "+UVM_VERBOSITY=UVM_MEDUIM"
TOPLEVEL := top
MODULE   ?= top_module
AHB_FILES ?= $(PWD)/../../hdl/rtl/bus_wrapper/DFFRAM128x32_ahbl.v $(PWD)/../../hdl/rtl/bus_wrapper/DFFRAM256x32_ahbl.v $(PWD)/../../hdl/rtl/bus_wrapper/DFFRAM512x32_ahbl.v $(PWD)/../../hdl/rtl/bus_wrapper/DFFRAM_ahbl.v
HDL_FILES ?= $(PWD)/../../hdl/rtl/DFFRAM.v $(PWD)/../../hdl/rtl/DFFRAM128x32.v $(PWD)/../../hdl/rtl/DFFRAM256x32.v $(PWD)/../../hdl/rtl/DFFRAM512x32.v
# PDK_FILES ?= $(PDK_ROOT)/sky130A/libs.ref/sky130_fd_sc_hd/verilog/primitives.v $(PDK_ROOT)/sky130A/libs.ref/sky130_fd_sc_hd/verilog/sky130_fd_sc_hd.v
PDK_FILES ?= $(PWD)/../utb/primitives.v $(PWD)/../utb/sky130_fd_sc_hd.v
PDK_DIR = $(PDK_ROOT)/sky130A/libs.ref/sky130_fd_sc_hd/verilog
VERILOG_SOURCES ?=  $(PWD)/top.v $(AHB_FILES) $(HDL_FILES) $(PDK_FILES)
RTL_MACROS ?= -DFUNCTIONAL -DUNIT_DELAY=\#1
BUS_TYPE ?= AHB
RTL_MACROS += -DBUS_TYPE_AHB

RAM_SIZE ?= 128

ifeq ($(RAM_SIZE),128)
    RTL_MACROS += -DRAM128
    YAML_FILE = $(PWD)/../../DFFRAM128x32.yaml
    POST_SYS_FILES = $(PWD)/top.v $(AHB_FILES) $(PWD)/../../hdl/gl/DFFRAM128x32.v
else ifeq ($(RAM_SIZE),256)
    RTL_MACROS += -DRAM256
    YAML_FILE = $(PWD)/../../DFFRAM256x32.yaml
    POST_SYS_FILES = $(PWD)/top.v $(AHB_FILES) $(PWD)/../../hdl/gl/DFFRAM256x32.v
else ifeq ($(RAM_SIZE),512)
    RTL_MACROS += -DRAM512
    YAML_FILE = $(PWD)/../../DFFRAM512x32.yaml
    POST_SYS_FILES = $(PWD)/top.v $(AHB_FILES) $(PWD)/../../hdl/gl/DFFRAM512x32.v
endif
GL_MACROS +=  $(RTL_MACROS) -DUSE_POWER_PINS
MAKEFLAGS += --no-print-directory
SKIP_SYNTHESIS = true

# List of tests
TESTS := dffram_wr_rd_test  dffram_corners_test

# Variable for tag - set this as required
SIM_TAG ?= default_tag

# Define SIM_PATH variable
SIM_PATH := $(PWD)/sim/$(SIM_TAG)

# Check and clone EF_UVM repository at the beginning of the Makefile execution

clone_ef_uvm := $(shell if [ ! -d "EF_UVM" ]; then \
	echo "Cloning the EF_UVM repository..."; \
	git clone https://github.com/efabless/EF_UVM.git; \
fi;)


include EF_UVM/Makefile.test
