SIM-RTL-128:
	iverilog -o ram128-rtl.vvp -s DFFRAM128x32_tb -DFUNCTIONAL -DUNIT_DELAY=#1 DFFRAM128x32_tb.v ../../hdl/rtl/DFFRAM128x32.v ../../hdl/rtl/DFFRAM.v sky130_fd_sc_hd.v primitives.v
	./ram128-rtl.vvp

SIM-GL-128:
	iverilog -o ram128-gl.vvp -s DFFRAM128x32_tb -DFUNCTIONAL -DUSE_POWER_PINS -DUNIT_DELAY=#1  ../../hdl/gl/DFFRAM128x32.v sky130_fd_sc_hd.v  primitives.v DFFRAM128x32_tb.v
	./ram128-gl.vvp

SIM-RTL-256:
	iverilog -o ram256-rtl.vvp -DFUNCTIONAL -DUNIT_DELAY=#1 DFFRAM256x32_tb.v ../../hdl/rtl/DFFRAM256x32.v ../../hdl/rtl/DFFRAM.v sky130_fd_sc_hd.v primitives.v
	./ram256-rtl.vvp

SIM-GL-256:
	iverilog -o ram128-gl.vvp -s DFFRAM256x32_tb -DFUNCTIONAL -DUSE_POWER_PINS -DUNIT_DELAY=#1  ../../hdl/gl/DFFRAM256x32.v sky130_fd_sc_hd.v  primitives.v DFFRAM256x32_tb.v
	./ram128-gl.vvp